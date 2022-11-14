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
    tennis = 'Tenis'
    basketball = 'Košarka'
    esports = 'Esports'
    soccer = 'Fudbal'
    tabletennis = 'Stoni tenis'

    def toStandardName(self):
        if self == MozzNames.tennis:
            return StandardNames.tennis
        if self == MozzNames.basketball:
            return StandardNames.basketball
        if self == MozzNames.esports:
            return StandardNames.esports
        if self == MozzNames.soccer:
            return StandardNames.soccer
        if self == MozzNames.tabletennis:
            return StandardNames.tabletennis
        raise ValueError('Unsuported value')

    @staticmethod
    def fromString(s):
        try:
            result = MozzNames(s)
        except ValueError:
            result = None
        finally:
            return result

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
        try:
            result = MaxbNames(s)
        except ValueError:
            result = None
        finally:
            return result
class SoccbetNames(str, enum.Enum):
    tennis = 'Tenis',
    basketball = 'Košarka',
    esports = 'ESport',
    soccer = 'Fudbal',
    tabletennis = 'Stoni Tenis',

    def toStandardName(self):
        if self == SoccbetNames.tennis:
            return StandardNames.tennis
        if self == SoccbetNames.basketball:
            return StandardNames.basketball
        if self == SoccbetNames.esports:
            return StandardNames.esports
        if self == SoccbetNames.soccer:
            return StandardNames.soccer
        if self == SoccbetNames.tabletennis:
            return StandardNames.tabletennis
        raise ValueError('Unsuported value here')

    @staticmethod
    def fromString(s):
        try:
            result = SoccbetNames(s)
        except ValueError:
            result = None
        finally:
            return result

class StandardNames(str, enum.Enum):
    tennis = 'tennis',
    basketball = 'basketball',
    esports = 'esports'
    soccer = 'soccer'
    tabletennis = 'tabletennis'

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

    def toSoccbetName(self):
        if self == StandardNames.tennis:
            return SoccbetNames.tennis
        if self == StandardNames.basketball:
            return SoccbetNames.basketball
        if self == StandardNames.esports:
            return SoccbetNames.esports
        if self == StandardNames.tabletennis:
            return SoccbetNames.tabletennis
        if self == StandardNames.soccer:
            return SoccbetNames.soccer
        raise ValueError('Unsuported value')

scraper_columns = ['kick_off', 'league', '1', '2', 'tip1_name', 'tip1_val', 'tip2_name', 'tip2_val']