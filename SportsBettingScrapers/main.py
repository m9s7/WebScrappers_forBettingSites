import pandas as pd
from thefuzz import fuzz


from models.common_functions import print_to_file
from maxbet.scraper import scrape as scrape_maxbet
from mozzart.mozzart_scraper import scrape as scrape_mozzart


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

        # turn strings to numbers
        # print()

        records_to_keep.append(merged_record)

    print(f"{bookies_ordered['1']}: ", len(bookie1.index))
    print(f"{bookies_ordered['2']}: ", len(bookie2.index))
    print("... merging scraped data")
    print("Successfully merged: ", successful_matches, " records\n")

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

    preprocessed_rec['%_bet1'] = preprocessed_rec['KI_1_MAX'].apply(lambda x: 100 / x)
    preprocessed_rec['%_bet2'] = preprocessed_rec['KI_2_MAX'].apply(lambda x: 100 / x)
    preprocessed_rec['outlay'] = preprocessed_rec['%_bet1'] + preprocessed_rec['%_bet2']

    # print(preprocessed_rec.to_string())

    results = preprocessed_rec.loc[preprocessed_rec['outlay'] <= 100.0]
    if results.empty:
        print("No arbitrage opportunities\n")
    else:
        print('OMG OMG is this real life\n')
        print("\n", results.to_string())
        print_to_file(data=results.to_string(), file="ARBITRAGE.txt", mode='a')


def process_arb_opportunities(a, capital):
    a['stake1'] = a['%_bet1'] * capital
    a['stake2'] = a['%_bet2'] * capital

    # not like this, but w8 till you find arb opportunity to test it
    a['ROI'] = (100.0 / a['outlay']) - 1

    print(a)


# TODO: Write your own fuzzy matching, where
# - you split by '/' if its a pair in tennis and then you combine the two scores
# - value partial matching percentage wise, idk just make it better then what you got currently
# - or start a database which you fill with your scraping, and automatically have a que of moz_name - maxb_name y/n

# its scraping for everything where it should only scrape for sports that are offered in both
maxb = scrape_maxbet()
mozz = scrape_mozzart()

# print(maxb.keys())
# print(mozz.keys(), "\n")

print('\n\n')
for sport in set(maxb.keys()).intersection(mozz.keys()):
    find_arb(merge_records(maxb[sport], mozz[sport]))

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
# TODO: send emails if you find anything
# TODO: set it to run nonstop

# TODO: retype whole project in Go language ?? why use python here, how to decide if slow speed is due to language
# but only do it after you have a minimum viable working product
