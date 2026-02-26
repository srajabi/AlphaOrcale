# Automated AI Investment Analyst & Portfolio Manager

## Proposed System Names
- **AlphaOracle:** Emphasizes predictive capabilities and generating alpha.
- **MarketMind Nexus:** Highlights the multi-LLM consensus approach.
- **SwingStream AI:** Focuses on the swing-trading / rotation strategy.
- **ThesisDriven:** Focuses on grounding the AI in your specific investment thesis.
- **QuantConsensus:** Blends quantitative data with LLM consensus.

## High-Level Architecture
The system is a static site generated daily via GitHub Actions, driven by a multi-agent LLM pipeline.

1.  **State/Input Repository:** 
    *   `portfolio.csv`: Current holdings, cost basis, quantities.
    *   `watchlist.csv`: Tickers of interest.
    *   `thesis/`: Markdown files detailing macro views, vertical interests (e.g., AI, biotech), and seasonality rules (e.g., "Midterm summer dips").
2.  **Data Ingestion Engine (Python Scripts):**
    *   Pulls end-of-day (or pre-market) price data, volume, and technical indicators (RSI, MACD, Moving Averages).
    *   Scrapes/pulls financial news, global market indices (e.g., Nikkei, Hang Seng for weekend Asian market action), and macroeconomic events (fed rates, CPI dates).
3.  **The "Mixture of Experts" LLM Pipeline:**
    *   **Context Builder:** Aggregates the inputs (CSV + Thesis + Data) into a massive, structured context prompt.
    *   **Independent Analysts:** The context is sent to multiple distinct LLMs (e.g., Gemini 1.5 Pro, DeepSeek, Claude 3.5 Sonnet, GPT-4o).
    *   **Output:** Each model generates an independent daily report (e.g., `reports/2026-02-25_gemini.md`).
4.  **The Portfolio Manager (Final LLM):**
    *   A final LLM (the smartest/most capable available, or one specifically prompted with a "Portfolio Manager" persona) reads all the independent analyst reports.
    *   It synthesizes the views, highlights consensus, debates disagreements, and outputs a final, actionable set of recommendations (e.g., "Rotate out of Semis into Defensive ETFs", "Buy SPY Puts for March volatility").
5.  **Presentation Layer:**
    *   The final markdown and individual reports are rendered into a static site (using Jekyll, Hugo, or MkDocs) and published to GitHub Pages.

## Maximizing the Likelihood to Beat SPY
To beat a buy-and-hold SPY strategy doing only a few trades a month, the system must focus on **avoiding major drawdowns** and **catching sector rotations**. 

Here is how to design the system to maximize this:

1.  **Specialized Prompting (Role-Playing):** Don't just ask the LLMs "what should I buy?". Assign them roles.
    *   *LLM 1 (The Risk Manager):* Tasked purely with finding reasons to sell, identifying bearish divergence, and highlighting macro risks.
    *   *LLM 2 (The Macro Strategist):* Focuses on interest rates, currency pairs, global markets (Asian/European leads), and seasonality.
    *   *LLM 3 (The Technical Trader):* Ignores news, looks purely at price action, moving average crossovers, and support/resistance levels.
    *   *The Portfolio Manager:* Weighs these inputs against your static `thesis.md` constraints.
2.  **Structured Output for Actionability:** Force the final LLM to output a structured JSON/Markdown table with explicit Conviction Levels (Low, Medium, High), Timeframe (Days, Weeks, Months), and specific Action (Buy, Sell, Hold, Buy Calls/Puts).
3.  **Historical Accountability (The Feedback Loop):** The system must look at its past predictions. Feed the previous week's final recommendation back into the current prompt along with what *actually* happened. "Last week you suggested buying XYZ, it dropped 5%. Analyze why you were wrong." This grounds the LLMs and reduces hallucination.
4.  **Hardcoded Seasonality & Regime Detection:** Relying on an LLM to "remember" that midterm summers are bad is risky. Instead, have the Python data ingestion script calculate the current macro regime (e.g., "High Volatility, Downtrend") and explicit seasonality metrics, and feed these as hard facts into the prompt.
5.  **Focus on Asymmetric Risk:** Since you are trading options and ETFs, prompt the system to specifically look for setups where implied volatility is low before a known binary event, or where a sector ETF is at a major multi-year support level.

## Recommended Tech Stack
*   **Hosting/Compute:** GitHub Repository + GitHub Actions (Cron triggers).
*   **Frontend:** MkDocs with Material theme (excellent for reading markdown reports).
*   **Data Gathering:** Python (`yfinance` for prices/technicals, `newsapi` or `alpaca-trade-api` for news, `pandas_ta` for technical indicators).
*   **LLM Integration:** Python scripts using `litellm` (provides a unified interface to call Gemini, OpenAI, Anthropic, etc., using the same code).