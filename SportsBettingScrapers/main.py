import pandas as pd
from thefuzz import fuzz

from maxbet_scraper import scrape as scrape_maxbet
from mozzart_scraper import scrape as scrape_mozzart


def merge_records(maxbet, mozzart):
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

        records_to_keep.append(merged_record)

    print('--------------------')
    print(successful_matches)
    print(f"{bookies_ordered['1']}: ", len(bookie1.index))
    print(f"{bookies_ordered['2']}: ", len(bookie2.index))

    merged_records = pd.DataFrame(records_to_keep, columns=columns)

    return merged_records


maxb = scrape_maxbet()
mozz = scrape_mozzart()

merged = merge_records(maxb, mozz)
print(merged.to_string())

# TODO: Compare dataframe values to find arbitrage opportunities
# sad kad hoces da poredis uradis remove if none za record
