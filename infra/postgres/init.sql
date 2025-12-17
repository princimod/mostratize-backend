-- Forçar UTC (financeiro exige)
SET TIME ZONE 'UTC';

-- Extensões obrigatórias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Schema principal do sistema
CREATE SCHEMA IF NOT EXISTS core;
CREATE SCHEMA IF NOT EXISTS accounting;
CREATE SCHEMA IF NOT EXISTS currency;
CREATE SCHEMA IF NOT EXISTS planning;
CREATE SCHEMA IF NOT EXISTS audit;

-- Garantir permissões
GRANT ALL PRIVILEGES ON SCHEMA core TO mostratize_admin;
GRANT ALL PRIVILEGES ON SCHEMA audit TO mostratize_admin;
GRANT ALL PRIVILEGES ON SCHEMA accounting TO mostratize_admin;
GRANT ALL PRIVILEGES ON SCHEMA currency TO mostratize_admin;
GRANT ALL PRIVILEGES ON SCHEMA planning TO mostratize_admin;

-- Exemplo de tabela base
CREATE TABLE accounting.accounts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(30) NOT NULL,
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE currency.exchange_rates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    from_currency VARCHAR(3) NOT NULL,
    to_currency VARCHAR(3) NOT NULL,
    rate DECIMAL(18, 6) NOT NULL,
    effective_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE planning.budgets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    amount DECIMAL(18, 2) NOT NULL,
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE audit.logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID,
    action VARCHAR(100) NOT NULL,
    entity VARCHAR(100) NOT NULL,
    entity_id UUID,
    timestamp TIMESTAMP DEFAULT now(),
    details JSONB
);