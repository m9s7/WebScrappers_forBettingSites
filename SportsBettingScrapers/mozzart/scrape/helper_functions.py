def init_export_help(matches_response):
    export = {}
    for match in matches_response:
        if match['specialType'] != 0 or len(match['participants']) != 2:
            continue
        e = [
            match['startTime'],
            match['competition_name_sr'],
            match['participants'][0]['name'].strip(),
            match['participants'][1]['name'].strip()
        ]
        export[match['id']] = e

    return export


def get_subgame_ids(offers, interested_subgames_list):
    focused_subgames = []
    for offer in offers:
        if offer['name'] != "Kompletna ponuda":
            continue
        for header in offer['regularHeaders']:
            game = header['gameName'][0]
            if game['shortName'] in interested_subgames_list:
                for subgame in header['subGameName']:
                    focused_subgames.append(subgame['id'])

    return focused_subgames
