import pandas as pd

from models.match_model import Subgames


def parse_ki_data(response_json):
    export = {}
    for league in response_json:
        for match in league['matchList']:
            e = [match['home'], match['away'], None, None]
            for i in match['odBetPickGroups']:
                for j in i['tipTypes']:

                    # if X exists, match is not 2-outcome
                    if j['tipType'] == "KI_X" and j['value'] != 0:
                        e = [match['home'], match['away'], None, None]
                        break

                    if j['tipType'] == "KI_1":
                        e[Subgames.KI_1] = j['value']
                    elif j['tipType'] == "KI_2":
                        e[Subgames.KI_2] = j['value']
                    else:
                        continue

            export[match['id']] = e

    columns = ['1', '2', 'KI_1', 'KI_2']

    # index = list(export.keys())
    # , index = index
    df = pd.DataFrame(list(export.values()), columns=columns)

    return df
