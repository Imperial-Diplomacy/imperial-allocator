from allocator.config import Config
from allocator.allocators.base import BaseAllocator
from allocator.allocators.hungarian import HungarianAllocator


class AllocatorFactory:
	REGISTRY = {"csv": HungarianAllocator}

	@classmethod
	def create(cls, config: Config) -> BaseAllocator:
		# TODO: get type from config
		loader_type = config.loader_type

		if loader_type not in cls.REGISTRY:
			raise ValueError(f"Unknown loader type: {loader_type}")

		return cls.REGISTRY[loader_type](config)
