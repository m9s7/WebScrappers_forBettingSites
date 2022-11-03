import time

from maxbet.scrape.maxbet_scraper import scrape as scrape_maxbet
from mozzart.scrape.mozzart_scraper import scrape as scrape_mozzart


def program():
    start_time = time.time()

    # library = ctypes.windll.LoadLibrary(
    #     r'C:\Users\Matija\PycharmProjects\ScrapeEscape\SportsBettingScrapers\go_code\merge_dfs.dll')
    # merge = library.merge
    # merge.argtypes = [ctypes.c_char_p]

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

    # - standardize these general 2outcome tip_names based on sport (preslikavanje napravi u jednom folderu, standardizeed_tip_names_maxb...)
    # - - not here, not like this, make standardization module, this is the scraping module
    # - - napravi neko preslikavanje maxbet_tip -> universal_tip, tip description

    # TODO: parallelize scraping
    # TODO: set it to run nonstop and trigger go part when its done

    # TODO: make debugging mode
    # TODO: error checking

    # TODO: its scraping for everything where it should only scrape for sports that are offered in both

    # TODO: osmisli kako da se neradi fuzzy matching 10 puta ako ima 0-1 i 2+ pa 0-2 i 3+
    # mozda u mainu da se napravi set parova pa da se dodeljuje match id tako

    maxb = scrape_maxbet()  # pass in a list of sports
    mozz = scrape_mozzart()

    # arbs = []
    # for sport in set(maxb.keys()).intersection(mozz.keys()):
    #     arg = str(sport).encode("utf-8")
    #     merge(arg)
    #     res = find_arb(str(sport), 1000)
    #     if res is None:
    #         print("nema arbe ", sport, "\n")
    #     else:
    #         arbs.append(res)
    #
    # print("OVERALL EXECUTION TIME")
    # print("--- %s seconds ---" % (time.time() - start_time))
    #
    # if len(arbs) != 0:
    #     broadcast_to_telegram("ALO LELEMUDI STIGLE FRISKE ARBE")
    # else:
    #     broadcast_to_telegram("nema arbe :'(")
    #
    # print('wha')
    # for a in arbs:
    #     print(a.to_string())
