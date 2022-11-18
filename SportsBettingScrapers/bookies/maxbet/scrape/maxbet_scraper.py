import time

from bookies.maxbet.scrape.odds_parsers.soccer_odds_parser import get_soccer_odds
from bookies.maxbet.scrape.odds_parsers.general_2outcome_odds_parser import get_2outcome_odds
from bookies.maxbet.standardize.standardization_functions import standardize_tennis_tip_name, \
    standardize_table_tennis_tip_name, \
    standardize_esports_tip_name, standardize_basketball_tip_name, standardize_soccer_tip_name, \
    standardize_kickoff_time_string
from common.common_functions import print_to_file, export_for_merge, box_print
from common.models import MaxbNames, ExportIDX
from requests_to_server.maxbet_requests import get_match_ids, get_curr_sidebar_sports_and_leagues


# Returns a dict { key = sport_name, val = [LeagueBetId] }
def parse_sidebar(sidebar_sports_json):
    sports = {}

    for sport in sidebar_sports_json:
        league_bet_ids = []
        for league_dict in sport['leagues']:
            if str(league_dict['name']).startswith("Max Bonus Tip"):
                continue
            league_bet_ids.append(league_dict['betLeagueId'])

        if len(league_bet_ids) != 0:
            sports[sport['name']] = league_bet_ids

    return sports


def get_sports_currently_offered():
    response = get_curr_sidebar_sports_and_leagues()
    while response is None:
        print("Stuck on getting maxbet sidebar info")
        response = get_curr_sidebar_sports_and_leagues()
    sports = [sport['name'] for sport in response]
    return sports


def parse_get_matches_response(response):
    matches = []
    for league in response:
        for match in league['matchList']:
            matches.append(match['id'])
    return matches


def get_standardization_func_4_tip_names(sport):
    if sport == MaxbNames.tennis:
        return standardize_tennis_tip_name
    if sport == MaxbNames.esports:
        return standardize_esports_tip_name
    if sport == MaxbNames.basketball:
        return standardize_basketball_tip_name
    if sport == MaxbNames.tabletennis:
        return standardize_table_tennis_tip_name
    if sport == MaxbNames.soccer:
        return standardize_soccer_tip_name
    raise TypeError('No tip name standardization function for sport enum: ', sport)


def scrape(sports_to_scrape):
    start_time = time.time()
    box_print("scraping max")

    response = get_curr_sidebar_sports_and_leagues()
    while response is None:
        print("Stuck on getting maxbet sidebar info")
        response = get_curr_sidebar_sports_and_leagues()

    sidebar = parse_sidebar(response)

    for sport in sports_to_scrape:

        try:
            sidebar[sport]
        except KeyError:
            print(sport, " not currently offered at maxbet")
            continue

        sport_standard_name = sport.toStandardName()
        print(f"...scraping maxb - {str(sport_standard_name)}")

        response_json = None
        while response_json is None:
            response_json = get_match_ids(sidebar[sport])
        matches_list = parse_get_matches_response(response_json)

        df = None
        if sport == MaxbNames.tennis:
            df = get_2outcome_odds(matches_list,
                                   ['Konačan ishod', 'Prvi set', 'Drugi set', 'Tie Break', 'Tie Break prvi set'])
        if sport == MaxbNames.esports:
            df = get_2outcome_odds(matches_list, ['Konačan ishod'])
        if sport == MaxbNames.basketball:
            df = get_2outcome_odds(matches_list, ['Konačan ishod sa produžecima'])
        if sport == MaxbNames.tabletennis:
            df = get_2outcome_odds(matches_list, ['Konačan ishod', 'Prvi set'])
        if sport == MaxbNames.soccer:
            df = get_soccer_odds(matches_list)

        standardize_tip_name = get_standardization_func_4_tip_names(sport)
        col_name = df.columns[ExportIDX.KICKOFF]
        df[col_name] = df[col_name].map(standardize_kickoff_time_string)
        col_name = df.columns[ExportIDX.TIP1_NAME]
        df[col_name] = df[col_name].map(standardize_tip_name)
        col_name = df.columns[ExportIDX.TIP2_NAME]
        df[col_name] = df[col_name].map(standardize_tip_name)

        print_to_file(df.to_string(index=False), f"maxb_{str(sport_standard_name)}.txt")
        export_for_merge(df, f"maxb_{str(sport_standard_name)}.txt")

    print("--- %s seconds ---" % (time.time() - start_time))
