import json
from pathlib import Path
from yahoo_fin_api.cache.base_cache import BaseCache

class FileCache(BaseCache):

	def __init__(self, output_dir: str)-> None:
		super().__init__()

		Path(output_dir).mkdir(parents=True, exist_ok=True)

		self.output_dir = output_dir

	def __cache_file(self, symbol: str)-> str:
		return f"{self.output_dir}/{symbol}.json"

	def is_cached(self, symbol: str)-> bool:
		symbol = symbol.upper()
		return Path(self.__cache_file(symbol)).is_file()

	def from_cache(self, symbol: str)-> dict:
		symbol = symbol.upper()
		with open(self.__cache_file(symbol), "r") as file:
			return json.loads(file.read())

	def to_cache(self, symbol: str, body: dict)-> None:
		symbol = symbol.upper()
		with open(self.__cache_file(symbol), "w") as file:
			file.write(json.dumps(body))

	def clear_cache(self, symbol: str)-> bool:
		symbol = symbol.upper()
		if self.is_cached(symbol) is False:
			return True

		Path(self.__cache_file(symbol)).unlink()

		return True

