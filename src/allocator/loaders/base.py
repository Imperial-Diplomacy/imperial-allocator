from abc import ABC, abstractmethod
from typing import List

from allocator.config import Config
from allocator.domain.models import Player


class BaseLoader(ABC):
	def __init__(self, config: Config) -> None:
		self.config = config

	@abstractmethod
	def load(self) -> List[Player]:
		pass
