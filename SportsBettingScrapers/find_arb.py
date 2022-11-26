import os
import time
import pandas as pd
from common.common_functions import print_to_file


def find_arb(sport_name, capital):
    _path = f"C:\\Users\\Matija\\PycharmProjects\\ScrapeEscape\\SportsBettingScrapers\\go_code\\dfs_for_export\\export_{sport_name}.txt"
    if os.path.isfile(_path) and os.path.getsize(_path) > 0:
        records = pd.read_csv(_path)
    else:
        return None

    print("...finding arbitrage opportunities\n-------------------------")
    start_time = time.time()

    # Fill NaN values
    for col in records:
        if records[col].dtype == "float64":
            records[col] = records[col].fillna(0.0)

    # Get best odds
    tip1_cols = [col for col in records if col.startswith('tip1_')]
    records['tip1_MAX'] = records[tip1_cols].values.max(axis=1)
    tip2_cols = [col for col in records if col.startswith('tip2_')]
    records['tip2_MAX'] = records[tip2_cols].values.max(axis=1)

    # Remove zero tips
    records = records[records.tip1_MAX != 0]
    records = records[records.tip2_MAX != 0]

    # Calculate outlay
    records['%_bet1'] = records['tip1_MAX'].apply(lambda x: 1 / x)
    records['%_bet2'] = records['tip2_MAX'].apply(lambda x: 1 / x)
    records['outlay'] = records['%_bet1'] + records['%_bet2']

    # Keep records where outlay is < 1
    results = records.loc[records['outlay'] < 1].copy(deep=True)
    if results.empty:
        return None

    # results['stake1'] = round(results['%_bet1'] * capital)
    # results['stake2'] = round(results['%_bet2'] * capital)
    # results['total_stake'] = round(results['stake1'] + results['stake2'])
    results['%_bet1_scaled'] = (records['%_bet1'] / records['outlay']) * 100
    results['%_bet2_scaled'] = (records['%_bet2'] / records['outlay']) * 100

    results['ROI'] = round(((1 / results['outlay']) - 1) * 100, 2)

    # results = results.drop(['%_bet1', '%_bet2'], axis=1)

    print_to_file(results.to_string(index=False), f"arbs_{sport_name}.txt")
    print("--- %s seconds ---" % (time.time() - start_time))
    return results
