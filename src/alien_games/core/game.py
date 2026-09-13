
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .tiles import Tile, TILE_COSTS


Position = tuple[int, int]


@dataclass(frozen=True)
class Game:
    grid: tuple[tuple[Tile, ...], ...]
    start: Position
    goal: Position

    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> "Game":
        rows = [line.strip() for line in lines if line.strip()]

        if not rows:
            raise ValueError("Game cannot be empty.")

        width = len(rows[0])

        if any(len(row) != width for row in rows):
            raise ValueError("All rows must have the same width.")

        grid: list[list[Tile]] = []
        start: Position | None = None
        goal: Position | None = None

        for row_index, row in enumerate(rows):
            parsed_row: list[Tile] = []

            for col_index, symbol in enumerate(row):
                try:
                    tile = Tile(symbol)
                except ValueError as exc:
                    raise ValueError(
                        f"Invalid tile '{symbol}' at "
                        f"({row_index}, {col_index})."
                    ) from exc

                if tile == Tile.START:
                    if start is not None:
                        raise ValueError(
                            "Game must contain exactly one start tile."
                        )
                    start = (row_index, col_index)

                if tile == Tile.GOAL:
                    if goal is not None:
                        raise ValueError(
                            "Game must contain exactly one goal tile."
                        )
                    goal = (row_index, col_index)

                parsed_row.append(tile)

            grid.append(parsed_row)

        if start is None:
            raise ValueError("Game must contain a start tile.")

        if goal is None:
            raise ValueError("Game must contain a goal tile.")

        return cls(
            grid=tuple(tuple(row) for row in grid),
            start=start,
            goal=goal,
        )

    @property
    def height(self) -> int:
        return len(self.grid)

    @property
    def width(self) -> int:
        return len(self.grid[0])

    def in_bounds(self, position: Position) -> bool:
        row, col = position
        return 0 <= row < self.height and 0 <= col < self.width

    def tile_at(self, position: Position) -> Tile:
        if not self.in_bounds(position):
            raise IndexError(
                f"Position {position} is outside the game grid."
            )

        row, col = position
        return self.grid[row][col]

    def is_walkable(self, position: Position) -> bool:
        return (
            self.in_bounds(position)
            and self.tile_at(position) != Tile.WALL
        )

    def movement_cost(self, position: Position) -> int:
        tile = self.tile_at(position)

        if tile == Tile.WALL:
            raise ValueError("Walls do not have a movement cost.")

        return TILE_COSTS[tile]

    def neighbors(self, position: Position) -> list[Position]:
        row, col = position

        candidates = [
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1),
        ]

        return [
            candidate
            for candidate in candidates
            if self.is_walkable(candidate)
        ]

    def to_lines(self) -> list[str]:
        return [
            "".join(tile.value for tile in row)
            for row in self.grid
        ]

    def __str__(self) -> str:
        return "\n".join(self.to_lines())
