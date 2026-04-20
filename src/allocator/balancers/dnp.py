import logging
import numpy as np

from allocator import utils
from allocator.config import Config

logger = logging.getLogger(__name__)

class DNPValidator:
	def __init__(self, config: Config, players):
		self.config = config
		self.players = players
		self.rng = np.random.default_rng(config.seed)
	
	@utils.timer
	def balance(self, games):
		max_attempts = 25
		logger.info(f"Attempting to auto-balance DNP lists ({max_attempts} attempts)")

		for attempt in range(1, max_attempts + 1):
			logger.info(f"DNP lists auto-balance attempt: {attempt}")
			validated = self._run_attempt(games)

			logger.info(f"Attempt {attempt} results: {validated}")

			if all(validated):
				logger.info("Successful Do Not Play balancing!")
				return games

		logger.warning("Unsuccessful Do Not Play balancing...")
		return games

	def _run_attempt(self, games):
		validated = []

		for i, game in enumerate(games):
			conflicts = self._get_conflicts(game)

			if not conflicts:
				validated.append(True)
				continue

			logger.info(f"Game {i}: {len(conflicts)} DNP conflicts")

			self._resolve_game_conflicts(i, game, games, conflicts)
			validated.append(len(self._get_conflicts(game)) == 0)

		return validated

	def _get_conflicts(self, game):
		players = {p.name for p in game.all_players()}
		return game.all_do_not_play() & players

	def _resolve_game_conflicts(self, i, game, games, conflicts):
		other_games = [g for j, g in enumerate(games) if j != i]

		for conflict in list(conflicts):
			power = game.get_power_by_player(conflict)

			if power is None:
				logger.warning(f"Game {i}: unassigned DNP player {conflict}")
				continue

			other_game = self._pick_other_game(other_games)
			self._execute_swap(i, game, other_game, conflict, power)

	def _execute_swap(self, i, game, other_game, conflict, power):
		match power:
			case "scrap":
				self._swap_scrap(i, game, other_game, conflict)

			case _ if power in self.config.powers:
				self._swap_power(i, game, other_game, conflict, power)

			case _:
				logger.warning(f"Game {i}: cannot resolve conflict {conflict}")

	def _swap_scrap(self, i, game, other_game, conflict):
		if not other_game.scrap_players:
			return

		conflict_player = self._get_player_from_scrap(conflict, game.scrap_players)
		game.scrap_players.remove(conflict_player)

		repl = other_game.scrap_players.pop()

		game.add_scrap(repl)
		other_game.add_scrap(conflict_player)

		logger.info(f"scrap swap '{conflict}' (Game {game.id}) ↔ '{repl.name} (Game {other_game.id})'")

	def _swap_power(self, i, game, other_game, conflict, power):
		player = game.assignments.get(power)
		other_player = other_game.assignments.get(power)

		if other_player:
			game.add_player(power, other_player)
			other_game.add_player(power, player)

			logger.info(
				f"power swap '{conflict}' (Game {game.id}) ↔ '{other_player.name}' (Game {other_game.id}) ({power})"
			)
			return

		# fallback to scrap
		if not other_game.scrap_players:
			return

		repl = other_game.scrap_players.pop()

		game.add_scrap(repl)
		other_game.add_player(power, player)

		logger.info(
			f"Game {i}: fallback swap '{conflict}' ↔ '{repl}' ({power})"
		)

	def _get_player_from_scrap(self, name: str, scraps):
		for player in scraps:
			if player.name == name:
				return player

	def _pick_other_game(self, other_games):
		return self.rng.choice(other_games)
