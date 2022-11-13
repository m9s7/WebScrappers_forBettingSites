import ctypes
import time

from find_arb import find_arb
from requests_to_server.telegram import broadcast_to_telegram

from maxbet.scrape.maxbet_scraper import scrape as scrape_maxbet
from mozzart.scrape.mozzart_scraper import scrape as scrape_mozzart

from models.match_model import StandardNames, MaxbNames, MozzNames, SoccbetNames

from maxbet.scrape.maxbet_scraper import get_sports_currently_offered as get_sports_currently_offered_maxb
from mozzart.scrape.mozzart_scraper import get_sports_currently_offered as get_sports_currently_offered_mozz
from soccerbet.scraper import get_sports_currently_offered as get_sports_currently_offered_soccbet


def get_sports_to_scrape():
    sports_im_interested_in = {
        StandardNames.tennis,
        StandardNames.basketball,
        StandardNames.esports,
        StandardNames.soccer,
        StandardNames.tabletennis
    }
    maxb_available_sports = set(
        [MaxbNames.fromString(s).toStandardName() for s in get_sports_currently_offered_maxb() if
         MaxbNames.fromString(s) is not None])
    mozz_available_sports = set(
        [MozzNames.fromString(s).toStandardName() for s in get_sports_currently_offered_mozz() if
         MozzNames.fromString(s) is not None])
    soccbet_available_sports = set(
        [SoccbetNames.fromString(s).toStandardName() for s in get_sports_currently_offered_soccbet() if
         SoccbetNames.fromString(s) is not None])

    available_bookies = [maxb_available_sports, mozz_available_sports, soccbet_available_sports]

    print("Sports I'm interested in: ", sports_im_interested_in)
    print("Maxbet sports available: ", maxb_available_sports)
    print("Mozzart sports available: ", mozz_available_sports)
    print("Soccerbet sports available: ", soccbet_available_sports)

    sports_to_scrape = []
    for s in sports_im_interested_in:
        if in_at_least_2(s, available_bookies):
            sports_to_scrape.append(s)
    print("Sports that will be scraped: ", [str(s) for s in sports_to_scrape])

    return sports_to_scrape


def in_at_least_2(el, set_list):
    counter = 0
    for s in set_list:
        if el in s:
            counter += 1
        if counter >= 2:
            return True
    return False


# ne match-uje mi OutSliders - Mouz i MOUZ - Outsiders, zasto

# old_arbs
def program():
    start_time = time.time()

    library = ctypes.windll.LoadLibrary(
        r'C:\Users\Matija\PycharmProjects\ScrapeEscape\SportsBettingScrapers\go_code\merge_dfs.dll')
    merge = library.merge
    merge.argtypes = [ctypes.c_char_p]

    # TODO: parallelize scraping
    sports_to_scrape = get_sports_to_scrape()
    scrape_maxbet([s.toMaxbName() for s in sports_to_scrape])
    scrape_mozzart([s.toMozzName() for s in sports_to_scrape])

    arbs = []
    for sport in sports_to_scrape:
        arg = str(sport).encode("utf-8")
        merge(arg)
        res = find_arb(str(sport), 1000)
        if res is None:
            print("nema arbe ", sport, "\n")
        else:
            arbs.append(res)

    if len(arbs) != 0:
        broadcast_to_telegram("ALO LELEMUDI STIGLE FRISKE ARBE")
        # if len(old_arbs) == 0:
        #     [broadcast_to_telegram(a.to_string()) for a in arbs]
        # else:
        #     for a in arbs:
        #         print(a.to_string())
        #         for b in old_arbs:
        #             print(b.to_string())
        #             print(a.compare(b))
        #             print(a.compare(b).empty)
    else:
        broadcast_to_telegram("nema arbe :'(")

    print('wha')
    for a in arbs:
        print(a.to_string())

    print("OVERALL EXECUTION TIME")
    print("--- %s seconds ---" % (time.time() - start_time))

    return arbs

# def is_df_in_df_list(df, df_list):
#     for el in df_list:
#         if are_equal_dfs(df, el):
#             return True
#     return False
#
#
# def are_equal_dfs(df1, df2):
#     return df1.compare(df2).empty
