import collections
import functools
import inspect
import json
import operator
import os

from Core.Settings import BOT_LOCALE


class Dict(dict):
	# TODO: add comp. function with "clone" feature
	def __setitem__(self, key, item):
		self.__dict__[key] = item

	def __getitem__(self, key):
		return self.__dict__[key]

	def __repr__(self):
		return repr(self.__dict__)

	def __len__(self):
		return len(self.__dict__)

	def __delitem__(self, key):
		del self.__dict__[key]

	def clear(self):
		return self.__dict__.clear()

	def delete(self, key):
		_r = self.get()[key]
		return _r

	def copy(self):
		return self.__dict__.copy()

	def has_key(self, k):
		return k in self.__dict__

	def update(self, *args, **kwargs):
		return self.__dict__.update(*args, **kwargs)

	def keys(self):
		return self.__dict__.keys()

	def values(self):
		return self.__dict__.values()

	def items(self):
		return self.__dict__.items()

	def keysList(self):
		return "".join(self.__dict__.keys())

	def valuesList(self):
		return "".join(self.__dict__.values())

	def pop(self, *args):
		return self.__dict__.pop(*args)

	def get(self, *args, default=None):
		try:
			return functools.reduce(operator.getitem, args, self.__dict__)
		except (KeyError, AttributeError, TypeError):
			# Will return default value or empty "Dict" class
			return default if default is not None else Dict() 

	def __contains__(self, item):
		return item in self.__dict__

	def __iter__(self):
		return iter(self.__dict__)

	def __str__(self):
		return str(repr(self.__dict__))


class Wrapper(Dict):
	"""
	* Supports dicts or file paths 
	* Wrapper({"main": "value"})
	* Wrapper("Path/File.json")
	"""

	__slots__ = "file"

	def __init__(self, file):
		super(Wrapper, self).__init__()
		self.file = file

		with open(self.file, "r", encoding="utf-8") as data:
			self.update(json.load(data))

	def __update(self, dicto, dictu):
		for k, v in dictu.items():
			if isinstance(v, collections.Mapping):
				dicto[k] = self.__update(dicto.get(k, {}), v)
			else:
				dicto[k] = v
		return dicto

	def remove(self, key):
		removed = self.get()
		del removed[key]
		self.save(removed)

	# save(<updated dict>) 
	def save(self, dict_, indent=4):
		u = self.__update(self.get(), dict_)
		with open(self.file, "wb") as file:
			data = json.dumps(u, indent=indent, ensure_ascii=False).encode("utf8")
			file.write(data)


class DictWrapper(Dict):
	"""
	How to use:
	* DictWrapper(DictObject)         - Dict object type
	* DictWrapper({"key": "value"})   - raw dict type
	* DictWrapper('{"key": "value"}') - string type dict
	"""

	__slots__ = "data"

	def __init__(self, data=None):
		super(DictWrapper, self).__init__()
		if isinstance(data, (dict, Dict)):
			self.data = self.update(data)

		if isinstance(data, str):
			self.data = json.loads(data)
			self.data = self.update(self.data)


class Translate(Wrapper):
	def __init__(self, *path):
		super().__init__(os.path.join(*path, f"{BOT_LOCALE}.json"))

	@property
	def message_patterns(self):
		return self.get("message-patterns")