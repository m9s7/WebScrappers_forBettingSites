import time

from models.common_functions import print_to_file, export_for_merge
from models.match_model import MozzNames, StandardNames

from mozzart.scrape.odds_parsers.basketball_odds_parser import scrape_basketball
from mozzart.scrape.odds_parsers.esports_odds_parser import scrape_esports
from mozzart.scrape.odds_parsers.soccer_odds_parser import scrape_soccer
from mozzart.scrape.odds_parsers.tennis_odds_parser import scrape_tennis

from requests_to_server.mozzart_requests import get_curr_sidebar_sports_and_leagues, get_all_subgames


def parse_sidebar(sidebar_response):
    name_id_dict = {}
    for sport in sidebar_response:
        name_id_dict[sport['name']] = sport['id']

    return name_id_dict


def get_sports_currently_offered():
    response = get_curr_sidebar_sports_and_leagues()
    sports = [sport['name'] for sport in response]
    return sports


def scrape(sports_to_scrape):
    start_time = time.time()
    print("...scraping mozz")

    name_id_dict = parse_sidebar(get_curr_sidebar_sports_and_leagues())
    all_subgames_json = get_all_subgames()

    results = {}

    for sport in sports_to_scrape:
        df = None
        if sport == MozzNames.tennis:
            df = scrape_tennis(name_id_dict[MozzNames.tennis], all_subgames_json)
        if sport == MozzNames.esports:
            df = scrape_esports(name_id_dict[MozzNames.esports], all_subgames_json)
        if sport == MozzNames.basketball:
            df = scrape_basketball(name_id_dict[MozzNames.basketball], all_subgames_json)
        if sport == MozzNames.soccer:
            df = scrape_soccer(name_id_dict[MozzNames.soccer], all_subgames_json)

        print_to_file(df.to_string(index=False), f"mozz_{str(sport.toStandardName())}.txt")
        export_for_merge(df, f"mozz_{str(sport.toStandardName())}.txt")
        results[sport.toStandardName()] = df

    print("--- %s seconds ---" % (time.time() - start_time))
    return results


# scrape()
