DROP TABLE IF EXISTS stock_tickers CASCADE;
DROP TABLE IF EXISTS stock_data CASCADE;
DROP TABLE IF EXISTS composite_tickers CASCADE;
DROP TABLE IF EXISTS composite_data CASCADE;

CREATE TABLE stock_tickers (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE stock_data (
    id SERIAL PRIMARY KEY,
    stock_ticker_id INT NOT NULL REFERENCES stock_tickers(id),
    open_price NUMERIC(2,0) NOT NULL,
    close_price NUMERIC(2,0) NOT NULL,
    date DATE NOT NULL
);

CREATE TABLE composite_tickers (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE composite_data (
    id SERIAL PRIMARY KEY,
    composite_ticker_id INT NOT NULL REFERENCES composite_tickers(id),
    open_price NUMERIC (2,0) NOT NULL,
    close_price NUMERIC (2,0) NOT NULL,
    date DATE NOT NULL
);
