import logging
import pandas as pd
import re
from typing import Dict, List, Optional

from allocator import utils
from allocator.config import Config
from allocator.loaders.base import BaseLoader
from allocator.domain.models import Player

logger = logging.getLogger(__name__)


USERNAME_TEXT = "Discord Username"
NO_PREFERENCE_TEXT = "Select Here If You Have No Power Preferences"
DNP_ROW_TEXT = "Are there any people you refuse to play with? (This will be shared with the Admins and your GM Team.)"
THROWING_PENALISED_TEXT = """Would you like to be placed in a game where throwing is penalized?\n\nThrowing would be determined as "Moving with the intention to end the game by providing supply centers to another power or to eliminate your power ahead of when it would naturally cease to exist." Penalties would include reputation (as if you had left the game) and loss of IDR invested in the game. Whether you threw would be determined by the GM and Angel (who would both have to agree you threw) and by a panel of 3 Admins, of which 2 would need to agree you threw.\n"""


class CSVSignupsLoader(BaseLoader):
	def __init__(self, config: Config):
		self.config = config

		self.filepath = config.input_file
		self.rep_filepath = config.rep_file

		self.reputations = self._fetch_reputations()

	def _fetch_reputations(self) -> Dict[str, int]:
		reputations = {}

		if self.rep_filepath is None:
			return reputations

		df = pd.read_csv(self.rep_filepath, skipinitialspace=True)
		for name, val in df.iloc[:, :2].itertuples(index=False, name=None):
			if pd.isna(name):
				continue

			if pd.isna(val):
				val = 10

			reputations[name.lower()] = int(val)

		return reputations

	@utils.timer
	def load(self) -> List[Player]:
		df = pd.read_csv(self.filepath, skipinitialspace=True)
		df = self._prepare_data(df)

		players = {}
		for _, row in df.iterrows():
			player = self._parse_player(row, df.columns)
			if player:
				players[player.name] = player

		logger.info(
			f"Identified {len(players)} valid signups from file: '{self.filepath}'"
		)
		return list(players.values())

	def _prepare_data(self, df: pd.DataFrame) -> pd.DataFrame:
		COUNTRY_RANK_COL_RE = re.compile(r"Rank Your Country Choices \[(.*)\]")
		country_columns = {}

		for c in df.columns:
			match = COUNTRY_RANK_COL_RE.match(c)
			if match:
				country_columns[c] = match.group(1)

		df = df.rename(columns={k: v for k, v in country_columns.items()})

		return df

	def _parse_player(self, row, columns) -> Optional[Player]:
		username = row.get(USERNAME_TEXT, "").lower().strip()
		if username == "":
			return None

		if username.startswith("@"):
			username = username[1:]

		preferences, scrap = self._fetch_preferences(row, columns)
		do_not_play = self._fetch_do_not_play(row, columns)
		reputation = self.reputations.get(username, None)
		if reputation is None:
			default = 10
			logger.warning(
				f"Could not find a reputation value for {username}: Assuming '{default}'"
			)
			reputation = default
		elif reputation <= -10:
			logger.warning(
				f"Ignored signup for user '{username}': Below threshold to play (Reputation={reputation})"
			)
			return None
		elif reputation < 0:
			logger.warning(
				f"Ignored signup for user '{username}': Below threshold to sign up (Reputation={reputation})"
			)
			return None

		throw_preference = row.get(THROWING_PENALISED_TEXT, None)
		if throw_preference is None:
			default = "I have no preference either way"
			logger.warning(
				f"Could not identify a throw preference for user '{username}': Assuming '{default}'"
			)
			throw_preference = default

		player = Player(
			name=username,
			timestamp=row.get("Timestamp"),
			reputation=reputation,
			preferences=preferences,
			no_preference=scrap,
			throw_pref=throw_preference,
			do_not_play=do_not_play,
		)

		return player

	def _fetch_preferences(self, row, columns) -> tuple[Dict[str, int], bool]:
		preferences = {}

		for col in columns:
			value = row[col]
			if value in self.config.RANK_TO_WEIGHTS:
				preferences[col] = self.config.RANK_TO_WEIGHTS[value]

		preferences = dict(
			sorted(preferences.items(), key=lambda p: p[1], reverse=True)
		)
		return preferences, row.get(NO_PREFERENCE_TEXT) == "No Preferences"

	def _fetch_do_not_play(self, row, columns):
		dnp = row.get(DNP_ROW_TEXT)
		if pd.isna(dnp):
			return {}

		dnp_players = {x.strip().lower() for x in dnp.split(",")}
		return dnp_players
