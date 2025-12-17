# app/domain/accounting/enums.py
from enum import Enum


# Enumeração para classificação contábil (Macro)
class AccountingType(str, Enum):
    """Classificação Contábil (Macro)"""
    ASSET = "ASSET"           # Ativo
    LIABILITY = "LIABILITY"   # Passivo
    EQUITY = "EQUITY"         # Patrimônio Líquido
    INCOME = "INCOME"         # Receita
    EXPENSE = "EXPENSE"       # Despesa

# Enumeração para natureza da conta
class AccountType(str, Enum):
    """Natureza do Recurso/Meio de Movimentação"""
    CASH = "CASH"             # Dinheiro em espécie
    BANK = "BANK"             # Conta Bancária Tradicional
    DIGITAL_WALLET = "DIGITAL_WALLET" # Carteira Digital (Ex: Wise, PayPal, PicPay)
    CREDIT_CARD = "CREDIT_CARD"       # Cartão de Crédito (Passivo)
    DEBIT_CARD = "DEBIT_CARD"         # Cartão de Débito

# Enumeração para finalidade da conta
class AccountPurpose(str, Enum):
    """Finalidade da Conta"""
    CHECKING = "CHECKING"     # Conta Corrente
    SAVINGS = "SAVINGS"       # Poupança
    INVESTMENT = "INVESTMENT" # Investimento
    PAYMENT = "PAYMENT"       # Pagamentos/Transacional (Comum em contas digitais)
    LOAN = "LOAN"             # Empréstimo / Financiamento


class EntryType(str, Enum):
    ENTRY = "ENTRY"   # ENTRADA
    EXIT = "EXIT"     # SAIDA

    # PRD RF-PRO-101 → ENTRADA / SAIDA


class EntryStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    SYNCED = "SYNCED"
    # PRD: lançamentos manuais iniciam como CONFIRMADO
    # PENDING: criado offline
    # CONFIRMED: salvo localmente
    # SYNCED: sincronizado com backend central (RNF-006)


class MovementType(str, Enum):
    NORMAL = "NORMAL"
    REVERSAL = "REVERSAL"
    ADJUSTMENT = "ADJUSTMENT"
    TRANSFER = "TRANSFER"
