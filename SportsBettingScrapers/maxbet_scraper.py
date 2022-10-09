import sys
import pandas as pd

from models.common_functions import print_to_file, nice_print_json
from models.match_model import Subgames
from requests_to_server.maxbet_requests import get_sport_data, get_curr_sidebar_sports_and_leagues, get_match_data


# Returns a list of dicts
# {
#     "name": string,                   # Sport name
#     "leagues": [(string, int)]        # list of pairs ( League_name, League ID )
# }
def parse_sidebar(sidebar_sports_json):
    sports = []

    for sport in sidebar_sports_json:
        my_sport = {
            'name': sport['name'],
            'leagues': [],
        }
        for league_dict in sport['leagues']:
            if str(league_dict['name']).startswith("Max Bonus Tip"):
                continue
            my_sport['leagues'].append((league_dict['name'], league_dict['betLeagueId']))

        if len(my_sport['leagues']) != 0:
            sports.append(my_sport)
    return sports


def parse_tennis_data(response_json):
    export = {}
    for league in response_json:
        for match in league['matchList']:
            e = [match['home'], match['away'], None, None]
            for i in match['odBetPickGroups']:
                for j in i['tipTypes']:
                    if j['tipType'] == "KI_1":
                        e[Subgames.KI_1] = j['value']
                    elif j['tipType'] == "KI_2":
                        e[Subgames.KI_2] = j['value']
                    else:
                        continue
            export[match['id']] = e

    columns = ['1', '2', 'KI_1', 'KI_2']

    # index = list(export.keys())
    # , index = index
    df = pd.DataFrame(list(export.values()), columns=columns)

    df['sport'] = "Tennis"
    return df


def parse_basketball_data(response_json):
    export = {}
    for league in response_json:
        for match in league['matchList']:

            match_info = get_match_data(match['id']).json()

            e = [match['home'], match['away'], None, None]
            for subgame in match_info['odBetPickGroups']:
                if subgame['name'] != "Konačan ishod sa produžecima":
                    continue
                e[Subgames.FT_OT_1] = subgame['tipTypes'][0]['value']
                e[Subgames.FT_OT_2] = subgame['tipTypes'][1]['value']

            export[match['id']] = e

    columns = ['1', '2', 'KI_1', 'KI_2']

    df = pd.DataFrame(list(export.values()), columns=columns)
    df['sport'] = "Basketball"

    return df


def scrape():
    print("...scraping maxbet")

    # Do error checking maybe
    sidebar_sports_and_leagues = parse_sidebar(get_curr_sidebar_sports_and_leagues().json())

    # Get data for every sport or just IDs for every sport
    sport_ids = {}
    for i, sport in enumerate(sidebar_sports_and_leagues):
        # print(f"{i}: ", sport['name'])
        sport_ids[sport['name']] = i
        # res_json = get_sport_data(sport, cookie).json()

    tennis_data_response_json = get_sport_data(sidebar_sports_and_leagues[sport_ids['Tenis']]).json()
    df_tennis = parse_tennis_data(tennis_data_response_json)
    print_to_file(df_tennis.to_string(), "maxb_tennis.txt")

    basketball_data_response_json = get_sport_data(sidebar_sports_and_leagues[sport_ids['Košarka']]).json()
    df_basketball = parse_basketball_data(basketball_data_response_json)
    print_to_file(df_basketball.to_string(), "maxb_basketball.txt")

    df = pd.concat([df_tennis, df_basketball], axis=0)
    # print_to_file(df.to_string(), "result.txt")

    return df
