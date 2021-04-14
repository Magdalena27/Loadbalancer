from enum import Enum


class StatusOfClient(Enum):
    IN_QUEUE = 0,
    CONNECTING_WITH_DRIVE = 1,
    SERVED = 2,
    IN_WAITING_ROOM = 3,
    JUST_GENERATED = 4
