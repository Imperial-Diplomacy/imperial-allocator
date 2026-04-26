from pathlib import Path
from allocator.output.base import BaseWriter


class PublicationsWriter(BaseWriter):
	def __init__(self, config):
		self.config = config

	def write(self, games, *, prefix="") -> None:
		out_path = Path(self.config.out_dir)
		out_path.mkdir(exist_ok=True)

		out_path = out_path / f"{prefix}publications.txt"
		out_path.touch(exist_ok=True)
		with open(out_path, "w") as f:
			for i, g in enumerate(games):
				f.write(f"===== Game {i} =====\n")
				for player in g.all_players():
					f.write(f"- @{player.name}\n")
