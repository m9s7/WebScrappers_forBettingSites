import time

from models.common_functions import print_to_file, export_for_merge
from models.match_model import MozzNames, StandardNames

from mozzart.basketball.scraper import scrape_basketball
from mozzart.esports.scraper import scrape_esports
from mozzart.helper_functions import parse_sidebar
from mozzart.soccer.scraper import scrape_soccer
from mozzart.tennis.scraper import scrape_tennis

from requests_to_server.mozzart_requests import get_curr_sidebar_sports_and_leagues, get_all_subgames


# TODO: Mozzart cookies are fucked

def scrape():
    start_time = time.time()
    print("...scraping mozz")

    mozz_id_name_dict = parse_sidebar(get_curr_sidebar_sports_and_leagues().json())
    # TODO: add to debug mode
    # See which sports there are
    # print(mozz_id_name_dict)

    all_subgames_json = get_all_subgames().json()
    # Format:
    # all_subgames_json is a dict where keys are ordered integers [1..77]
    # and values are lists which contain subgame dictionaries

    # TODO: parallelize.
    results = {}

    if MozzNames.tennis in mozz_id_name_dict:
        tennis = scrape_tennis(mozz_id_name_dict[MozzNames.tennis], all_subgames_json)
        print_to_file(tennis.to_string(), f"mozz_tennis.txt")
        export_for_merge(tennis, "mozz_tennis.txt")
        results[StandardNames.tennis] = tennis

    if MozzNames.esports in mozz_id_name_dict:
        esports = scrape_esports(mozz_id_name_dict[MozzNames.esports], all_subgames_json)
        print_to_file(esports.to_string(), f"mozz_esports.txt")
        export_for_merge(esports, "mozz_esports.txt")
        results[StandardNames.esports] = esports

    if MozzNames.basketball in mozz_id_name_dict:
        basketball = scrape_basketball(mozz_id_name_dict[MozzNames.basketball], all_subgames_json)
        print_to_file(basketball.to_string(), f"mozz_basketball.txt")
        export_for_merge(basketball, "mozz_basketball.txt")
        results[StandardNames.basketball] = basketball

    if MozzNames.soccer in mozz_id_name_dict:
        soccer = scrape_soccer(mozz_id_name_dict[MozzNames.soccer], all_subgames_json)
        print_to_file(soccer.to_string(), f"mozz_soccer.txt")
        export_for_merge(soccer, "mozz_soccer.txt")
        results[StandardNames.soccer] = soccer

    print("--- %s seconds ---" % (time.time() - start_time))
    return results

# scrape()
