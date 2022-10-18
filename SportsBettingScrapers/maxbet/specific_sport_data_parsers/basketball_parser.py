import pandas as pd

from models.match_model import ExportIDX
from requests_to_server.maxbet_requests import get_match_data


def parse_basketball_data(response_json):
    export = {}
    for league in response_json:
        for match in league['matchList']:

            match_info = get_match_data(match['id']).json()
            e = [match['home'], match['away'], None, None, None, None]
            for subgame in match_info['odBetPickGroups']:
                if subgame['name'] != "Konačan ishod sa produžecima":
                    continue
                e[ExportIDX.TIP1_NAME] = subgame['tipTypes'][0]['tipType']
                e[ExportIDX.TIP1_VAL] = subgame['tipTypes'][0]['value']
                e[ExportIDX.TIP2_NAME] = subgame['tipTypes'][1]['tipType']
                e[ExportIDX.TIP2_VAL] = subgame['tipTypes'][1]['value']

            export[match['id']] = e

    df = pd.DataFrame(list(export.values()), columns=['1', '2', 'tip1_name', 'tip1_val', 'tip2_name', 'tip2_val'])
    return df
