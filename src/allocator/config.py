from dataclasses import field
from dataclasses import dataclass

@dataclass
class Config:
	rep_file: str = "data/Imperial Diplomacy Reputation - Master Sheet.csv"
	input_file: str = "data/Imperial Diplomacy _ Beta 2.4 Signup (Responses) - Form responses 1.csv"
	loader_type: str = "csv"

	powers: list = field(default_factory=list)
	RANK_TO_WEIGHTS: dict = field(default_factory=dict)

	seed: int = 42

	def __init__(self):
		self.RANK_TO_WEIGHTS = {"1st": 36, "2nd": 25, "3rd": 16, "4th": 9, "5th": 4}
		self.powers = [
			"Abyssinia",
			"Ajuuraan"
			"Athapasca",
			"Austria"
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
			"Tokugawa"
		]

