
from __future__ import annotations

import heapq
from itertools import count

from src.alien_games.agents.base import SearchResult
from src.alien_games.core.game import Game, Position


class AStarAgent:
    name = "A*"

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

        g_costs: dict[Position, int] = {
            game.start: 0
        }

        closed: set[Position] = set()

        nodes_expanded = 0

        while frontier:
            _, _, current = heapq.heappop(frontier)

            if current in closed:
                continue

            closed.add(current)
            nodes_expanded += 1

            if current == game.goal:
                path = self._reconstruct_path(
                    parents=parents,
                    goal=game.goal,
                )

                return SearchResult(
                    solved=True,
                    path=path,
                    path_cost=g_costs[game.goal],
                    nodes_expanded=nodes_expanded,
                )

            for neighbor in game.neighbors(current):
                if neighbor in closed:
                    continue

                tentative_cost = (
                    g_costs[current]
                    + game.movement_cost(neighbor)
                )

                if (
                    neighbor not in g_costs
                    or tentative_cost < g_costs[neighbor]
                ):
                    g_costs[neighbor] = tentative_cost
                    parents[neighbor] = current

                    f_cost = (
                        tentative_cost
                        + self._heuristic(neighbor, game.goal)
                    )

                    heapq.heappush(
                        frontier,
                        (
                            f_cost,
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
