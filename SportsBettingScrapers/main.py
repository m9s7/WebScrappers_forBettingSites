import pandas as pd
from thefuzz import fuzz

from maxbet_scraper import scrape as scrape_maxbet
from models.common_functions import print_to_file
from mozzart_scraper import scrape as scrape_mozzart


def merge_records(maxbet, mozzart):
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
               f'KI_1_{bookies_ordered["1"]}', f'KI_1_{bookies_ordered["2"]}',
               f'KI_2_{bookies_ordered["1"]}', f'KI_2_{bookies_ordered["2"]}'
               ]

    # merge
    successful_matches = 0
    records_to_keep = []
    for i in bookie1.to_dict('records'):
        merged_record = []

        for j in bookie2.to_dict('records'):
            fr11 = fuzz.ratio(i['1'], j['1'])
            fr12 = fuzz.ratio(i['1'], j['2'])
            fr21 = fuzz.ratio(i['2'], j['1'])
            fr22 = fuzz.ratio(i['2'], j['2'])

            if fr11 >= 80 and fr22 >= 80:
                # merge as is
                merged_record = [i['1'], i['2'], i['KI_1'], j['KI_1'], i['KI_2'], j['KI_2']]
            elif fr12 >= 80 and fr21 >= 80:
                # switch mozz record order
                merged_record = [i['1'], i['2'], i['KI_1'], j['KI_2'], i['KI_2'], j['KI_1']]
            else:
                continue
            successful_matches += 1

        if not merged_record:
            merged_record = [i['1'], i['2'], i['KI_1'], None, i['KI_2'], None]

        # turn strings to numbers
        # print()

        records_to_keep.append(merged_record)

    print(f"{bookies_ordered['1']}: ", len(bookie1.index))
    print(f"{bookies_ordered['2']}: ", len(bookie2.index))
    print("Successfully merged: ", successful_matches, " records")

    merged_records = pd.DataFrame(records_to_keep, columns=columns)

    return merged_records


def find_arb(records):
    print("...finding arbitrage opportunities\n-------------------------")

    preprocessed_rec = records.astype(
        {'KI_1_maxb': 'float', 'KI_1_mozz': 'float', 'KI_2_maxb': 'float', 'KI_2_mozz': 'float'}).fillna(0.0)

    preprocessed_rec['KI_1_MAX'] = preprocessed_rec[['KI_1_mozz', 'KI_1_maxb']].values.max(1)
    preprocessed_rec['KI_2_MAX'] = preprocessed_rec[['KI_2_mozz', 'KI_2_maxb']].values.max(1)

    preprocessed_rec = preprocessed_rec[preprocessed_rec.KI_1_MAX != 0]
    preprocessed_rec = preprocessed_rec[preprocessed_rec.KI_2_MAX != 0]

    print_to_file(preprocessed_rec.to_string(), "result.txt")

    preprocessed_rec['outlay'] = preprocessed_rec['KI_1_MAX'].apply(lambda x: 100 / x) + preprocessed_rec[
        'KI_2_MAX'].apply(lambda x: 100 / x)

    if (preprocessed_rec.loc[preprocessed_rec['outlay'] <= 100.0]).empty:
        print("No arbitrage opportunities")
        return None
    else:
        print('OMG is this real life')
        return preprocessed_rec


maxb = scrape_maxbet()
mozz = scrape_mozzart()

merged = merge_records(maxb, mozz)

find_arb(merged)

# TODO: scrape more data
# Two-outcome Betting: tennis (DONE), baseball, and basketball (with extra time included)
# Three-outcome Betting: test cricket and soccer
# TODO: parallelize scraping
# TODO: send emails if you find anything
# TODO: set it to run nonstop
