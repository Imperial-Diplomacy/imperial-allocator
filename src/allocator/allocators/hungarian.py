import logging
import numpy as np
from scipy.optimize import linear_sum_assignment
from typing import List

from allocator import utils
from allocator.config import Config
from allocator.domain.models import Game, Player
from allocator.allocators.base import BaseAllocator

logger = logging.getLogger(__name__)


class HungarianAllocator(BaseAllocator):
	def __init__(self, config: Config):
		self.config = config
		self.powers = config.powers
		self.rng = np.random.default_rng(config.seed)

	@utils.timer
	def allocate(self, players: List[Player]) -> List[Game]:
		ranked = [p for p in players if not p.no_preference]
		scraps = [p for p in players if p.no_preference]

		num_games = int(round(len(players) / len(self.powers), 0))
		games = [Game(i) for i in range(num_games)]
		logger.info(f"Decided on {num_games} games for {len(players)} players")

		matrix = self._build_matrix(ranked, num_games)
		row_idx, col_idx = linear_sum_assignment(-matrix)

		self._assign_ranked(games, ranked, row_idx, col_idx)
		self._assign_scrap(games, scraps)

		return games

	def _build_matrix(self, players, num_games):
		logger.info("Constructing power preference score matrix")
		matrix = np.zeros((len(players), len(self.powers) * num_games))
		for i, p in enumerate(players):
			for j, power in enumerate(self.powers * num_games):
				matrix[i, j] = p.preferences.get(power, 0)

		logger.info("Adding noise to power preference score matrix")
		noise = self.rng.integers(0, 5, size=matrix.shape)
		matrix = matrix * 100 + noise

		logger.info("Built power preference score matrix")
		return matrix

	def _assign_ranked(self, games, ranked, row_idx, col_idx) -> None:
		logger.info("Allocating players their preferred players")
		for r, c in zip(row_idx, col_idx):
			player = ranked[r]
			game_id = c // len(self.powers)
			power = self.powers[c % len(self.powers)]

			if power not in player.preferences:
				logger.warning(
					f"User {player.name} was not allocated a preferred power: Reassigned as scrap"
				)
				games[game_id].add_scrap(player)
				continue

			games[game_id].add_player(power, player)

	def _assign_scrap(self, games: List[Game], scraps) -> None:
		logger.info("Allocating no preference players to vacant slots")
		self.rng.shuffle(scraps)

		for g in games:
			remaining = len(self.powers) - len(g.all_players())

			available = min(remaining, len(scraps))
			for _ in range(available):
				p = scraps.pop()
				g.add_scrap(p)

		lost = "|".join(map(lambda p: f"{p.name}", scraps))
		if lost:
			logger.critical(f"{len(scraps)} unassigned scrap players: [{lost}]")
