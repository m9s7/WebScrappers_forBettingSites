import time

from maxbet.specific_sport_data_parsers.basketball_parser import parse_basketball_data
from maxbet.specific_sport_data_parsers.football_parser import parse_football_data
from maxbet.specific_sport_data_parsers.general_ki_parser import parse_ki_data
from models.common_functions import print_to_file
from requests_to_server.maxbet_requests import get_sport_data, get_curr_sidebar_sports_and_leagues


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


def scrape():
    start_time = time.time()
    print("...scraping maxbet")

    results = {}

    # Do error checking maybe
    sidebar_sports_and_leagues = parse_sidebar(get_curr_sidebar_sports_and_leagues().json())

    # Get data for every sport or just IDs for every sport
    sport_ids = {}
    for i, sport in enumerate(sidebar_sports_and_leagues):
        # print(f"{i}: ", sport['name'])
        sport_ids[sport['name']] = i
        # res_json = get_sport_data(sport, cookie).json()

    # print(sport_ids.keys())

    if 'Tenis' in sport_ids:
        tennis_data_response_json = get_sport_data(sidebar_sports_and_leagues[sport_ids['Tenis']]).json()
        df_tennis = parse_ki_data(tennis_data_response_json)
        print_to_file(df_tennis.to_string(), "maxb_tennis.txt")
        results['Tenis'] = df_tennis

    if 'eSport' in sport_ids:
        esport_data_response_json = get_sport_data(sidebar_sports_and_leagues[sport_ids['eSport']]).json()
        df_esport = parse_ki_data(esport_data_response_json)
        print_to_file(df_esport.to_string(), "maxb_eSport.txt")
        results['Esports'] = df_esport

    if 'Košarka' in sport_ids:
        basketball_data_response_json = get_sport_data(sidebar_sports_and_leagues[sport_ids['Košarka']]).json()
        df_basketball = parse_basketball_data(basketball_data_response_json)
        print_to_file(df_basketball.to_string(), "maxb_basketball.txt")
        results['Košarka'] = df_basketball

    if 'Fudbal' in sport_ids:
        football_data_response_json = get_sport_data(sidebar_sports_and_leagues[sport_ids['Fudbal']]).json()
        df_football = parse_football_data(football_data_response_json)
        print_to_file(df_football.to_string(), "maxb_football.txt")
        results['Fudbal'] = df_football

    print("--- %s seconds ---" % (time.time() - start_time))
    return results


# scrape()
