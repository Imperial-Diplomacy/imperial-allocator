from allocator.config import Config
from allocator.loaders.base import BaseLoader
from allocator.loaders.csv_loader import CSVSignupsLoader


class LoaderFactory:
	REGISTRY = {"csv": CSVSignupsLoader}

	@classmethod
	def create(cls, config: Config) -> BaseLoader:
		loader_type = config.loader_method

		if loader_type not in cls.REGISTRY:
			raise ValueError(f"Unknown loader type: {loader_type}")

		return cls.REGISTRY[loader_type](config)
