
from __future__ import annotations

from dataclasses import dataclass

from src.alien_games.agents.astar import AStarAgent
from src.alien_games.agents.base import SearchResult
from src.alien_games.agents.bfs import BFSAgent
from src.alien_games.agents.greedy import GreedyAgent
from src.alien_games.core.game import Game


@dataclass(frozen=True)
class EvaluationResult:
    results: dict[str, SearchResult]

    @property
    def solved_by_all(self) -> bool:
        return all(
            result.solved
            for result in self.results.values()
        )

    @property
    def solved_count(self) -> int:
        return sum(
            result.solved
            for result in self.results.values()
        )


class GameEvaluator:
    def __init__(self) -> None:
        self.agents = [
            BFSAgent(),
            GreedyAgent(),
            AStarAgent(),
        ]

    def evaluate(self, game: Game) -> EvaluationResult:
        results = {
            agent.name: agent.solve(game)
            for agent in self.agents
        }

        return EvaluationResult(results=results)
