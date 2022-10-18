import pandas as pd

from models.match_model import ExportIDX


def parse_ki_data(response_json):
    export = {}
    for league in response_json:
        for match in league['matchList']:
            e = [match['home'].strip(), match['away'].strip(), None, None, None, None]
            for i in match['odBetPickGroups']:
                for j in i['tipTypes']:

                    # if X exists, match is not 2-outcome
                    if j['tipType'] == "KI_X" and j['value'] != 0:
                        e = [match['home'], match['away'], None, None, None, None]
                        break

                    if j['tipType'] == "KI_1":
                        e[ExportIDX.TIP1_NAME] = 'KI_1'
                        e[ExportIDX.TIP1_VAL] = j['value']
                    elif j['tipType'] == "KI_2":
                        e[ExportIDX.TIP2_NAME] = 'KI_2'
                        e[ExportIDX.TIP2_VAL] = j['value']
                    else:
                        continue

            export[match['id']] = e

    df = pd.DataFrame(list(export.values()), columns=['1', '2', 'tip1_name', 'tip1_val', 'tip2_name', 'tip2_val'])
    return df
