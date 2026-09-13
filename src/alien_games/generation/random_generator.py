
from __future__ import annotations

import random

from src.alien_games.core.game import Game
from src.alien_games.core.tiles import Tile


class RandomGameGenerator:
    def __init__(
        self,
        width: int = 9,
        height: int = 9,
        wall_probability: float = 0.20,
        hazard_probability: float = 0.08,
        mud_probability: float = 0.08,
        seed: int | None = None,
    ) -> None:
        if width < 5 or height < 5:
            raise ValueError(
                "Game width and height must be at least 5."
            )

        total_probability = (
            wall_probability
            + hazard_probability
            + mud_probability
        )

        if total_probability > 1.0:
            raise ValueError(
                "Tile probabilities cannot sum to more than 1."
            )

        self.width = width
        self.height = height
        self.wall_probability = wall_probability
        self.hazard_probability = hazard_probability
        self.mud_probability = mud_probability

        self.random = random.Random(seed)

    def generate(self) -> Game:
        grid = [
            [Tile.WALL for _ in range(self.width)]
            for _ in range(self.height)
        ]

        for row in range(1, self.height - 1):
            for col in range(1, self.width - 1):
                grid[row][col] = self._random_floor_tile()

        start = self._random_position()
        goal = self._random_position()

        while goal == start:
            goal = self._random_position()

        start_row, start_col = start
        goal_row, goal_col = goal

        grid[start_row][start_col] = Tile.START
        grid[goal_row][goal_col] = Tile.GOAL

        lines = [
            "".join(tile.value for tile in row)
            for row in grid
        ]

        return Game.from_lines(lines)

    def _random_position(self) -> tuple[int, int]:
        row = self.random.randint(1, self.height - 2)
        col = self.random.randint(1, self.width - 2)

        return row, col

    def _random_floor_tile(self) -> Tile:
        value = self.random.random()

        if value < self.wall_probability:
            return Tile.WALL

        if value < (
            self.wall_probability
            + self.hazard_probability
        ):
            return Tile.HAZARD

        if value < (
            self.wall_probability
            + self.hazard_probability
            + self.mud_probability
        ):
            return Tile.MUD

        return Tile.EMPTY
