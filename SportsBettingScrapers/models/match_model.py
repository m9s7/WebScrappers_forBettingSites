import enum


class Subgames(enum.IntEnum):
    KI_1 = 2
    KI_2 = 3
    FT_OT_1 = 2
    FT_OT_2 = 3


class MozzNames(str, enum.Enum):
    tennis = 'Tenis',
    basketball = 'Košarka',
    esports = 'Esports'
    soccer = 'Fudbal'
