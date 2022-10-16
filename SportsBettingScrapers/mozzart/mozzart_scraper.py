from models.match_model import MozzNames

from mozzart.basketball.scraper import scrape_basketball
from mozzart.esports.scraper import scrape_esports
from mozzart.helper_functions import parse_sidebar
from mozzart.tennis.scraper import scrape_tennis

from requests_to_server.mozzart_requests import get_curr_sidebar_sports_and_leagues, get_all_subgames


def scrape():
    print("...scraping mozz")

    mozz_id_name_dict = parse_sidebar(get_curr_sidebar_sports_and_leagues().json())
    # TODO: add to debug mode
    # See which sports there are
    # print(mozz_id_name_dict)

    all_subgames_json = get_all_subgames().json()
    # Format:
    # all_subgames_json is a dict where keys are ordered integers [1..77]
    # and values are lists which contain subgame dictionaries

    # TODO: parallelize
    results = {
        MozzNames.tennis: scrape_tennis(mozz_id_name_dict[MozzNames.tennis], all_subgames_json),
        MozzNames.esports: scrape_esports(mozz_id_name_dict[MozzNames.esports], all_subgames_json),
        MozzNames.basketball: scrape_basketball(mozz_id_name_dict[MozzNames.basketball], all_subgames_json)
    }

    return results


# scrape()
