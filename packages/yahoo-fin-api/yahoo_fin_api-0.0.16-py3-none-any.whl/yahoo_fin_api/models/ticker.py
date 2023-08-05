from __future__ import annotations
from dataclasses import dataclass
import yahoo_fin_api.utils as U
from yahoo_fin_api.models import (
	FinancialData, 
	SummaryDetail, 
	CashFlows, 
	BalanceSheets,
	IncomeStatements
)

@dataclass
class Ticker:

	symbol: str | None

	title: str | None

	financial_data: FinancialData | None

	summary_detail: SummaryDetail | None

	cashflows: CashFlows | None

	balance_sheets: BalanceSheets | None

	income_statements: IncomeStatements | None

	@staticmethod
	def from_dict(data: dict)-> Ticker | None:
		symbol = U.extract_key(data, "quoteType", "symbol")
		title = U.extract_key(data, "quoteType", "longName")
		if symbol is None:
			return None

		return Ticker(
			symbol,
			title,
			FinancialData.from_dict(data),
			SummaryDetail.from_dict(data),
			CashFlows.from_dict(data),
			BalanceSheets.from_dict(data),
			IncomeStatements.from_dict(data)
		)

