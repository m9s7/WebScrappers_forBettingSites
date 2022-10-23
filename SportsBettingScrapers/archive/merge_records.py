import time

import pandas as pd
from thefuzz import fuzz

from models.common_functions import print_to_file


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
