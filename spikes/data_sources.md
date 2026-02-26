# Spike: Data Sources Evaluation

**Objective:** Identify reliable, cost-effective (preferably free for low volume) APIs to fetch end-of-day stock prices, options data, technical indicators, and financial news.

## 1. Stock Prices & Volume
We need daily end-of-day (EOD) data for a custom watchlist and major indices.

*   **yfinance (Python Library):**
    *   *Pros:* Free, easy to use, pulls directly from Yahoo Finance. Returns Pandas DataFrames. Good for historical data and current EOD.
    *   *Cons:* Unofficial API; can break if Yahoo changes their site structure. Rate limits apply if abused, but fine for a daily run.
    *   *Verdict:* **Primary Choice** for MVP.

*   **Alpaca Market Data API:**
    *   *Pros:* Official, robust API. Generous free tier for basic market data. Built for algorithmic trading.
    *   *Cons:* Requires account setup and API keys.
    *   *Verdict:* Excellent backup or upgrade path.

*   **Polygon.io / Alpha Vantage:**
    *   *Pros:* High quality, institutional grade.
    *   *Cons:* Free tiers are often very restrictive (e.g., 5 API calls per minute).

## 2. Options Data (Crucial for Volatility Analysis)
We need implied volatility and basic options chain data.

*   **yfinance:**
    *   *Pros:* Can fetch basic options chains `ticker.options`.
    *   *Cons:* Data can be delayed or incomplete. Implied volatility calculations might be rudimentary.
*   **Options Profit Calculator / CBOE free data:** Hard to automate via simple API.
*   *Verdict:* Stick to `yfinance` for basic options volume/open interest for MVP.

## 3. Financial News & Sentiment
We need context on why the market is moving.

*   **NewsAPI (newsapi.org):**
    *   *Pros:* Broad coverage, easy to search by keyword (e.g., "Federal Reserve", "SPY").
    *   *Cons:* Free tier is delayed (often 24h) and limited to top headlines for recent news.
*   **Finnhub / Polygon News:**
    *   *Pros:* Specifically tailored for financial news.
    *   *Cons:* Cost constraints.
*   **Yahoo Finance News (via yfinance or feedparser):**
    *   *Pros:* Free, relevant to specific tickers.
    *   *Verdict:* **Primary Choice.** RSS feeds or the `yfinance.Ticker().news` method.

## 4. Macroeconomic Events
Need to know when Fed meetings or CPI data releases occur.

*   **ForexFactory Calendar (Scraping/RSS):** Highly reliable for macro events.
*   **FRED (Federal Reserve Economic Data) API:**
    *   *Pros:* Official, free API for all economic data (inflation, interest rates, etc.).
    *   *Verdict:* **Primary Choice** for macro indicators.

## Summary Recommendation for MVP
Use `yfinance` for all stock price, volume, and basic options data. Use `yfinance` news and `feedparser` on financial RSS feeds for sentiment. Use the `FRED API` for major economic indicators. This stack is entirely free and robust enough for a daily cron job.