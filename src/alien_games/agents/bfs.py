
from __future__ import annotations

from collections import deque

from src.alien_games.agents.base import SearchResult
from src.alien_games.core.game import Game, Position


class BFSAgent:
    name = "BFS"

    def solve(self, game: Game) -> SearchResult:
        frontier = deque([game.start])

        parents: dict[Position, Position | None] = {
            game.start: None
        }

        nodes_expanded = 0

        while frontier:
            current = frontier.popleft()
            nodes_expanded += 1

            if current == game.goal:
                path = self._reconstruct_path(
                    parents=parents,
                    goal=game.goal,
                )

                path_cost = self._calculate_path_cost(
                    game=game,
                    path=path,
                )

                return SearchResult(
                    solved=True,
                    path=path,
                    path_cost=path_cost,
                    nodes_expanded=nodes_expanded,
                )

            for neighbor in game.neighbors(current):
                if neighbor not in parents:
                    parents[neighbor] = current
                    frontier.append(neighbor)

        return SearchResult(
            solved=False,
            path=(),
            path_cost=0,
            nodes_expanded=nodes_expanded,
        )

    @staticmethod
    def _reconstruct_path(
        parents: dict[Position, Position | None],
        goal: Position,
    ) -> tuple[Position, ...]:
        path: list[Position] = []

        current: Position | None = goal

        while current is not None:
            path.append(current)
            current = parents[current]

        path.reverse()

        return tuple(path)

    @staticmethod
    def _calculate_path_cost(
        game: Game,
        path: tuple[Position, ...],
    ) -> int:
        if len(path) <= 1:
            return 0

        return sum(
            game.movement_cost(position)
            for position in path[1:]
        )
