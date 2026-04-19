from typing import List

from allocator import utils
from allocator.domain.models import Game, Player
from allocator.allocators.base import BaseAllocator

class HungarianAllocator(BaseAllocator):
	pass

	@utils.timer
	def allocate(self, players: List[Player]) -> List[Game]:
		num_games = round(len(players) / len(self.config.powers))
		print(num_games)
		return []
		
