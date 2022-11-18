import json
import os
import sys


def print_to_file(data, file, mode='w+'):
    old_dir = os.getcwd()
    os.chdir(r"C:\Users\Matija\PycharmProjects\ScrapeEscape\SportsBettingScrapers\output")

    original_stdout = sys.stdout
    with open(file, mode, encoding="utf-8") as f:
        sys.stdout = f
        print(data)
        sys.stdout = original_stdout

    os.chdir(old_dir)


def nice_print_json(data_json):
    print(json.dumps(data_json, indent=4, separators=(',', ': '), ensure_ascii=False).encode('utf8').decode())


def box_print(string):
    box_char = '='
    print('\n')
    print(box_char * (len(string) + 4))
    print(box_char, string, box_char)
    print(box_char * (len(string) + 4), '\n')


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def export_for_merge(data, file):
    old_dir = os.getcwd()
    os.chdir(r'C:\Users\Matija\PycharmProjects\ScrapeEscape\SportsBettingScrapers\go_code\dfs_for_import')

    original_stdout = sys.stdout
    with open(file, 'w+', encoding="utf-8") as f:
        sys.stdout = f
        print(data.to_csv(index=False, lineterminator='\n'))
        sys.stdout = original_stdout

    os.chdir(old_dir)

# Append 2 dfs with same column names
# df = pd.concat([df_tennis, df_basketball], axis=0)

# Add new column with same values for all rows
# df['sport'] = sport_name
