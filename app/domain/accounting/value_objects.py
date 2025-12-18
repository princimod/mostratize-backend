# app/domain/accounting/value_objects.py
from decimal import Decimal, ROUND_HALF_UP

# Money
class Money:
    __slots__ = ("amount", "currency")

    def __init__(self, amount: Decimal, currency: str):
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")

        if len(currency) != 3:
            raise ValueError("Invalid currency code (ISO 4217)")

        self.amount = amount.quantize(
            Decimal("0.0001"), rounding=ROUND_HALF_UP
        )
        self.currency = currency.upper()


# ExchangeRate: 
class ExchangeRate:
    def __init__(self, rate: Decimal):
        if rate <= 0:
            raise ValueError("Invalid exchange rate")

        self.rate = rate.quantize(
            Decimal("0.000001"), rounding=ROUND_HALF_UP
        )
