from typing import Set
from typing import Optional
from typing import Dict
from dataclasses import field
from dataclasses import dataclass


@dataclass
class Player:
	name: str
	timestamp: str
	preferences: dict
	reputation: int
	throw_pref: str

	do_not_play: set[str] = field(default_factory=set)
	no_preference: bool = False


@dataclass
class Game:
	id: int

	assignments: Dict[str, Optional[str]] = field(default_factory=dict)
	scrap_players: Set[str] = field(default_factory=set)

	def add_player(self, power: str, player: str):
		self.assignments[power] = player

	def add_scrap(self, player: str):
		self.scrap_players.add(player)

	def all_players(self) -> Set[str]:
		players = {p for p in self.assignments.values() if p}
		return players + self.scrap_players
