from allocator.config import Config
from allocator.allocators.base import BaseAllocator
from allocator.allocators.hungarian import HungarianAllocator


class AllocatorFactory:
	REGISTRY = {"hungarian": HungarianAllocator}

	@classmethod
	def create(cls, config: Config) -> BaseAllocator:
		alloc_type = config.allocation_method

		if alloc_type not in cls.REGISTRY:
			raise ValueError(f"Unknown loader type: {alloc_type}")

		return cls.REGISTRY[alloc_type](config)
