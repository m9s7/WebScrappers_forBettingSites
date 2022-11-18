import ctypes
import time

from common.models import StandardNames, MaxbNames, MozzNames, SoccbetNames
from bookies.maxbet.scrape.maxbet_scraper import get_sports_currently_offered as get_sports_currently_offered_maxb, \
    scrape as scrape_maxbet
from bookies.mozzart.scrape.mozzart_scraper import get_sports_currently_offered as get_sports_currently_offered_mozz, \
    scrape as scrape_mozzart
from bookies.soccerbet.scrape.soccerbet_scraper import \
    get_sports_currently_offered as get_sports_currently_offered_soccbet, scrape as scrape_soccerbet
from find_arb import find_arb
from requests_to_server.telegram import broadcast_to_telegram


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

    print("Sports I'm interested in: ", [str(s) for s in sports_im_interested_in], '\n')
    print("Maxbet sports available: ", [str(s) for s in maxb_available_sports])
    print("Mozzart sports available: ", [str(s) for s in mozz_available_sports])
    print("Soccerbet sports available: ", [str(s) for s in soccbet_available_sports])

    sports_to_scrape = []
    for s in sports_im_interested_in:
        if in_at_least_2(s, available_bookies):
            sports_to_scrape.append(s)
    print("\nSports that will be scraped: ", [str(s) for s in sports_to_scrape])

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
def get_bookies_names(a):
    book1_name, book2_name = "", ""
    for k, v in a.items():
        if k.endswith('MAX'):
            continue
        if k.startswith('tip1_') and a[k] == a['tip1_MAX']:
            book1_name = k.removeprefix('tip1_')
        if k.startswith('tip2_') and a[k] == a['tip2_MAX']:
            book2_name = k.removeprefix('tip2_')

    return book1_name, book2_name


def center(line, max_line_len):
    line_len = len(line)
    padding = (max_line_len - line_len) // 2
    return '|' + (' '*padding) + line + (' '*padding) + '|'


def program():
    start_time = time.time()

    library = ctypes.windll.LoadLibrary(
        r'C:\Users\Matija\PycharmProjects\ScrapeEscape\SportsBettingScrapers\go_code\merge_dfs.dll')
    merge = library.merge
    merge.argtypes = [ctypes.c_char_p]

    # TODO: parallelize scraping
    sports_to_scrape = get_sports_to_scrape()

    arbs = []
    for sport in sports_to_scrape:
        scrape_maxbet([sport.toMaxbName()])
        scrape_mozzart([sport.toMozzName()])
        scrape_soccerbet([sport.toSoccbetName()])

        arg = str(sport).encode("utf-8")
        merge(arg)
        res = find_arb(str(sport), 1000)
        if res is None:
            continue
        arbs.append(res)

        for a in res.to_dict('records'):
            line0 = " --FRISKE ARBE-- "
            league_name = next(v for k, v in a.items() if k.startswith('league_') and v is not None)
            line1 = f"{sport}, {league_name.lower()}"
            line2 = f"{a['1']} vs {a['2']}"
            book1_name, book2_name = get_bookies_names(a)
            line3p5 = f"{book1_name}:"
            line3 = f"{a['tip1'].lower()} @ {a['tip1_MAX']} <- {a['stake1']} din."
            line4p5 = f"{book2_name}:"
            line4 = f"{a['tip2'].lower()} @ {a['tip2_MAX']} <- {a['stake2']} din."
            line5 = f"ROI: {a['ROI']}%"

            lines = [line0, line1, line2, line3, line3p5, line4, line4p5, line5]
            max_line_len = max([len(line) for line in lines])
            lines = [center(line, max_line_len) for line in lines]
            content = '\n'.join(lines)
            broadcast_to_telegram(content)
            # broadcast_to_telegram(json.dumps(a, indent=2))

    # if len(arbs) != 0:
    #     broadcast_to_telegram("ALO LELEMUDI, STIGLE FRISKE ARBE")
    #     for a in arbs:
    #         broadcast_to_telegram(a)
    #         print(a)

    # if len(old_arbs) == 0:
    #     [broadcast_to_telegram(a.to_string()) for a in arbs]
    # else:
    #     for a in arbs:
    #         print(a.to_string())
    #         for b in old_arbs:
    #             print(b.to_string())
    #             print(a.compare(b))
    #             print(a.compare(b).empty)
    # else:
    #     broadcast_to_telegram("nema arbe :'(")

    print("OVERALL EXECUTION TIME")
    print("--- %s seconds ---" % (time.time() - start_time))
    # return arbs


program()
