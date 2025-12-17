# 
from decimal import Decimal
from app.domain.accounting.exceptions import (
    MissingExchangeRate,
    InsufficientBalance,
)


def ensure_exchange_rate(rate):
    # PRD RF-PRO-101 → erro se moeda ≠ moeda base sem taxa
    if rate is None:
        raise MissingExchangeRate(
            "Exchange rate not configured for this currency"
        )


def ensure_minimum_balance(
    current_balance: Decimal,
    expense_amount: Decimal,
    minimum_balance: Decimal | None,
):
    # RN-LANC-01
    if minimum_balance is not None:
        if current_balance - expense_amount < minimum_balance:
            raise InsufficientBalance(
                f"Minimum balance {minimum_balance} cannot be violated"
            )
