import time

import pandas as pd

from common.models import scraper_columns
from requests_to_server.soccerbet_requests import get_league_matches_info, get_match_odd_values
from bookies.soccerbet.scrape.parse_response_functions import parse_get_league_matches_info


def soccer_odds_parser(leagues_from_sidebar, betgame_dict, betgame_outcome_dict, betgame_groups_dict):
    print("...scraping soccerbet - soccer")
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

            tip1 = {}
            tip2 = {}
            for odds in match_odds:
                if not odds['IsEnabled']:
                    continue

                outcome = betgame_outcome_dict[odds['BetGameOutcomeId']]
                betgame = betgame_dict[outcome['BetGameId']]
                betgame_group = betgame_groups_dict[betgame['BetGameGroupId']]
                tip_value = odds['Odds']

                # GG/NG
                if betgame_group['Name'] == 'OBA TIMA DAJU GOL' and betgame['Name'] == 'Oba Tima Daju Gol':
                    tip_key = (betgame['Name'], outcome['Name'], outcome['CodeForPrinting'])
                    if outcome['Name'] == 'GG':
                        tip1[tip_key] = tip_value
                    if outcome['Name'] == 'NG':
                        tip2[tip_key] = tip_value
                    continue

                # UKUPNO GOLOVA
                if betgame_group['Name'] not in ['UKUPNO GOLOVA', 'DOMAĆIN UK. GOLOVA', 'GOST UK. GOLOVA']:
                    continue
                if (betgame['Name'] in ['Ukupno Golova', 'I Pol. Uk. Golova', 'II Pol. Uk. Golova',
                                        'Domaćin Ukupno Golova', 'I Pol. Domaćin Uk. Golova',
                                        'II Pol. Domaćin Uk. Golova',
                                        'Gost Ukupno Golova', 'I Pol. Gost Uk. Golova', 'II Pol. Gost Uk. Golova']):

                    tip_key = (betgame['Name'], outcome['Name'], outcome['CodeForPrinting'])
                    if outcome['Name'].startswith('0-') or outcome['Name'] == '0':
                        tip1[tip_key] = tip_value
                    if outcome['Name'].endswith('+'):
                        tip2[tip_key] = tip_value

            for t1_game, t1_subgame, t1_code in tip1:
                if t1_subgame == '0':
                    for t2_game, t2_subgame, t2_code in tip2:
                        if t2_game == t1_game and t2_subgame == '1+':
                            e = e1 + [t1_code, tip1[t1_game, t1_subgame, t1_code],
                                      t2_code, tip2[t2_game, t2_subgame, t2_code]]
                            export.append(e)
                            matched_scraped_counter += 1

                if t1_subgame.startswith('0-') and len(t1_subgame) == 3:
                    x = int(t1_subgame[2])
                    for t2_game, t2_subgame, t2_code in tip2:
                        if t2_game == t1_game and t2_subgame == f'{x + 1}+':
                            e = e1 + [t1_code, tip1[t1_game, t1_subgame, t1_code],
                                      t2_code, tip2[t2_game, t2_subgame, t2_code]]
                            export.append(e)
                            matched_scraped_counter += 1

    df = pd.DataFrame(export, columns=scraper_columns)
    print("\nMatches scraped: ", matched_scraped_counter)
    print("--- %s seconds ---" % (time.time() - start_time))
    return df
