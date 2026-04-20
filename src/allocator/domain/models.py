from typing import Set
from typing import Optional
from typing import Dict
from dataclasses import field
from dataclasses import dataclass

from allocator.config import Config

config = Config()

@dataclass
class Player:
	name: str
	timestamp: str
	preferences: Dict[str, int]
	reputation: int
	throw_pref: str

	do_not_play: Set[str] = field(default_factory=set)
	no_preference: bool = False

	def __str__(self):
		return f"Player(name={self.name}, reputation={self.reputation})"

	def __hash__(self):
		return hash(self.name)

	def __eq__(self, other):
		if not isinstance(other, Player):
			return False

		return self.name == other.name

@dataclass
class Game:
	id: int

	throwing_penalty: bool = False
	assignments: Dict[str, Optional[Player]] = field(default_factory=dict)
	scrap_players: Set[Player] = field(default_factory=set)

	def __str__(self) -> str:
		return f"Game(id={self.id}, players={len(self.assignments)}, scraps={len(self.scrap_players)}, throw_penalty={self.throwing_penalty})"

	def add_player(self, power: str, player: Player) -> None:
		self.assignments[power] = player

	def get_power_by_player(self, player: str | Player) -> Optional[str]:
		for power, p in self.assignments.items():
			if player == p:
				return power
			elif isinstance(player, str):
				if player == p.name:
					return power

		scraps = self.scrap_players
		if isinstance(player, str):
			scraps = set(map(lambda p: p.name, scraps))
		if player in scraps:
			return "scrap"

		return None

	def add_scrap(self, player: Player) -> None:
		self.scrap_players.add(player)

	def all_players(self) -> Set[Player]:
		players: Set[Player] = {p for p in self.assignments.values() if p}
		return players.union(self.scrap_players)

	def all_do_not_play(self) -> Set[str]:
		usernames = set()
		for p in self.all_players():
			usernames.update(p.do_not_play)		

		return usernames
