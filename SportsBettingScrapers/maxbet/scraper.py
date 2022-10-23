import time

from maxbet.specific_sport_data_parsers.basketball_parser import parse_basketball_data
from maxbet.specific_sport_data_parsers.football_parser import parse_football_data
from maxbet.specific_sport_data_parsers.general_ki_parser import parse_ki_data
from models.common_functions import print_to_file, export_for_merge
from models.match_model import StandardNames, MaxbNames
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

    print("...scraping maxb - tennis")
    if 'Tenis' in sport_ids:
        tennis_data_response_json = get_sport_data(sidebar_sports_and_leagues[sport_ids[MaxbNames.tennis]]).json()
        df_tennis = parse_ki_data(tennis_data_response_json)
        print_to_file(df_tennis.to_string(), "maxb_tennis.txt")
        export_for_merge(df_tennis, "maxb_tennis.txt")
        results[StandardNames.tennis] = df_tennis

    print("...scraping maxb - esports")
    if 'eSport' in sport_ids:
        esport_data_response_json = get_sport_data(sidebar_sports_and_leagues[sport_ids[MaxbNames.esports]]).json()
        df_esport = parse_ki_data(esport_data_response_json)
        print_to_file(df_esport.to_string(), "maxb_esports.txt")
        export_for_merge(df_esport, "maxb_esports.txt")
        results[StandardNames.esports] = df_esport

    print("...scraping maxb - košarka")
    if 'Košarka' in sport_ids:
        basketball_data_response_json = get_sport_data(sidebar_sports_and_leagues[sport_ids[MaxbNames.basketball]]).json()
        df_basketball = parse_basketball_data(basketball_data_response_json)
        print_to_file(df_basketball.to_string(), "maxb_basketball.txt")
        export_for_merge(df_basketball, "maxb_basketball.txt")
        results[StandardNames.basketball] = df_basketball

    print("...scraping maxb - fudbal")
    if 'Fudbal' in sport_ids:
        soccer_data_response_json = get_sport_data(sidebar_sports_and_leagues[sport_ids[MaxbNames.soccer]]).json()
        df_soccer = parse_football_data(soccer_data_response_json)
        print_to_file(df_soccer.to_string(), "maxb_soccer.txt")
        export_for_merge(df_soccer, "maxb_soccer.txt")
        results[StandardNames.soccer] = df_soccer

    print("--- %s seconds ---" % (time.time() - start_time))
    return results


# scrape()
