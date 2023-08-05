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

	symbol: str

	title: str

	financial_data: FinancialData

	summary_detail: SummaryDetail

	cashflows: CashFlows

	balance_sheets: BalanceSheets

	income_statements: IncomeStatements

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

