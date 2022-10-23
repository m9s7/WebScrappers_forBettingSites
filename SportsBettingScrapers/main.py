import datetime
import os
import time
import pandas as pd

from maxbet.scraper import scrape as scrape_maxbet
from models.common_functions import print_to_file
from mozzart.mozzart_scraper import scrape as scrape_mozzart

import ctypes

library = ctypes.windll.LoadLibrary(
    r'C:\Users\Matija\PycharmProjects\ScrapeEscape\SportsBettingScrapers\go_code\merge_dfs.dll')
merge = library.merge
merge.argtypes = [ctypes.c_char_p]

# TODO: its scraping for everything where it should only scrape for sports that are offered in both
maxb = scrape_maxbet()
mozz = scrape_mozzart()

print(list(maxb.keys()))
print(list(mozz.keys()), "\n")


# TODO: scrape more data
# Two-outcome Betting:
# - (DONE) tennis
# - cricket
# - baseball
# - (DONE) basketball with extra time included
# - (DONE) E-Sport
# - Football 0-3, 4+ (trazis ug 0-x i ako nadjes onda trazis ug (x+1)+), sve to isto za prvo/drugo poluvreme, 90', tim1/tim2, tim1-prvoPV kombinacije
# - Hokej pobednik meca ukljucujuci produzetke i penale
# Three-outcome Betting: test cricket and soccer
# The I gotta throw myself at handicaps, think of a system because there are is a million of options for them
# Winner = tie, kvota 1.0, mozda nije lose igrati i to


# TODO: parallelize scraping
# TODO: set it to run nonstop and trigger go part when its done

# TODO: make debugging mode
# TODO: error checking


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


for sport in set(maxb.keys()).intersection(mozz.keys()):
    arg = str(sport).encode("utf-8")
    merge(arg)
    find_arb(str(sport), 1000)

# arg = sport.encode("utf-8")
# merge(arg)
# find_arb(merge_records(sport, maxb[sport], mozz[sport]), 1000)

# print(str(StandardNames.tennis))
