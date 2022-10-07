import pandas as pd
from thefuzz import fuzz

from maxbet_scraper import scrape as scrape_maxbet
from mozzart_scraper import scrape as scrape_mozzart

maxb = scrape_maxbet()
mozz = scrape_mozzart()

# Prvo se iterira po onoj kladionici koja ima najvise meceva, sortiras ih po len(kladza.index)
# tako su najmanje sanse da izgubim info neki a da se necimam maksimalno oko proveravanja
successful_matches = 0
records_to_keep = []
for i in maxb.to_dict('records'):
    merged_record = []
    for j in mozz.to_dict('records'):
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
print("maxb: ", len(maxb.index))
print("mozz: ", len(mozz.index))

columns = ['1', '2', 'KI_1_maxb', 'KI_1_mozz', 'KI_2_maxb', 'KI_2_mozz']
merged_records = pd.DataFrame(records_to_keep, columns=columns)

print(merged_records.to_string())

# TODO: Compare dataframe values to find arbitrage opportunities
# sad kad hoces da poredis uradis remove if none za record
