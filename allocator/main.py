import logging
from pathlib import Path

from allocator import utils
from allocator.config import Config
from allocator.allocators.factory import AllocatorFactory
from allocator.balancers.dnp import DNPValidator
from allocator.domain.models import Game
from allocator.loaders.factory import LoaderFactory
from allocator.output.allocations import AllocationsWriter
from allocator.output.donotplays import DoNotPlayListsWriter
from allocator.output.publications import PublicationsWriter

logger = logging.getLogger(__name__)


def setup_logging(log_filepath: str) -> None:
	logging.basicConfig(
		filename=log_filepath,
		level=logging.INFO,
		format="[%(asctime)s.%(msecs)03d] %(levelname)s | %(message)s",
		datefmt="%Y/%m/%d %H:%M:%S",
	)

	logging.getLogger().addHandler(logging.StreamHandler())


@utils.timer
def main() -> None:
	config = Config()
	setup_logging(config.out_dir + "/stdout.log")

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

	final_players = set()
	for i, (prefix, group) in enumerate(groups):
		logger.info(f"=== Starting allocation for group {i} (prefix={prefix}) ===")

		alloc = AllocatorFactory.create(config)
		games: list[Game] = alloc.allocate(group)

		dnp_balancer = DNPValidator(config, players)
		games = dnp_balancer.balance(games)

		for g in games:
			players = set(g.assignments.values()) | g.scrap_players
			final_players |= (players)

		writers = [
			AllocationsWriter(config),
			DoNotPlayListsWriter(config),
			PublicationsWriter(config),
		]
		for writer in writers:
			writer.write(games, prefix=prefix)

	final_player_file = Path(config.out_dir) / "all_players.txt"
	final_player_file.touch(exist_ok=True)
	with open(final_player_file, "w") as f:
		player_names = list(map(lambda p: p.name, final_players))
		f.write("\n".join(player_names))

if __name__ == "__main__":
	main()
