import time

import pandas as pd

from models.match_model import ExportIDX
from requests_to_server.maxbet_requests import get_match_data

# # Added:
# Ukupno golova 90'
# Ukupno golova prvo poluvreme
# Ukupno golova drugo poluvreme
# Domaćin golovi
# Domaćin golovi prvo poluvreme
# Domaćin golovi drugo poluvreme
# Gost golovi
# Gost golovi prvo poluvreme
# Gost golovi drugo poluvreme

# # Not yet added:
# Winner (ne ako je kvota 1)
# Winner prvo poluvreme
# Winner drugo poluvreme
# GG, NG


golovi_subgames = {
    "Ukupno golova 90'": {
        'prefix': 'ug ',
        'tip1_length': 6,
        'tip1_special': 'ug T0',
    },
    "Ukupno golova prvo poluvreme": {
        'prefix': 'ug 1P',
        'tip1_length': 8,
        'tip1_special': 'ug 1PT0',
    },
    "Ukupno golova drugo poluvreme": {
        'prefix': 'ug 2P',
        'tip1_length': 8,
        'tip1_special': 'ug 2PT0',
    },
    "Domaćin golovi": {
        'prefix': 'D',
        'tip1_length': 4,
        'tip1_special': 'D0',
    },
    "Domaćin golovi prvo poluvreme": {
        'prefix': '1D',
        'tip1_length': 5,
        'tip1_special': '1D0',
    },
    "Domaćin golovi drugo poluvreme": {
        'prefix': '2D',
        'tip1_length': 5,
        'tip1_special': '2D0',
    },
    "Gost golovi": {
        'prefix': 'G',
        'tip1_length': 4,
        'tip1_special': 'G0',
    },
    "Gost golovi prvo poluvreme": {
        'prefix': '1G',
        'tip1_length': 5,
        'tip1_special': '1G0',
    },
    "Gost golovi drugo poluvreme": {
        'prefix': '2G',
        'tip1_length': 5,
        'tip1_special': '2G0',
    }
}


def get_soccer_odds(match_ids):
    start_time = time.time()

    matches_scraped_counter = 0
    export = []
    for match_id in match_ids:

        match = get_match_data(match_id)
        matches_scraped_counter += 1
        e = [match['kickOffTime'], match['leagueName'], match['home'], match['away'], None, None, None, None]
        for subgame in match['odBetPickGroups']:

            if subgame['name'] not in golovi_subgames:
                continue

            s = golovi_subgames[subgame['name']]
            tips = [tip['name'] for tip in subgame['tipTypes']]

            # Process 0-x and x+ combinations
            for tip1 in tips:
                if len(tip1) != s['tip1_length'] or tip1.startswith(s['prefix'] + '0-') is False:
                    continue

                x = int(tip1[len(s['prefix']) + 2])

                tip2 = f'{s["prefix"]}{x + 1}+'
                if tip2 not in tips:
                    continue

                tip1_value = subgame['tipTypes'][tips.index(tip1)]['value']
                tip2_value = subgame['tipTypes'][tips.index(tip2)]['value']

                e[ExportIDX.TIP1_NAME] = tip1
                e[ExportIDX.TIP1_VAL] = tip1_value
                e[ExportIDX.TIP2_NAME] = tip2
                e[ExportIDX.TIP2_VAL] = tip2_value
                export.append(e[:])

            # Process T0 and 1+ combo
            tip1 = s['tip1_special']
            tip2 = s['prefix'] + '1+'
            if tip1 in tips:
                tip1_value = subgame['tipTypes'][tips.index(tip1)]['value']

                if tip1_value == 0 or tip2 not in tips:
                    continue
                tip2_value = subgame['tipTypes'][tips.index(tip2)]['value']

                e[ExportIDX.TIP1_NAME] = tip1
                e[ExportIDX.TIP1_VAL] = tip1_value
                e[ExportIDX.TIP2_NAME] = tip2
                e[ExportIDX.TIP2_VAL] = tip2_value
                export.append(e[:])

    columns = ['kick_off', 'league', '1', '2', 'tip1_name', 'tip1_val', 'tip2_name', 'tip2_val']
    df = pd.DataFrame(export, columns=columns)
    print("Matches scraped: ", matches_scraped_counter)
    print("--- %s seconds ---" % (time.time() - start_time))
    return df
