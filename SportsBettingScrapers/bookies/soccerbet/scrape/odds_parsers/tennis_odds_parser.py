import time

import pandas as pd

from common.models import scraper_columns
from requests_to_server.soccerbet_requests import get_league_matches_info, get_match_odd_values
from bookies.soccerbet.scrape.common_functions import raise_not_2_outcome_game_error
from bookies.soccerbet.scrape.parse_response_functions import parse_get_league_matches_info


def tennis_odds_parser(leagues_from_sidebar, betgame_dict, betgame_outcome_dict, betgame_groups_dict):
    print("...scraping soccerbet - tennis")
    start_time = time.time()

    matched_scraped_counter = 0
    export = []
    for league in leagues_from_sidebar:

        response = get_league_matches_info(league['Id'])
        if response is None:
            print(f"Soccerbet league {league['Id']}, get_league_matches_info() is None, skipping it..")
        match_info_list = parse_get_league_matches_info(response)

        for match in match_info_list:
            e1 = [match['kickoff'], league['Name'], match['home'], match['away']]

            match_odds = get_match_odd_values(match['match_id'])
            if match_odds is None:
                continue

            export_match_helper = {}
            for odds in match_odds:
                if not odds['IsEnabled']:
                    continue

                outcome = betgame_outcome_dict[odds['BetGameOutcomeId']]
                betgame = betgame_dict[outcome['BetGameId']]
                betgame_group = betgame_groups_dict[betgame['BetGameGroupId']]
                tip_value = odds['Odds']

                game = betgame_group['Name'] + ' ' + betgame['Name']
                # nemaju TB prvi/drugi set, sranje

                # Konačni Ishod
                if betgame_group['Name'] == 'MEČ' and betgame['Name'] == 'Konačni Ishod':
                    if game not in export_match_helper:
                        export_match_helper[game] = [None, None, None, None]

                    if outcome['Name'] == '1':
                        export_match_helper[game][0] = outcome['CodeForPrinting']
                        export_match_helper[game][1] = tip_value
                    elif outcome['Name'] == '2':
                        export_match_helper[game][2] = outcome['CodeForPrinting']
                        export_match_helper[game][3] = tip_value
                    else:
                        raise_not_2_outcome_game_error(game, outcome['Name'], outcome['Description'],
                                                       outcome['CodeForPrinting'], tip_value)

                # Konačni Ishod Prvi Set
                if betgame_group['Name'] == 'SET' and betgame['Name'] == 'I Set':
                    if game not in export_match_helper:
                        export_match_helper[game] = [None, None, None, None]

                    if outcome['Name'] == '1':
                        export_match_helper[game][0] = outcome['CodeForPrinting']
                        export_match_helper[game][1] = tip_value
                    elif outcome['Name'] == '2':
                        export_match_helper[game][2] = outcome['CodeForPrinting']
                        export_match_helper[game][3] = tip_value
                    else:
                        raise_not_2_outcome_game_error(game, outcome['Name'], outcome['Description'],
                                                       outcome['CodeForPrinting'], tip_value)

                # Tie Break
                if betgame_group['Name'] == 'MEČ' and betgame['Name'] == 'Tie Break':
                    if game not in export_match_helper:
                        export_match_helper[game] = [None, None, None, None]

                    if outcome['Name'] == 'DA':
                        export_match_helper[game][0] = outcome['CodeForPrinting']
                        export_match_helper[game][1] = tip_value
                    elif outcome['Name'] == 'NE':
                        export_match_helper[game][2] = outcome['CodeForPrinting']
                        export_match_helper[game][3] = tip_value
                    else:
                        raise_not_2_outcome_game_error(game, outcome['Name'], outcome['Description'],
                                                       outcome['CodeForPrinting'], tip_value)

            for e2 in export_match_helper.values():
                export.append(e1 + e2)
                matched_scraped_counter += 1

    df = pd.DataFrame(export, columns=scraper_columns)
    print("\nMatches scraped: ", matched_scraped_counter)
    print("--- %s seconds ---" % (time.time() - start_time))
    return df
