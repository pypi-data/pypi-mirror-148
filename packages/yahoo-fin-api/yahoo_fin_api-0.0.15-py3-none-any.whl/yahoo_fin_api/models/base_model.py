from datetime import datetime

class Model:

	def fmt_end_date(self)-> str:
		ts = datetime.fromtimestamp(self.end_date)
		return ts.strftime("%Y-%m-%d")