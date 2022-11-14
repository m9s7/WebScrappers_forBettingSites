import time

from common.common_functions import print_to_file, export_for_merge
from common.models import StandardNames, SoccbetNames, ExportIDX
from requests_to_server.soccerbet_requests import get_master_data
from bookies.soccerbet.scrape.odds_parsers.basketball_odds_parser import basketball_odds_parser
from bookies.soccerbet.scrape.odds_parsers.tabletennis_odds_parser import tabletennis_odds_parser
from bookies.soccerbet.scrape.odds_parsers.tennis_odds_parser import tennis_odds_parser
from bookies.soccerbet.scrape.odds_parsers.soccer_odds_parser import soccer_odds_parser

from bookies.soccerbet.scrape.parse_response_functions import get_sport_dict, create_sidebar, get_betgame_dict, \
    get_betgame_outcome_dict, get_betgame_groups_dict
from bookies.soccerbet.standardize.standardization_functions import standardize_kickoff_time_string, \
    get_standardization_func_4_tip_names


def get_sports_currently_offered():
    master_data = None
    while master_data is None:
        print("Stuck on soccerbet, get_master_data()")
        master_data = get_master_data()

    sport_dict = get_sport_dict(master_data)  # key = id, val = name, all sports
    sidebar = create_sidebar(master_data, sport_dict)  # key = sport name, val = list of leagues, available sports

    return sidebar.keys()


def scrape(sports_to_scrape):
    print("scrapping soccerbet... ")
    start_time = time.time()

    master_data = None
    while master_data is None:
        print("Stuck on soccerbet, get_master_data()")
        master_data = get_master_data()

    sport_dict = get_sport_dict(master_data)
    betgame_dict = get_betgame_dict(master_data)
    betgame_outcome_dict = get_betgame_outcome_dict(master_data)
    betgame_groups_dict = get_betgame_groups_dict(master_data)

    sidebar = create_sidebar(master_data, sport_dict)

    for sport in sports_to_scrape:

        try:
            sidebar[sport]
        except KeyError:
            print(sport, " not currently offered at soccerbet")
            continue

        df = None
        if sport == SoccbetNames.tennis:
            df = tennis_odds_parser(sidebar[sport], betgame_dict, betgame_outcome_dict,
                                    betgame_groups_dict)
        # TODO: add esports when they offer it in soccbet
        # if sport == SoccbetNames.esports:
        #     df = esports_odds_parser(sidebar[sport], betgame_dict, betgame_outcome_dict,
        #                              betgame_groups_dict)
        if sport == SoccbetNames.tabletennis:
            df = tabletennis_odds_parser(sidebar[sport], betgame_dict, betgame_outcome_dict,
                                         betgame_groups_dict)
        if sport == SoccbetNames.basketball:
            df = basketball_odds_parser(sidebar[sport], betgame_dict, betgame_outcome_dict,
                                        betgame_groups_dict)
        if sport == SoccbetNames.soccer:
            df = soccer_odds_parser(sidebar[sport], betgame_dict, betgame_outcome_dict,
                                    betgame_groups_dict)

        standardize_tip_name = get_standardization_func_4_tip_names(sport)
        col_name = df.columns[ExportIDX.KICKOFF]
        df[col_name] = df[col_name].map(standardize_kickoff_time_string)
        col_name = df.columns[ExportIDX.TIP1_NAME]
        df[col_name] = df[col_name].map(standardize_tip_name)
        col_name = df.columns[ExportIDX.TIP2_NAME]
        df[col_name] = df[col_name].map(standardize_tip_name)

        print_to_file(df.to_string(index=False), f"soccbet_{str(sport.toStandardName())}.txt")
        export_for_merge(df, f"soccbet_{str(sport.toStandardName())}.txt")

    print("OVERALL EXECUTION TIME")
    print("--- %s seconds ---" % (time.time() - start_time))

# esports
# scrape([StandardNames(s).toSoccbetName() for s in ['basketball', 'soccer', 'tennis', 'table_tennis']])
