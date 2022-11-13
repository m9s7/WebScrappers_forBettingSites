import time

from models.match_model import StandardNames, SoccbetNames
from requests_to_server.soccerbet_requests import get_master_data
from soccerbet.odds_parsers.basketball_odds_parser import basketball_odds_parser
from soccerbet.odds_parsers.tennis_odds_parser import tennis_odds_parser
from soccerbet.odds_parsers.soccer_odds_parser import soccer_odds_parser

from soccerbet.scrape.parse_response_functions import get_sport_dict, create_sidebar, get_betgame_dict, \
    get_betgame_outcome_dict, get_betgame_groups_dict


def get_sports_currently_offered():
    master_data = get_master_data()
    sport_dict = get_sport_dict(master_data)
    sidebar = create_sidebar(master_data, sport_dict)

    return [sport_dict[k] for k in sidebar]


def scrape(sports_to_scrape):
    print("scrapping soccerbet... ")
    start_time = time.time()

    master_data = get_master_data()

    sport_dict = get_sport_dict(master_data)
    betgame_dict = get_betgame_dict(master_data)
    betgame_outcome_dict = get_betgame_outcome_dict(master_data)
    betgame_groups_dict = get_betgame_groups_dict(master_data)

    sidebar = create_sidebar(master_data, sport_dict)

    basketball_odds_parser(sidebar[SoccbetNames.basketball], betgame_dict, betgame_outcome_dict, betgame_groups_dict)
    tennis_odds_parser(sidebar[SoccbetNames.tennis], betgame_dict, betgame_outcome_dict, betgame_groups_dict)
    soccer_odds_parser(sidebar[SoccbetNames.soccer], betgame_dict, betgame_outcome_dict, betgame_groups_dict)

    print("OVERALL EXECUTION TIME")
    print("--- %s seconds ---" % (time.time() - start_time))


scrape([StandardNames(s).toSoccbetName() for s in ['basketball', 'soccer', 'table_tennis', 'tennis', 'esports']])
