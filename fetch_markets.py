# fetch_markets.py — fetches live market data from Yahoo Finance using yfinance

import yfinance


MARKET_SYMBOLS = [
    {"symbol": "^GSPC",   "name": "S&P 500"},
    {"symbol": "^IXIC",   "name": "NASDAQ"},
    {"symbol": "^DJI",    "name": "Dow Jones"},
    {"symbol": "^RUT",    "name": "Russell 2K"},
    {"symbol": "^VIX",    "name": "VIX"},
    {"symbol": "^TNX",    "name": "10Y Treasury"},
    {"symbol": "BTC-USD", "name": "Bitcoin"},
    {"symbol": "GC=F",    "name": "Gold"},
    {"symbol": "CL=F",    "name": "WTI Oil"},
    {"symbol": "EURUSD=X","name": "EUR/USD"},
]


def get_vix_label(vix_price):
    """Return a fear label string based on VIX level."""
    if vix_price < 15:
        return "Low Fear"
    elif vix_price <= 25:
        return "Moderate Fear"
    else:
        return "High Fear"


def fetch_markets():
    """
    Fetch live prices and daily changes for key market indicators.
    Returns a list of dicts: {"name", "price", "change", "pct", "label"}.
    Returns empty list on any failure so the page still builds.
    """
    market_data = []
    try:
        for item in MARKET_SYMBOLS:
            try:
                ticker = yfinance.Ticker(item["symbol"])
                info = ticker.fast_info
                price = info.last_price
                prev_close = info.previous_close
                if price is None or prev_close is None:
                    continue
                change = price - prev_close
                pct = (change / prev_close) * 100 if prev_close else 0

                label = ""
                if item["symbol"] == "^VIX":
                    label = get_vix_label(price)

                market_data.append({
                    "name": item["name"],
                    "symbol": item["symbol"],
                    "price": price,
                    "change": change,
                    "pct": pct,
                    "label": label,
                })
            except Exception as error:
                print(f"Warning: could not fetch {item['symbol']} — {error}")
    except Exception as error:
        print(f"Warning: market data fetch failed — {error}")
        return []

    print(f"Fetched market data for {len(market_data)} symbols.")
    return market_data
