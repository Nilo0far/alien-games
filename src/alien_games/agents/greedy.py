
from __future__ import annotations

import heapq
from itertools import count

from src.alien_games.agents.base import SearchResult
from src.alien_games.core.game import Game, Position


class GreedyAgent:
    name = "Greedy Best-First"

    def solve(self, game: Game) -> SearchResult:
        tie_breaker = count()

        frontier: list[tuple[int, int, Position]] = []

        heapq.heappush(
            frontier,
            (
                self._heuristic(game.start, game.goal),
                next(tie_breaker),
                game.start,
            ),
        )

        parents: dict[Position, Position | None] = {
            game.start: None
        }

        visited: set[Position] = set()

        nodes_expanded = 0

        while frontier:
            _, _, current = heapq.heappop(frontier)

            if current in visited:
                continue

            visited.add(current)
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
                if neighbor in visited:
                    continue

                if neighbor not in parents:
                    parents[neighbor] = current

                    heapq.heappush(
                        frontier,
                        (
                            self._heuristic(neighbor, game.goal),
                            next(tie_breaker),
                            neighbor,
                        ),
                    )

        return SearchResult(
            solved=False,
            path=(),
            path_cost=0,
            nodes_expanded=nodes_expanded,
        )

    @staticmethod
    def _heuristic(
        position: Position,
        goal: Position,
    ) -> int:
        row, col = position
        goal_row, goal_col = goal

        return abs(row - goal_row) + abs(col - goal_col)

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
