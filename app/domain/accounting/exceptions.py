# app
class AccountingDomainError(Exception):
    """Base class for accounting domain errors"""
    pass


class MissingExchangeRate(AccountingDomainError):
    """Raised when currency conversion rate is missing"""
    pass


class InsufficientBalance(AccountingDomainError):
    """Raised when balance would fall below minimum"""
    pass


class InvalidSubBalanceSelection(AccountingDomainError):
    """Raised when SubBalance is required but not provided"""
    pass
