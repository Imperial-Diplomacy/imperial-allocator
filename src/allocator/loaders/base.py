from abc import ABC, abstractmethod
from typing import List

from allocator.domain.models import Player


class BaseLoader(ABC):
	def __init__(self, config):
		self.config = config

	@abstractmethod
	def load(self) -> List[Player]:
		pass
