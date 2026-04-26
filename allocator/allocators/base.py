from abc import ABC, abstractmethod
from typing import List

from allocator.domain.models import Game, Player
from allocator.config import Config


class BaseAllocator(ABC):
	def __init__(self, config: Config):
		self.config = config

	@abstractmethod
	def allocate(self, players: List[Player]) -> List[Game]: ...
