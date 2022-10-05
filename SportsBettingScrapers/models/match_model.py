class Match:
    def __init__(self, match_id, start_time, participants=None, subgames=None):
        if participants is None:
            participants = []
        if subgames is None:
            subgames = []
        self.match_id = match_id
        self.start_time = start_time
        self.participants = participants
        self.subgames = subgames

    def __str__(self):
        return f"ID: {self.match_id} | {' vs '.join([p.name for p in self.participants])} \n{''.join([s.__str__() for s in self.subgames])} \n"


class Participant:
    def __init__(self, participant_id, name):
        self.participant_id = participant_id
        self.name = name


class Subgame:
    def __init__(self, game_name, game_shortname, subgame_name, subgame_description, value):
        self.game_name = game_name
        self.game_shortname = game_shortname
        self.subgame_name = subgame_name
        self.subgame_description = subgame_description
        self.value = value

    def __str__(self):
        return f"{self.game_name} ({self.game_shortname}) - {self.subgame_name} ({self.subgame_description}) : {self.value} \n"
