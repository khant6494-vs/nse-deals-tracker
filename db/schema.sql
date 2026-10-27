-- Schema for the NSE Deals Tracker. Loaded automatically by docker-compose
-- on first start (docker-entrypoint-initdb.d), or run manually:
--   mysql -u nse_user -p nse_deals < db/schema.sql

CREATE TABLE IF NOT EXISTS deals (
  id         INT AUTO_INCREMENT PRIMARY KEY,
  deal_id    VARCHAR(64)    NOT NULL DEFAULT '',
  deal_date  DATE           NOT NULL,
  symbol     VARCHAR(64)    NOT NULL,
  client     VARCHAR(255)   NOT NULL,
  buy_sell   VARCHAR(8)     NOT NULL,          -- BUY / SELL
  quantity   BIGINT         NOT NULL,
  price      DECIMAL(14,2)  NOT NULL,
  value_cr   DECIMAL(14,2)  NOT NULL,          -- quantity * price / 1e7
  deal_type  VARCHAR(16)    NOT NULL,          -- bulk / block / short

  -- INSERT IGNORE in the fetch/merge scripts relies on this to skip duplicates
  UNIQUE KEY uq_deal (deal_date, symbol, client, buy_sell, quantity, price, deal_type),
  KEY idx_date   (deal_date),
  KEY idx_symbol (symbol),
  KEY idx_client (client)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
