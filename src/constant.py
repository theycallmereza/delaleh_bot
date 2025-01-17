from enum import Enum


class STATES(Enum):
    NAME = 0
    BIRTH_DATE = 1
    HEIGHT = 2
    BIO = 3
    IMAGE = 4
    LOCATION = 5


class UpdateProfileStates(Enum):
    NAME = 1
    BIRTH_DATE = 2
    HEIGHT = 3
    BIO = 4
    IMAGE = 5
    LOCATION = 6
