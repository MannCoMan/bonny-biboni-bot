import os
import re
import random
from pathlib import Path

from Core.constants import Const
from Core.typos import Dict
from Core.wrapper import Wrapper
from Core.sql import get_guilds


class Translate(Wrapper):
	consts = Const()
	guilds = Dict()

	def __init__(self, path):
		"""
		Args:
			path - path to "Mod" folder

		container dict contains all translations        - {lc-LC: data, ...}
		guild dict contains all guild and their Locales - {guild id: lc-LC}
		"""

		for guild in get_guilds():
			gid, locale, _ = guild
			self.guilds[gid] = locale

		for locale in os.listdir(path):
			# Catch filename "lc-LC.json"
			regex = re.compile(r"[a-z]{2}-[A-Z]{2}.*\.json")
			if re.search(regex, locale):
				key = locale.split(".")[-2]
				super().read(Path(path, locale), key=key)
				super().get()

		self.path = path		

	def get(self, *args, ctx=None, emoji=None, **kwargs):
		"""
		Get translated string
		
		Args:
			args (tuple) - mapped dict args
			ctx (object) - discord ctx (context)
			emoji (str)  - emoji for the string
			kwargs       - kwargs for string format
		Returns:
			formated string
			example: ":emoji: Formated string with args: {arg1} {arg2}"
		"""

		# Get locale (lc-LC) from `container`
		# container[guilds[gid]]
		locale = self.guilds.get(ctx.message.guild.id)
		if locale == self.consts.BOT_DEFAULT_LOCALE:
			string = args[-1]
		else:
			string = self.container.get(locale, *args)

		if isinstance(string, str):
			if emoji:
				emoji = ":{}:".format(emoji)
			
			if emoji is None:
				emoji = ""

			if emoji is True:
				emoji = random.choice(self.consts.EMOJI_RESPONSE)

			string = string.format(**kwargs)
			string = "{} {}".format(emoji, string)
			return string
		else:
			return string

	def getalias(self, key):
		"""
		Get alias(-es) from "Locales/aliases.json"
		
		Args:
			key (str) - key to get
		Returns:
			list of strings (alises)

		"""

		super().read(Path(self.path, "aliases.json"), key="aliases")
		return super().get("aliases", key)
		