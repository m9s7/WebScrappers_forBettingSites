import time

from common.common_functions import print_to_file, export_for_merge, box_print
from common.models import MozzNames, ExportIDX

from bookies.mozzart.scrape.odds_parsers.basketball_odds_parser import scrape_basketball
from bookies.mozzart.scrape.odds_parsers.esports_odds_parser import scrape_esports
from bookies.mozzart.scrape.odds_parsers.soccer_odds_parser import scrape_soccer
from bookies.mozzart.scrape.odds_parsers.tabletennis_odds_parser import scrape_tabletennis
from bookies.mozzart.scrape.odds_parsers.tennis_odds_parser import scrape_tennis
from bookies.mozzart.standardize.standardization_functions import standardize_kickoff_time_string, \
    get_standardization_func_4_tip_names

from requests_to_server.mozzart_requests import get_curr_sidebar_sports_and_leagues, get_all_subgames


def parse_sidebar(sidebar_response):
    name_id_dict = {}
    for sport in sidebar_response:
        name_id_dict[sport['name']] = sport['id']

    return name_id_dict


def get_sports_currently_offered():
    response = get_curr_sidebar_sports_and_leagues()
    while response is None:
        print('Stuck on getting mozz sidebar info')
        response = get_curr_sidebar_sports_and_leagues()
    sports = [sport['name'] for sport in response]
    return sports


def scrape(sports_to_scrape):
    start_time = time.time()
    # box_print("scraping mozz")

    response = get_curr_sidebar_sports_and_leagues()
    while response is None:
        print('Stuck on getting mozz sidebar info')
        response = get_curr_sidebar_sports_and_leagues()

    name_id_dict = parse_sidebar(response)

    all_subgames_json = get_all_subgames()
    while all_subgames_json is None:
        all_subgames_json = get_all_subgames()

    for sport in sports_to_scrape:

        try:
            name_id_dict[sport]
        except KeyError:
            print(sport, " not currently offered at mozzart")
            continue

        df = None
        if sport == MozzNames.tennis:
            df = scrape_tennis(name_id_dict[MozzNames.tennis], all_subgames_json)
        if sport == MozzNames.esports:
            df = scrape_esports(name_id_dict[MozzNames.esports], all_subgames_json)
        if sport == MozzNames.basketball:
            df = scrape_basketball(name_id_dict[MozzNames.basketball], all_subgames_json)
        if sport == MozzNames.soccer:
            df = scrape_soccer(name_id_dict[MozzNames.soccer], all_subgames_json)
        if sport == MozzNames.tabletennis:
            df = scrape_tabletennis(name_id_dict[MozzNames.tabletennis], all_subgames_json)

        standardize_tip_name = get_standardization_func_4_tip_names(sport)
        col_name = df.columns[ExportIDX.KICKOFF]
        df[col_name] = df[col_name].map(standardize_kickoff_time_string)
        col_name = df.columns[ExportIDX.TIP1_NAME]
        df[col_name] = df[col_name].map(standardize_tip_name)
        col_name = df.columns[ExportIDX.TIP2_NAME]
        df[col_name] = df[col_name].map(standardize_tip_name)

        print_to_file(df.to_string(index=False), f"mozz_{str(sport.toStandardName())}.txt")
        export_for_merge(df, f"mozz_{str(sport.toStandardName())}.txt")

    print("--- %s seconds ---" % (time.time() - start_time))


# scrape([StandardNames(s).toMozzName() for s in StandardNames])
