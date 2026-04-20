import logging

from allocator import utils
from allocator.config import Config
from allocator.allocators.factory import AllocatorFactory
from allocator.balancers.dnp import DNPValidator
from allocator.loaders.factory import LoaderFactory
from allocator.output.allocations import AllocationsWriter
from allocator.output.donotplays import DoNotPlayListsWriter
from allocator.output.publications import PublicationsWriter

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

	groups = [("", players)]

	throwing_penalised = len(set(map(lambda p: p.throw_pref, players))) != 1
	if throwing_penalised:
		rest = set(players)

		# = identify clear preferences
		# filter out no_votes for holding
		no_votes = set(filter(lambda p: p.throw_pref == "No", rest))
		rest -= no_votes

		yes_votes = set(filter(lambda p: p.throw_pref == "Yes", rest))
		rest -= yes_votes

		# top up yes votes to make full games
		remaining = len(config.powers) - (len(yes_votes) % len(config.powers))
		yes_votes |= {rest.pop() for _ in range(remaining)}

		# fold no votes back in to the group
		rest |= no_votes
		groups = [("tp", yes_votes), ("np", rest)]

	for i, (prefix, group) in enumerate(groups):
		logger.info(f"=== Starting allocation for group {i} (prefix={prefix}) ===")

		alloc = AllocatorFactory.create(config)
		games = alloc.allocate(group)

		dnp_balancer = DNPValidator(config, players)
		games = dnp_balancer.balance(games)

		writers = [
			AllocationsWriter(config),
			DoNotPlayListsWriter(config),
			PublicationsWriter(config),
		]
		for writer in writers:
			writer.write(games, prefix=prefix)

if __name__ == "__main__":
	setup_logging()
	main()
