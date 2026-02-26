# Spike: Trading Strategies & Rotations

**Objective:** Define the specific trading setups AlphaOracle should look for to maximize returns over a buy-and-hold SPY strategy, focusing on a few trades per month (swing trading, ETFs, options).

## 1. Sector Rotation Strategy
The core driver of outperformance. Markets move in cycles; money flows out of one sector and into another based on the economic environment.

*   **The Framework (Business Cycle):**
    *   *Early Recovery:* Financials, Consumer Discretionary, Technology.
    *   *Mid Cycle:* Industrials, Materials, Tech.
    *   *Late Cycle:* Energy, Healthcare, Consumer Staples (Defensive).
    *   *Recession:* Utilities, Staples, Bonds.
*   **LLM Task:** The "Macro Strategist" LLM must analyze recent news and the relative strength of sector ETFs (XLK for Tech, XLF for Financials, XLE for Energy) against SPY to identify where money is rotating.

## 2. Swing Trading Setups (Mean Reversion & Breakouts)
Since the goal is a few trades a month, we are looking for multi-day to multi-week moves.

*   **Mean Reversion (The "Bounce"):**
    *   *Setup:* A fundamentally strong stock or ETF (e.g., SPY, QQQ) drops rapidly to a major support level (e.g., the 200-day SMA or the lower Bollinger Band) and RSI drops below 30.
    *   *Action:* Buy shares or long Call options expecting a reversion to the 20-day moving average.
*   **Volatility Contraction (The "Squeeze"):**
    *   *Setup:* Bollinger Bands narrow significantly. Price consolidates in a tight range on low volume.
    *   *Action:* Wait for the breakout. Buy Calls or shares on a high-volume break above resistance.

## 3. Options Strategies for Yield and Leverage
Options should be used carefully to enhance returns or hedge risk, not for reckless gambling.

*   **Cash-Secured Puts (Income Generation):**
    *   *Strategy:* Sell puts on stocks/ETFs we *want* to own, at a price we are happy to pay (e.g., 5% below current price).
    *   *LLM Prompting:* Identify high-quality stocks in our watchlist that have elevated implied volatility (higher premiums) but are near strong support levels.
*   **Covered Calls (Yield Enhancement):**
    *   *Strategy:* Sell upside calls against existing positions in `portfolio.csv` to generate income, especially during "Bull Quiet" or "Bear Quiet" regimes.
*   **Directional Plays (Long Calls/Puts):**
    *   *Strategy:* Use to capitalize on high-conviction swing setups with defined risk. Buy SPY Puts to hedge the portfolio if the LLMs detect an impending high-volatility event.

## 4. Prompting the Portfolio Manager LLM
The final LLM must be given strict rules:
1.  **Protect Capital First:** If the Market Regime is "Bear Volatile," default to raising cash or hedging.
2.  **Require Consensus:** For a "High Conviction" buy, at least two of the subordinate LLMs (e.g., Technical Analyst and Macro Strategist) must agree on the setup.
3.  **Specify Exits:** Every recommendation must include an invalidation level (stop loss) and a target (take profit). "Buy SPY at 500. Stop loss if it closes below 490. Target 520."