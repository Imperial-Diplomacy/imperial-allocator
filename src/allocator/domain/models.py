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

	def __hash__(self):
		return hash(self.name)

	def __eq__(self, other):
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

	def add_scrap(self, player: Player) -> None:
		self.scrap_players.add(player)

	def all_players(self) -> Set[Player]:
		players: Set[Player] = {p for p in self.assignments.values() if p}
		return players.union(self.scrap_players)
