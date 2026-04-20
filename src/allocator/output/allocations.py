from pathlib import Path
from allocator.output.base import BaseWriter

class AllocationsWriter(BaseWriter):
	def __init__(self, config):
		self.config = config

	def write(self, games, *, prefix="") -> None:
		out_path = Path(self.config.out_dir) 
		out_path.mkdir(exist_ok=True)

		out_path = out_path / f"{prefix}allocations.txt"
		out_path.touch(exist_ok=True)
		with open(out_path, "w") as f:
			for i, g in enumerate(games):
				f.write(f"===== Game {i} allocations =====\n")

				ranked_powers = [name for name in g.assignments if g.assignments[name] is not None]

				scrap_powers = sorted(set(self.config.powers) - set(g.assignments.keys()))
				scrap_powers = " ".join([f"@{power}" for power in scrap_powers])

				f.write(f"Scrap Powers: {scrap_powers}\n")
				f.write("Scrap Players:\n")
				for scrapper in g.scrap_players:
					f.write(f"- @{scrapper.name}\n")

				f.write("Allocated Players:\n")
				for power in ranked_powers:
					player = g.assignments[power]
					f.write(f"- @{power} - @{player.name}({player.name})\n")
