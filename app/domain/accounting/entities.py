# app/domain/accounting/entities.py
from uuid import UUID, uuid4
from abc import ABC
from datetime import datetime, date, timezone
from decimal import Decimal

from app.domain.accounting.enums import (
    EntryType,
    EntryStatus,
    MovementType,
    AccountType,
    AccountingType,
    AccountPurpose,
)
from app.domain.accounting.value_objects import Money, ExchangeRate
from app.domain.accounting.rules import ensure_exchange_rate


# Entidade Base
class EntityBase(ABC):    
    def __init__(self, *, id: UUID | None = None):
        self.id: UUID = id or uuid4() # identificador único da entidade
        self.created_at = datetime.now(timezone.utc) # data de criação
        self.updated_at = self.created_at # data de última atualização
        self.deleted_at: datetime | None = None # data de exclusão lógica


# Lançamento Contábil
class AccountingEntry(EntityBase):
    def __init__(
        self,
        *,
        user_id: UUID,
        sub_balance_id: UUID,
        entry_type: EntryType,
        money: Money,
        entry_date: date,
        base_currency: str,
        category_id: UUID,
        description: str | None = None,
        movement_type: MovementType = MovementType.NORMAL,
        exchange_rate: ExchangeRate | None = None,
        transfer_id: UUID | None = None,
        counterpart_id: UUID | None = None,
        tags: list[str] | None = None,
    ):
        # PRD: Data não pode ser futura
        if entry_date > date.today():
            raise ValueError("Entry date cannot be in the future")

        # PRD RF-PRO-101 → valida taxa se moeda ≠ base
        if money.currency != base_currency:
            ensure_exchange_rate(exchange_rate)

        self.user_id = user_id # proprietário do lançamento
        self.sub_balance_id = sub_balance_id # subsaldo afetado

        self.entry_type = entry_type # tipo do lançamento
        self.movement_type = movement_type # tipo de movimentação

        self.amount = money.amount # valor na moeda do lançamento
        self.currency = money.currency # moeda do lançamento
        self.base_currency = base_currency  # moeda base do sistema

        # RN-LANC-02 → taxa congelada
        # RN-LANC-03 → taxa usada no cálculo do valor base
        self.exchange_rate_used = (
            exchange_rate.rate if exchange_rate else None
        )

        # RN-LANC-03: valor convertido para moeda base
        self.base_amount = (
            money.amount * exchange_rate.rate
            if exchange_rate
            else money.amount
        )

        self.category_id = category_id # categoria do lançamento

         # descrição limitada a 255 caracteres
        self.description = description[:255] if description else None

        self.transfer_id = transfer_id # se for transferência, id do lançamento complementar
        self.counterpart_id = counterpart_id # id do lançamento contraparte (se aplicável)

        self.tags = tags[:10] if tags else [] # máximo de 10 tags por lançamento

        # PRD: lançamentos manuais iniciam CONFIRMADO
        self.status = EntryStatus.CONFIRMED # status do lançamento

        self.entry_date = entry_date # data do lançamento

    def confirm(self):
        self.status = EntryStatus.CONFIRMED
        self.updated_at = datetime.now(timezone.utc)


# Conta
class Account(EntityBase):
    def __init__(
        self,
        *,
        user_id: UUID,
        name: str,
        account_type: AccountType,
        accounting_type: AccountingType,
        purpose: AccountPurpose,
        default_currency: str | None = None,
    ):
        if account_type == AccountType.CASH and not default_currency:
            raise ValueError("Cash accounts must define a default currency")

        self.user_id = user_id # proprietário da conta
        self.name = name[: 100] # nome da conta limitado a 100 caracteres

        self.account_type = account_type # tipo da conta
        self.accounting_type = accounting_type # classificação contábil (macro)
        self.purpose = purpose # finalidade da conta

        # RN-CONTA-01
        self.allows_multiple_balances = account_type != AccountType.CASH # dinheiro em espécie não permite múltiplos saldos
        self.default_currency = default_currency # moeda padrão (se aplicável)

        self.active = True # conta ativa por padrão


    # RN-CONTA-05: verifica se pode adicionar subsaldo
    def can_add_sub_balance(self, currency: str, existing_currencies: set[str]):
        """
        RN-CONTA-05:
        Prevents duplicate currencies per account.
        """

        if not self.allows_multiple_balances:
            if existing_currencies:
                raise ValueError("Cash account supports only one sub-balance")

        if currency in existing_currencies:
            raise ValueError(
                f"Sub-balance with currency {currency} already exists for this account"
            )
        

# Subsaldo da Conta
class SubBalance(EntityBase):
    def __init__(
        self,
        *,
        account_id: UUID,
        currency: str,
        initial_balance: Decimal = Decimal("0"),
        minimum_balance: Decimal | None = None,
        maximum_balance: Decimal | None = None,
    ):
        if len(currency) != 3:
            raise ValueError("Currency must be ISO 4217 (3 characters)")

        self.account_id = account_id # conta associada
        self.currency = currency # moeda do subsaldo

        self.initial_balance = initial_balance # saldo inicial
        self.current_balance = initial_balance # saldo atual

        self.minimum_balance = minimum_balance # saldo mínimo permitido
        self.maximum_balance = maximum_balance # saldo máximo permitido

        self.active = True # subsaldo ativo por padrão

    # RN-CONTA-04: desativa subsaldo
    def deactivate(self, has_entries: bool):
        """
        RN-CONTA-04:
        Sub-balances with accounting entries cannot be deleted,
        only deactivated.
        """

        if not has_entries:
            # Mesmo sem lançamentos, o modelo opta por inativar (não excluir)
            self.active = False
        else:
            self.active = False

        self.updated_at = datetime.now(timezone.utc)
        self.deleted_at = datetime.now(timezone.utc)

    # Verifica se é possível realizar um saque sem violar o saldo mínimo
    def can_withdraw(self, amount: Decimal) -> bool:
        if self.minimum_balance is None:
            return True
        return (self.current_balance - amount) >= self.minimum_balance
    
    # Verifica se é possível realizar um depósito sem violar o saldo máximo
    def can_deposit(self, amount: Decimal) -> bool:
        if self.maximum_balance is None:
            return True
        return (self.current_balance + amount) <= self.maximum_balance

    # Atualiza o saldo atual
    def update_balance(self, entry_type: EntryType, amount: Decimal):
        """
        Applies an accounting entry to the sub-balance.

        PRD:
        - ENTRADA → soma
        - SAIDA → subtrai
        - RN-LANC-01: não violar saldo mínimo
        - RN-CONTA-03: respeitar limites
        """

        if entry_type == EntryType.EXPENSE:
            if not self.can_withdraw(amount):
                raise ValueError("Minimum balance violation")
            self.current_balance -= amount

        elif entry_type == EntryType.INCOME:
            self.current_balance += amount

        else:
            raise ValueError("Unsupported entry type")

        self.updated_at = datetime.now(timezone.utc)