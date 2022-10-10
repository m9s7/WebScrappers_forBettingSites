# don't need cookies for mozart
import pandas as pd

from models.common_functions import print_to_file
from models.match_model import Subgames
from requests_to_server.mozzart_requests import get_curr_sidebar_sports_and_leagues, get_all_subgames, get_match_ids, \
    get_odds


# Get a specific "sport" that is currently offered
def get_sport_with_name(name, sidebar_sports):
    for sport in sidebar_sports:
        if sport['name'] == name:
            # Can return list of ( sportId, sportName ) pairs, because IDs are needed to get subgames
            # print(name, " id: ", sport['id'])
            return sport
    return None


# Focused subgames are subgames I plan on comparing with other betting sites
def get_focused_subgames(offers, sport_name):
    focused_subgames = []

    for offer in offers:
        # Maybe switch to 'Kompletna ponuda' because there is everything there but idk
        if offer['name'] != "Konačan ishod":
            continue

        for header in offer['regularHeaders']:
            if len(header['gameName']) != 1:
                print("FINALLY FOUND AN INCONSISTENCY IN MOZZART DATA STRUCTURE")
                exit(1)
            game = header['gameName'][0]
            short_name = game['shortName']

            if sport_name == "Tenis" or sport_name == "Esports":
                if short_name != 'ki':
                    continue
                for subgame in header['subGameName']:
                    focused_subgames.append(subgame['id'])

            if sport_name == "Košarka":
                if short_name != 'pobm':
                    continue
                for subgame in header['subGameName']:
                    focused_subgames.append(subgame['id'])

    return focused_subgames


def scrape():
    print("...scraping mozz")

    columns = ['1', '2', 'KI_1', 'KI_2']

    sidebar_sports_response_json = get_curr_sidebar_sports_and_leagues().json()

    all_subgames_dictionary = get_all_subgames().json()
    # Format:
    # all_subgames_dictionary is a map where keys are ordered integers [1..77]
    # and values are lists which contain subgame dictionaries

    # See which sports there are
    # for ss in sidebar_sports_response_json:
    #     print(ss['name'])

    # Get sports you are interested in

    sport_names = ["Tenis", "Košarka", "Esports"]
    results = {}
    interested_subgames = {
        "Tenis": 'ki',
        "Košarka": 'pobm',
        "Esports": 'ki'
    }
    for sport_name in sport_names:

        sport = get_sport_with_name(sport_name, sidebar_sports_response_json)
        if sport is None:
            print("Send email")
            exit(1)

        sport_id = sport['id']

        # Get subgameIds za "Konačan ishod"
        offer_list = all_subgames_dictionary[str(sport_id)]
        subgames = get_focused_subgames(offer_list, sport_name)

        # Get matches and participants
        matches_response = get_match_ids(sport_id).json()['matches']

        # Parse matches
        export = {}
        for match in matches_response:
            if match['specialType'] != 0 or len(match['participants']) != 2:
                continue
            e = [match['participants'][0]['name'], match['participants'][1]['name'], None, None]
            export[match['id']] = e

        # For testing with Insomnia
        # print(list(export.keys())[1:10], " - ", subgames)

        # Get odds for chosen matches and subgames
        odds = get_odds(list(export.keys()), subgames).json()

        for o in odds:
            if "kodds" not in o:
                continue

            match_id = o['id']
            for sg in o['kodds'].values():
                if sg is None:
                    continue

                # Should have try catch blocks to raise exceptions and not break the program
                if "subGame" not in sg:
                    print("WTF")
                    continue

                # Konačan ishod
                if sg['subGame']['gameShortName'] == interested_subgames[sport_name]:
                    if sg['subGame']['subGameName'] == 'x' or sg['subGame']['subGameName'] == 'X':
                        print("WHAT mozz_scrape")

                    if sg['subGame']['subGameName'] == '1':
                        export[match_id][Subgames.FT_OT_1] = sg['value']
                    elif sg['subGame']['subGameName'] == '2':
                        export[match_id][Subgames.FT_OT_2] = sg['value']
                    else:
                        continue

        # Format result
        df = pd.DataFrame(list(export.values()), columns=columns)
        print_to_file(df.to_string(), f"mozz_{sport_name}.txt")
        results[sport_name] = df

    return results


# scrape()
