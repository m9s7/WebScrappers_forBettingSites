import datetime
import os
import time
import pandas as pd
from models.common_functions import print_to_file


def find_arb(sport_name, capital):
    _path = f"C:\\Users\\Matija\\PycharmProjects\\ScrapeEscape\\SportsBettingScrapers\\go_code\\dfs_for_export\\export_{sport_name}.txt"
    if os.path.isfile(_path) and os.path.getsize(_path) > 0:
        records = pd.read_csv(_path)
    else:
        return

    print("...finding arbitrage opportunities\n-------------------------")
    start_time = time.time()

    preprocessed_rec = records.astype(
        {'tip1_mozz': 'float', 'tip2_mozz': 'float', 'tip1_maxb': 'float', 'tip2_maxb': 'float'}).fillna(0.0)

    preprocessed_rec['tip1_MAX'] = preprocessed_rec[['tip1_mozz', 'tip1_maxb']].values.max(axis=1)
    preprocessed_rec['tip2_MAX'] = preprocessed_rec[['tip2_mozz', 'tip2_maxb']].values.max(axis=1)

    preprocessed_rec = preprocessed_rec[preprocessed_rec.tip1_MAX != 0]
    preprocessed_rec = preprocessed_rec[preprocessed_rec.tip2_MAX != 0]

    preprocessed_rec['%_bet1'] = preprocessed_rec['tip1_MAX'].apply(lambda x: 1 / x)
    preprocessed_rec['%_bet2'] = preprocessed_rec['tip2_MAX'].apply(lambda x: 1 / x)
    preprocessed_rec['outlay'] = preprocessed_rec['%_bet1'] + preprocessed_rec['%_bet2']

    results = preprocessed_rec.loc[preprocessed_rec['outlay'] < 1].copy(deep=True)
    if results.empty:
        print("No arbitrage opportunities\n")
        return

    print('OMG OMG is this real life\n')

    results['stake1'] = round(results['%_bet1'] * capital)
    results['stake2'] = round(results['%_bet2'] * capital)
    results['total_stake'] = round(results['stake1'] + results['stake2'])
    results['ROI'] = round(((capital / results['total_stake']) - 1) * 100, 2)

    results.drop(['%_bet1', '%_bet2'], axis=1)

    print("\n", results.to_string(index=False))
    print("--- %s seconds ---" % (time.time() - start_time))
    print_to_file(data=f'{datetime.datetime.now().timestamp()}\n', file="ARBITRAGE.txt", mode='a')
    print_to_file(data=results.to_string(index=False), file="ARBITRAGE.txt", mode='a')
    return results
