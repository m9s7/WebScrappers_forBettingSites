import enum


class ExportIDX(enum.IntEnum):
    KICKOFF = 0,
    LEAGUE = 1,
    TEAM_1 = 2,
    TEAM_2 = 3,
    TIP1_NAME = 4,
    TIP1_VAL = 5,
    TIP2_NAME = 6,
    TIP2_VAL = 7,


class MozzNames(str, enum.Enum):
    tennis = 'Tenis',
    basketball = 'Košarka',
    esports = 'Esports'
    soccer = 'Fudbal'


class MaxbNames(str, enum.Enum):
    tennis = 'Tenis',
    basketball = 'Košarka',
    esports = 'eSport'
    soccer = 'Fudbal'
    tabletennis = 'Stoni Tenis'


class StandardNames(str, enum.Enum):
    def __str__(self):
        return str(self.value)

    tennis = 'tennis',
    basketball = 'basketball',
    esports = 'esports'
    soccer = 'soccer'
    tabletennis = 'table tennis'

scraper_columns = ['kick_off', 'league', '1', '2', 'tip1_name', 'tip1_val', 'tip2_name', 'tip2_val']