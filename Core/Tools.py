import json
import re

from functools import reduce
from operator import getitem


class Wrapper:
	# Init json library and read json file
	def __init__(self, file=None):
		self.file = file
		try:
			with open(file, 'r', encoding='utf-8') as data:
				self.js = json.load(data)
		except Exception:
			pass

	# Extension: "*.json"
	# Catching: section and section's key
	# Returning: value
	# You actually can use digits instead of hex values
	# conv  - output value type
	# case  - string case
	def gv(self, *args, conv=str, case=0, scope={}):
		col = []
		for i in range(len(args)):
			if isinstance(args[i], (list, tuple)):
				obj = reduce(getitem, args[i], self.js)
				obj = self.convert_value(obj, conv)
				obj = self.set_case(obj, case)
				col.append(obj)
				# col.append(self.set_case(self.convert_value(reduce(getitem, args[i], self.js), conv)), case)
			else:
				obj = reduce(getitem, args, self.js)
				obj = self.convert_value(obj, conv)
				obj = self.set_case(obj, case)
				return obj
				# return self.set_case(self.convert_value(reduce(getitem, args, self.js), conv), case)
		return col

	def convert_value(self, value, vt):
		if vt == hex:
			return hex(int(value, 16))
		
		if vt == str:
			return value
		
		if vt == int:
			value = int(value[2:], 16)
			return value

	def set_case(self, value, case=0):
		if case == 0:
			return value

		if case == 1:
			return value.lower()
		
		if case == 2:
			return value.upper()

		if case == 3:
			return value.capitalize()

	# This code not working inside "save" function, because... I dunno
	def __update(self, dicto, dictu):
		for k, v in dictu.items():
			if isinstance(v, collections.Mapping):
				dicto[k] = self.__update(dicto.get(k, {}), v)
			else:
				dicto[k] = v

		return dicto

	# File: "configs/config.json"
	# Do: overwrite config file ( save('section name', {'key': 'value', ...}) )
	def save(self, dicto, dictu, indent=4):
		self.js = self.__update(dicto, dictu)
		with open(self.file, 'wb') as file:
			data = json.dumps(self.js, indent=indent, ensure_ascii=False).encode('utf8')
			file.write(data)