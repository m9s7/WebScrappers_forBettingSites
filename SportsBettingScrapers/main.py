from fuzzywuzzy import process, fuzz

from maxbet_scraper import scrape as scrape_maxbet
from mozzart_scraper import scrape as scrape_mozzart

print(fuzz.ratio('Van De Zandschulp B.', 'Van De Zands. B.'))
print(fuzz.partial_ratio('Van De Zandschulp B.', 'Van De Zands. B.'))
print(fuzz.token_sort_ratio('Van De Zandschulp B.', 'Van De Zands. B.'))
print(fuzz.WRatio('Van De Zandschulp B.', 'Van De Zands. B.'))

maxb = scrape_maxbet()
mozz = scrape_mozzart()

print(maxb)
print(mozz)

# TODO: Merge and compare dataframes with fuzz
