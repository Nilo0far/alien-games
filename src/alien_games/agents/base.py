
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from src.alien_games.core.game import Game, Position


@dataclass(frozen=True)
class SearchResult:
    solved: bool
    path: tuple[Position, ...]
    path_cost: int
    nodes_expanded: int


class Agent(Protocol):
    name: str

    def solve(self, game: Game) -> SearchResult:
        ...
