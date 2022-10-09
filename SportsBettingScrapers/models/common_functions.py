import json
import sys


def print_to_file(data, file):
    original_stdout = sys.stdout
    with open(f'output/{file}', 'w', encoding="utf-8") as f:
        sys.stdout = f
        print(data)
        sys.stdout = original_stdout


def nice_print_json(data_json):
    print(json.dumps(data_json, indent=4, separators=(',', ': '), ensure_ascii=False).encode('utf8').decode())
