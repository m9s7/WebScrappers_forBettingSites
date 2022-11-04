import time

from maxbet.scrape.odds_parsers.soccer_odds_parser import get_soccer_odds
from maxbet.scrape.odds_parsers.general_2outcome_odds_parser import get_2outcome_odds
from maxbet.standardize.standardization_functions import standardize_tennis_tip_name, standardize_table_tennis_tip_name, \
    standardize_esports_tip_name, standardize_basketball_tip_name, standardize_soccer_tip_name
from models.common_functions import print_to_file, export_for_merge
from models.match_model import StandardNames, MaxbNames, ExportIDX
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
    sports = [sport['name'] for sport in response]
    return sports


def parse_get_matches_response(response):
    matches = []
    for league in response:
        for match in league['matchList']:
            matches.append(match['id'])
    return matches


# Pass in a list of sports you want to scrape
def scrape():
    start_time = time.time()

    results = {}
    sidebar = parse_sidebar(get_curr_sidebar_sports_and_leagues())

    if MaxbNames.tabletennis in sidebar:
        print("...scraping maxb - table tennis")

        response_json = get_match_ids(sidebar[MaxbNames.tabletennis])
        matches_list = parse_get_matches_response(response_json)

        df_tabletennis = get_2outcome_odds(matches_list, ['Konačan ishod', 'Prvi set'])

        # Standardize tip names
        col_name = df_tabletennis.columns[ExportIDX.TIP1_NAME]
        df_tabletennis[col_name] = df_tabletennis[col_name].map(standardize_table_tennis_tip_name)
        col_name = df_tabletennis.columns[ExportIDX.TIP2_NAME]
        df_tabletennis[col_name] = df_tabletennis[col_name].map(standardize_table_tennis_tip_name)

        results[StandardNames.tabletennis] = df_tabletennis

        print_to_file(df_tabletennis.to_string(index=False), "maxb_table_tennis.txt")
        export_for_merge(df_tabletennis, "maxb_table_tennis.txt")

    if MaxbNames.tennis in sidebar:
        print("...scraping maxb - tennis")

        response_json = get_match_ids(sidebar[MaxbNames.tennis])
        matches_list = parse_get_matches_response(response_json)

        df_tennis = get_2outcome_odds(matches_list, ['Konačan ishod', 'Prvi set', 'Drugi set', 'Tie Break', 'Tie Break prvi set'])

        # Standardize tip names
        col_name = df_tennis.columns[ExportIDX.TIP1_NAME]
        df_tennis[col_name] = df_tennis[col_name].map(standardize_tennis_tip_name)
        col_name = df_tennis.columns[ExportIDX.TIP2_NAME]
        df_tennis[col_name] = df_tennis[col_name].map(standardize_tennis_tip_name)

        results[StandardNames.tennis] = df_tennis

        print_to_file(df_tennis.to_string(index=False), "maxb_tennis.txt")
        export_for_merge(df_tennis, "maxb_tennis.txt")

    if MaxbNames.esports in sidebar:
        print("...scraping maxb - esports")

        response_json = get_match_ids(sidebar[MaxbNames.esports])
        matches_list = parse_get_matches_response(response_json)

        df_esports = get_2outcome_odds(matches_list, ['Konačan ishod'])

        # Standardize tip names
        col_name = df_esports.columns[ExportIDX.TIP1_NAME]
        df_esports[col_name] = df_esports[col_name].map(standardize_esports_tip_name)
        col_name = df_esports.columns[ExportIDX.TIP2_NAME]
        df_esports[col_name] = df_esports[col_name].map(standardize_esports_tip_name)

        results[StandardNames.esports] = df_esports

        print_to_file(df_esports.to_string(index=False), "maxb_esports.txt")
        export_for_merge(df_esports, "maxb_esports.txt")

    if MaxbNames.basketball in sidebar:
        print("...scraping maxb - basketball")

        response_json = get_match_ids(sidebar[MaxbNames.basketball])
        matches_list = parse_get_matches_response(response_json)

        df_basketball = get_2outcome_odds(matches_list, ['Konačan ishod sa produžecima'])

        # Standardize tip names
        col_name = df_basketball.columns[ExportIDX.TIP1_NAME]
        df_basketball[col_name] = df_basketball[col_name].map(standardize_basketball_tip_name)
        col_name = df_basketball.columns[ExportIDX.TIP2_NAME]
        df_basketball[col_name] = df_basketball[col_name].map(standardize_basketball_tip_name)

        results[StandardNames.basketball] = df_basketball

        print_to_file(df_basketball.to_string(index=False), "maxb_basketball.txt")
        export_for_merge(df_basketball, "maxb_basketball.txt")

    if MaxbNames.soccer in sidebar:
        print("...scraping maxb - soccer")

        response_json = get_match_ids(sidebar[MaxbNames.soccer])
        matches_list = parse_get_matches_response(response_json)

        df_soccer = get_soccer_odds(matches_list)

        # Standardize tip names
        col_name = df_soccer.columns[ExportIDX.TIP1_NAME]
        df_soccer[col_name] = df_soccer[col_name].map(standardize_soccer_tip_name)
        col_name = df_soccer.columns[ExportIDX.TIP2_NAME]
        df_soccer[col_name] = df_soccer[col_name].map(standardize_soccer_tip_name)

        results[StandardNames.soccer] = df_soccer

        print_to_file(df_soccer.to_string(index=False), "maxb_soccer.txt")
        export_for_merge(df_soccer, "maxb_soccer.txt")

    print("--- %s seconds ---" % (time.time() - start_time))
    return results


# scrape()
