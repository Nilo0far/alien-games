
from enum import Enum


class Tile(str, Enum):
    WALL = "#"
    EMPTY = "."
    START = "S"
    GOAL = "G"
    HAZARD = "H"
    MUD = "M"


TILE_COSTS = {
    Tile.EMPTY: 1,
    Tile.START: 1,
    Tile.GOAL: 1,
    Tile.HAZARD: 5,
    Tile.MUD: 3,
}
