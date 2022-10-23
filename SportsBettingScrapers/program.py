import time

from find_arb import find_arb
from maxbet.scraper import scrape as scrape_maxbet
from mozzart.mozzart_scraper import scrape as scrape_mozzart

import ctypes

from requests_to_server.telegram import broadcast_to_telegram


def program():
    start_time = time.time()

    library = ctypes.windll.LoadLibrary(
        r'C:\Users\Matija\PycharmProjects\ScrapeEscape\SportsBettingScrapers\go_code\merge_dfs.dll')
    merge = library.merge
    merge.argtypes = [ctypes.c_char_p]

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

    # TODO: its scraping for everything where it should only scrape for sports that are offered in both
    maxb = scrape_maxbet()
    mozz = scrape_mozzart()

    arbs = []
    for sport in set(maxb.keys()).intersection(mozz.keys()):
        arg = str(sport).encode("utf-8")
        merge(arg)
        res = find_arb(str(sport), 1000)
        if res is None:
            print("nema arbe ", sport, "\n")
        else:
            arbs.append(res)

    print("OVERALL EXECUTION TIME")
    print("--- %s seconds ---" % (time.time() - start_time))

    if len(arbs) != 0:
        broadcast_to_telegram("ALO LELEMUDI STIGLE FRISKE ARBE")
    else:
        broadcast_to_telegram("nema arbe :'(")

    for a in arbs:
        print(a)
