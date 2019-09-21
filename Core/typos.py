import functools
import operator


class Dict(dict):
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

	def keyslist(self):
		return "".join(self.__dict__.keys())

	def valueslist(self):
		return "".join(self.__dict__.values())

	def pop(self, *args):
		return self.__dict__.pop(*args)

	def get(self, *args, default=None):
		try:
			return functools.reduce(operator.getitem, args, self.__dict__)
		except KeyError:
			raise KeyError("Wrong args: {}".format(*args))
			
	def set(self, *args):
		for k in args[:-2]:
			self = self[k]
		self[args[-2]] = args[-1]

	def __contains__(self, item):
		return item in self.__dict__

	def __iter__(self):
		return iter(self.__dict__)

	def __str__(self):
		return str(repr(self.__dict__))