import ctypes
import time

from maxbet.scrape.maxbet_scraper import scrape as scrape_maxbet
from maxbet.scrape.maxbet_scraper import get_sports_currently_offered as get_sports_currently_offered_maxb
from models.match_model import StandardNames, MaxbNames, MozzNames
from mozzart.scrape.mozzart_scraper import scrape as scrape_mozzart
from mozzart.scrape.mozzart_scraper import get_sports_currently_offered as get_sports_currently_offered_mozz


def get_sports_to_scrape():
    sports_im_interested_in = {
        StandardNames.tennis,
        # StandardNames.basketball,
        # StandardNames.esports,
        # StandardNames.soccer,
        # StandardNames.tabletennis
    }
    maxb_available_sports = set(
        [MaxbNames.fromString(s).toStandardName() for s in get_sports_currently_offered_maxb() if
         MaxbNames.fromString(s) is not None])
    mozz_available_sports = set(
        [MozzNames.fromString(s).toStandardName() for s in get_sports_currently_offered_mozz() if
         MozzNames.fromString(s) is not None])

    sports_to_scrape = list(
        sports_im_interested_in.intersection(
            maxb_available_sports.intersection(mozz_available_sports)
        )
    )

    print("Sports I'm interested in: ", sports_im_interested_in)
    print("Maxbet sports available: ", maxb_available_sports)
    print("Mozzart sports available: ", mozz_available_sports)

    print("Sports that will be scraped: ", [str(s) for s in sports_to_scrape])

    return sports_to_scrape


def program():
    start_time = time.time()

    library = ctypes.windll.LoadLibrary(
        r'C:\Users\Matija\PycharmProjects\ScrapeEscape\SportsBettingScrapers\go_code\merge_dfs.dll')
    merge = library.merge
    merge.argtypes = [ctypes.c_char_p]

    # TODO: scrape more data
    # TODO: parallelize scraping

    sports_to_scrape = get_sports_to_scrape()

    maxb = scrape_maxbet([s.toMaxbName() for s in sports_to_scrape])
    mozz = scrape_mozzart([s.toMozzName() for s in sports_to_scrape])

    # arbs = []
    for sport in sports_to_scrape:
        arg = str(sport).encode("utf-8")
        merge(arg)
    #     res = find_arb(str(sport), 1000)
    #     if res is None:
    #         print("nema arbe ", sport, "\n")
    #     else:
    #         arbs.append(res)
    #
    #
    # if len(arbs) != 0:
    #     broadcast_to_telegram("ALO LELEMUDI STIGLE FRISKE ARBE")
    # else:
    #     broadcast_to_telegram("nema arbe :'(")
    #
    # print('wha')
    # for a in arbs:
    #     print(a.to_string())

    print("OVERALL EXECUTION TIME")
    print("--- %s seconds ---" % (time.time() - start_time))
