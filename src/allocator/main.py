import logging

from allocator import utils
from allocator.config import Config
from allocator.allocators.factory import AllocatorFactory
from allocator.loaders.factory import LoaderFactory

logger = logging.getLogger(__name__)


def setup_logging() -> None:
	logging.basicConfig(
		level=logging.INFO,
		format="[%(asctime)s.%(msecs)03d] %(levelname)s | %(message)s",
		datefmt="%Y/%m/%d %H:%M:%S",
	)


@utils.timer
def main() -> None:
	config = Config()

	loader = LoaderFactory.create(config)
	players = loader.load()

	alloc = AllocatorFactory.create(config)
	games = alloc.allocate(players)

	logger.critical(games)

if __name__ == "__main__":
	setup_logging()
	main()
