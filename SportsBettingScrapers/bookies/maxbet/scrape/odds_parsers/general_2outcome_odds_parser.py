import time

import pandas as pd

from common.models import ExportIDX, scraper_columns
from requests_to_server.maxbet_requests import get_match_data


def get_2outcome_odds(match_ids, subgame_names):
    start_time = time.time()

    matches_scraped_counter = 0
    export = []
    for match_id in match_ids:

        match = get_match_data(match_id)
        if match is None:
            continue
        matches_scraped_counter += 1
        e = [match['kickOffTime'], match['leagueName'], match['home'], match['away'], None, None, None, None]
        for subgame in match['odBetPickGroups']:

            if (
                    subgame['name'] not in subgame_names or
                    len(subgame['tipTypes']) != 2 or
                    (subgame['tipTypes'][0]['value'] == 0 and subgame['tipTypes'][1]['value'] == 0)
            ):
                continue

            e[ExportIDX.TIP1_NAME] = subgame['tipTypes'][0]['tipType']
            e[ExportIDX.TIP1_VAL] = subgame['tipTypes'][0]['value']
            e[ExportIDX.TIP2_NAME] = subgame['tipTypes'][1]['tipType']
            e[ExportIDX.TIP2_VAL] = subgame['tipTypes'][1]['value']
            export.append(e[:])

    df = pd.DataFrame(export, columns=scraper_columns)
    print("\nMatches scraped: ", matches_scraped_counter)
    print("--- %s seconds ---" % (time.time() - start_time))
    return df
