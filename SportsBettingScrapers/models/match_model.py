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

    def toStandardName(self):
        if self == MozzNames.tennis:
            return StandardNames.tennis
        if self == MozzNames.basketball:
            return StandardNames.basketball
        if self == MozzNames.esports:
            return StandardNames.esports
        if self == MozzNames.soccer:
            return StandardNames.soccer
        raise ValueError('Unsuported value')

    @staticmethod
    def fromString(s):
        if s == 'Tenis':
            return MozzNames.tennis
        if s == 'Košarka':
            return MozzNames.basketball
        if s == 'Esports':
            return MozzNames.esports
        if s == 'Fudbal':
            return MozzNames.soccer
        return None

class MaxbNames(str, enum.Enum):
    tennis = 'Tenis',
    basketball = 'Košarka',
    esports = 'eSport',
    soccer = 'Fudbal',
    tabletennis = 'Stoni Tenis',

    def toStandardName(self):
        if self == MaxbNames.tennis:
            return StandardNames.tennis
        if self == MaxbNames.basketball:
            return StandardNames.basketball
        if self == MaxbNames.esports:
            return StandardNames.esports
        if self == MaxbNames.soccer:
            return StandardNames.soccer
        if self == MaxbNames.tabletennis:
            return StandardNames.tabletennis
        raise ValueError('Unsuported value here')

    @staticmethod
    def fromString(s):
        if s == 'Tenis':
            return MaxbNames.tennis
        if s == 'Košarka':
            return MaxbNames.basketball
        if s == 'Esports':
            return MaxbNames.esports
        if s == 'Fudbal':
            return MaxbNames.soccer
        if s == 'Stoni Tenis':
            return MaxbNames.tabletennis
        return None



class StandardNames(str, enum.Enum):
    tennis = 'tennis',
    basketball = 'basketball',
    esports = 'esports'
    soccer = 'soccer'
    tabletennis = 'table_tennis'

    def __str__(self):
        return str(self.value)

    def toMaxbName(self):
        if self == StandardNames.tennis:
            return MaxbNames.tennis
        if self == StandardNames.basketball:
            return MaxbNames.basketball
        if self == StandardNames.esports:
            return MaxbNames.esports
        if self == StandardNames.tabletennis:
            return MaxbNames.tabletennis
        if self == StandardNames.soccer:
            return MaxbNames.soccer
        raise ValueError('Unsuported value')

    def toMozzName(self):
        if self == StandardNames.tennis:
            return MozzNames.tennis
        if self == StandardNames.basketball:
            return MozzNames.basketball
        if self == StandardNames.esports:
            return MozzNames.esports
        if self == StandardNames.tabletennis:
            return MozzNames.tabletennis
        if self == StandardNames.soccer:
            return MozzNames.soccer
        raise ValueError('Unsuported value')

scraper_columns = ['kick_off', 'league', '1', '2', 'tip1_name', 'tip1_val', 'tip2_name', 'tip2_val']