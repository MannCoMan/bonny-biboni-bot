import collections
import json

from pathlib import Path
from Core.Types import Dict


class Wrapper:
	""" JSON Wrapper """

	container = Dict()

	def __init__(self, path):
		super(Wrapper, self).__init__()
		self.path = Path(path)

	def read(self, path=None, container=None, key=None):
		if path:
			path = Path(path)
		else:
			path = self.path

		if not container:
			container = self.container
			
		with open(path, "r", encoding="utf-8") as file:
			if key:
				if key in container:
					container[key].update(json.load(file))
				else:
					container[key] = json.load(file)					
			else:
				container.update(json.load(file))

	def _update(self, dicto, dictu):
		for k, v in dictu.items():
			if isinstance(v, collections.Mapping):
				dicto[k] = self._update(dicto.get(k, {}), v)
			else:
				dicto[k] = v
		return dicto

	def get(self, *args):
		return self.container.get(*args)

	def save(self, *args, file=None, indent=None, check=True):
		"""
		save - method for saving data to json file
		
		Args:
			file   - file path for another file
			indent - json-file indent
			check  - check hash sum difference

		How to use:
			# save it
			myDict.save("section", "key", "value") # save it
		
			# save it (with arguments)
			myDict.save("section", "key", "value", file="backup.json", indent=3)
		"""

		if not indent:
			indent = 4
		
		self.container.set(*args)

		with open(self.path, "wb") as file:
			data = json.dumps(self.container, indent=indent, ensure_ascii=False).encode("utf-8")
			file.write(data)

	def rawsave(self, data: Dict, file=None, indent=None, check=True):
		"""
		rawsave - method for updating json file from raw dict

		Args:
			data   - raw dictionary
			file   - file path for another file
			indent - json-file indent

		How to use:
			# save it
			myDict.rawsave({"section": {"key": "value"}})

			# save it (with parameters)
			myDict.rawsave({"section": {"key": "value"}}, file="backup.json", indent=3)
		"""

		if not file:
			file = self.path

		if not indent:
			indent = 4

		update = self._update(self.container.get(), data)
		with open(self.path, "wb") as file:
			data = json.dumps(update, indent=indent, ensure_ascii=False).encode("utf-8")
			file.write(data)