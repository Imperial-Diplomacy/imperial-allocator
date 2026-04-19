from dataclasses import field
from dataclasses import dataclass


@dataclass
class Config:
	rep_file: str = "data/Imperial Diplomacy Reputation - Master Sheet.csv"
	input_file: str = (
		"data/Imperial Diplomacy _ Beta 2.4 Signup (Responses) - Form responses 1.csv"
	)
	loader_method: str = "csv"
	allocation_method: str = "hungarian"

	powers: list[str] = field(default_factory=list)
	RANK_TO_WEIGHTS: dict[str, int] = field(default_factory=dict)
	WEIGHTS_TO_RANKS: dict[int, str] = field(default_factory=dict)

	seed: int = 42

	def __init__(self) -> None:
		self.RANK_TO_WEIGHTS = {"1st": 81, "2nd": 49, "3rd": 36, "4th": 16, "5th": 9}
		self.WEIGHTS_TO_RANKS = {v: k for k, v in self.RANK_TO_WEIGHTS.items()}
		self.powers = [
			"Abyssinia",
			"Ajuuraan",
			"Athapasca",
			"Austria",
			"Aymara",
			"Ayutthaya",
			"England",
			"France",
			"Guarani",
			"Inuit",
			"Kongo",
			"Mapuche",
			"Ming",
			"Mughal",
			"Netherlands",
			"Ottoman",
			"Poland-Lithuania",
			"Portugal",
			"Qing",
			"Russia",
			"Safavid",
			"Spain",
			"Sweden",
			"Ute-Shoshone",
			"Tokugawa",
		]
