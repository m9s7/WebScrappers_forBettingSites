# don't need cookies for mozart
import sys
import pandas as pd

from models.match_model import Subgames
from requests_to_server.mozzart_requests import get_curr_sidebar_sports_and_leagues, get_all_subgames, get_match_ids, \
    get_odds


def print_to_file(data):
    original_stdout = sys.stdout
    with open('mozz_tennis.txt', 'w', encoding="utf-8") as f:
        sys.stdout = f
        print(data)
        sys.stdout = original_stdout


# Get a specific "sport" that is currently offered
def get_sport_with_name(name, sidebar_sports):
    for sport in sidebar_sports:
        if sport['name'] == name:
            # Can return list of ( sportId, sportName ) pairs, because IDs are needed to get subgames
            print(name, " id: ", sport['id'])
            return sport
    return None


# Focused subgames are subgames I plan on comparing with other betting sites
def get_focused_subgames_for_sport_id(sport_id):
    all_subgames_dictionary = get_all_subgames().json()
    # Format:
    # all_subgames_dictionary is a map where keys are ordered integers [1..77]
    # and values are lists which contain subgame dictionaries

    offer_list = all_subgames_dictionary[str(sport_id)]
    focused_subgames = []

    for offer in offer_list:
        if offer['name'] != "Konačan ishod":
            continue
        # offer_id = offer['id']
        # print("Offer name ", offer['name'])

        for header in offer['regularHeaders']:
            if len(header['gameName']) != 1:
                print("KONACNO SMO NASLI ODSTUPANJE OD OVE GLUPE STRUKTURE")
                exit(1)
            game = header['gameName'][0]
            # game_id = game['id']
            short_name = game['shortName']
            if short_name != 'ki':
                continue
            for subgame in header['subGameName']:
                subgame_id = subgame['id']
                focused_subgames.append(subgame_id)
                # subgame_name = subgame['name']
                # subgame_desc = subgame['description']
                # print(subgame_id, " - ", subgame_name, " (", subgame_desc, ")")

    return focused_subgames


def scrape():
    sidebar_sports_response_json = get_curr_sidebar_sports_and_leagues().json()

    # Košarka nema kodds?
    # Limit yourself to tennis
    tennis = get_sport_with_name("Tenis", sidebar_sports_response_json)
    if tennis is None:
        print("Send email")
        exit(1)
    tennis_id = tennis['id']

    # Get subgameIds za "Konacan ishod"
    subgames = get_focused_subgames_for_sport_id(tennis_id)

    # Get matches and participants
    matches_response = get_match_ids(tennis_id).json()['matches']

    # Parse matches
    export = {}
    for match in matches_response:
        if match['specialType'] != 0:
            continue
        e = [match['participants'][0]['name'], match['participants'][1]['name'], None, None]
        export[match['id']] = e

    # For testing with Insomnia
    # print(list(export.keys())[1:10], " - ", subgames)

    # Get odds for chosen matches and subgames
    odds = get_odds(list(export.keys()), subgames).json()

    # Parse odds
    for o in odds:
        match_id = o['id']
        for sg in o['kodds'].values():

            # Konacan ishod
            if sg['subGame']['gameShortName'] == 'ki':
                if sg['subGame']['subGameName'] == '1':
                    export[match_id][Subgames.KI_1] = sg['value']
                elif sg['subGame']['subGameName'] == '2':
                    export[match_id][Subgames.KI_2] = sg['value']
                else:
                    continue

    # Format result
    columns = ['1', '2', 'KI_1', 'KI_2']
    index = list(export.keys())

    df = pd.DataFrame(list(export.values()), columns=columns, index=index)

    print(df.to_string())
    return df
