from enum import Enum

__author__ = "Snekith, Patrick and Ashwin"
__date__ = "17/06/2023"


class MoveType(Enum):
    """
    Enum to contain all move types

    Args:
        Enum: Enum for outlines
    """

    PLACE = "place"
    MOVE = "move"
    REMOVE = "remove"
    FLY = "fly"
