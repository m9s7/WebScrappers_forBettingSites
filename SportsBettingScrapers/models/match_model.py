import enum


class ExportIDX(enum.IntEnum):
    TEAM_1 = 0,
    TEAM_2 = 1,
    TIP1_NAME = 2,
    TIP1_VAL = 3,
    TIP2_NAME = 4,
    TIP2_VAL = 5


class MozzNames(str, enum.Enum):
    tennis = 'Tenis',
    basketball = 'Košarka',
    esports = 'Esports'
    soccer = 'Fudbal'


# Nisam ovo podesio i nznm sta cu da tim imenima kako da ih ord
class MaxbNames(str, enum.Enum):
    tennis = 'Tenis',
    basketball = 'Košarka',
    esports = 'eSport'
    soccer = 'Fudbal'


class StandardNames(str, enum.Enum):
    def __str__(self):
        return str(self.value)

    tennis = 'tennis',
    basketball = 'basketball',
    esports = 'esports'
    soccer = 'soccer'
