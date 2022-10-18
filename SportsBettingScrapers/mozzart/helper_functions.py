def get_sidebar_sport_by_name(name, sidebar_sports):
    for sport in sidebar_sports:
        if sport['name'] == name:
            return sport

    raise KeyError(f"Mozzart: '{name}' not currently offered")


def init_export_with_matches(matches_response):
    export = {}
    for match in matches_response:
        if match['specialType'] != 0 or len(match['participants']) != 2:
            continue
        e = [match['participants'][0]['name'], match['participants'][1]['name'], None, None, None, None]
        export[match['id']] = e

    return export


def parse_sidebar(sidebar_response):
    name_id_dict = {}
    for sport in sidebar_response:
        name_id_dict[sport['name']] = sport['id']

    return name_id_dict
