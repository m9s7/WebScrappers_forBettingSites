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
