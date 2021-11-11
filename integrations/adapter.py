from typing import List, Dict


class Site:
	name: str

	def __init__(self, name):
		self.name = name

	def check(self):
		pass


class Service:
	sites: Dict[str, Site]

	def __init__(self):
		pass
