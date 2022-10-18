import pandas as pd
import time

from thefuzz import fuzz

from models.common_functions import print_to_file
from maxbet.scraper import scrape as scrape_maxbet
from mozzart.mozzart_scraper import scrape as scrape_mozzart


def merge_records(sport_name, maxbet, mozzart):
    start_time = time.time()
    print("... merging scraped data")

    # order books based by num of records
    bookies_ordered = {}
    if len(maxbet.index) > len(mozzart.index):
        bookie1 = maxbet
        bookie2 = mozzart
        bookies_ordered['1'] = "maxb"
        bookies_ordered['2'] = "mozz"
    else:
        bookie1 = mozzart
        bookie2 = maxbet
        bookies_ordered['1'] = "mozz"
        bookies_ordered['2'] = "maxb"

    columns = ['1', '2',
               'tip1', f'tip1_{bookies_ordered["1"]}', f'tip1_{bookies_ordered["2"]}',
               'tip2', f'tip2_{bookies_ordered["1"]}', f'tip2_{bookies_ordered["2"]}'
               ]

    # merge
    successful_matches = 0
    records_to_keep = []
    for i in bookie1.to_dict('records'):
        merged_record = []
        for j in bookie2.to_dict('records'):

            if sport_name == 'Fudbal':
                if i['tip1_name'] != j['tip1_name'] or i['tip2_name'] != j['tip2_name']:
                    continue

                fr11 = fuzz.ratio(i['1'], j['1'])
                if fr11 < 80:
                    continue

                fr22 = fuzz.ratio(i['2'], j['2'])
                if fr22 < 80:
                    continue

                merged_record = [i['1'], i['2'], i['tip1_name'], i['tip1_val'], j['tip1_val'], i['tip2_name'],
                                 i['tip2_val'], j['tip2_val']]
            else:
                "                          1                     2 tip1_name tip1_val tip2_name tip2_val"
                if fuzz.ratio(i['1'], j['1']) >= 80 and fuzz.ratio(i['2'], j['2']) >= 80:
                    # merge as is
                    merged_record = [i['1'], i['2'], i['tip1_name'], i['tip1_val'], j['tip1_val'], i['tip2_name'],
                                     i['tip2_val'], j['tip2_val']]
                elif fuzz.ratio(i['1'], j['2']) >= 80 and fuzz.ratio(i['2'], j['1']) >= 80:
                    # switch mozz record order
                    merged_record = [i['1'], i['2'], i['tip1_name'], i['tip1_val'], j['tip2_val'], i['tip2_name'],
                                     i['tip2_val'], j['tip1_val']]
                else:
                    continue

            successful_matches += 1

        # No point in doing this with only 2 bookies because you are just gonna remove None rows later
        if not merged_record:
            continue
            # merged_record = [i['1'], i['2'], i['tip1_name'], i['tip1_val'], None, i['tip2_name'], i['tip2_val'], None]

        records_to_keep.append(merged_record)

    print(f"{bookies_ordered['1']}: ", len(bookie1.index))
    print(f"{bookies_ordered['2']}: ", len(bookie2.index))
    print("Successfully merged: ", successful_matches, " records\n")

    merged_records = pd.DataFrame(records_to_keep, columns=columns)
    print_to_file(merged_records.to_string(), 'merged.txt')

    print("--- %s seconds ---" % (time.time() - start_time))
    return merged_records


def find_arb(records, capital):
    print("...finding arbitrage opportunities\n-------------------------")
    start_time = time.time()

    preprocessed_rec = records.astype(
        {'tip1_mozz': 'float', 'tip2_mozz': 'float', 'tip1_maxb': 'float', 'tip2_maxb': 'float'}).fillna(0.0)

    preprocessed_rec['tip1_MAX'] = preprocessed_rec[['tip1_mozz', 'tip1_maxb']].values.max(axis=1)
    preprocessed_rec['tip2_MAX'] = preprocessed_rec[['tip2_mozz', 'tip2_maxb']].values.max(axis=1)

    preprocessed_rec = preprocessed_rec[preprocessed_rec.tip1_MAX != 0]
    preprocessed_rec = preprocessed_rec[preprocessed_rec.tip2_MAX != 0]

    print_to_file(preprocessed_rec.to_string(), "result.txt")

    preprocessed_rec['%_bet1'] = preprocessed_rec['tip1_MAX'].apply(lambda x: 1 / x)
    preprocessed_rec['%_bet2'] = preprocessed_rec['tip2_MAX'].apply(lambda x: 1 / x)
    preprocessed_rec['outlay'] = preprocessed_rec['%_bet1'] + preprocessed_rec['%_bet2']

    # print(preprocessed_rec.to_string())

    results = preprocessed_rec.loc[preprocessed_rec['outlay'] < 1]
    if results.empty:
        print("No arbitrage opportunities\n")
        return

    print('OMG OMG is this real life\n')
    print("\n", results.to_string())

    results['stake1'] = results['%_bet1'] * capital
    results['stake2'] = results['%_bet2'] * capital
    results['total_stake'] = results['stake1'] + results['stake2']
    results['ROI'] = (capital / results['total_stake']) - 1

    print("--- %s seconds ---" % (time.time() - start_time))
    print_to_file(data=results.to_string(), file="ARBITRAGE.txt", mode='a')
    return results


# TODO: Write your own fuzzy matching, where
# - you split by '/' if its a pair in tennis and then you combine the two scores
# - value partial matching percentage wise, idk just make it better then what you got currently
# - or start a database which you fill with your scraping, and automatically have a que of moz_name - maxb_name y/n

# its scraping for everything where it should only scrape for sports that are offered in both
maxb = scrape_maxbet()
mozz = scrape_mozzart()

print(maxb.keys())
print(mozz.keys(), "\n")

for sport in set(maxb.keys()).intersection(mozz.keys()):
    print(sport)
    res = find_arb(merge_records(sport, maxb[sport], mozz[sport]), 1000)

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
# TODO: parallelize MERGING IN GO
# TODO: send emails if you find anything
# TODO: set it to run nonstop

# TODO: make debugging mode
# TODO: error checking

# TODO: retype whole project in Go language ?? why use python here, how to decide if slow speed is due to language
# but only do it after you have a minimum viable working product
