# Research Spikes for AlphaOracle

This document outlines the initial research tasks ("spikes") required to validate and design the core components of AlphaOracle.

A spike is a time-boxed investigation to explore a technical approach, evaluate a tool, or answer a specific architectural question before committing to a full implementation.

## Completed / Active Spikes
The detailed findings for each spike are located in the `spikes/` directory.

1.  **[Data Sources Evaluation](spikes/data_sources.md):** What are the most reliable, cost-effective APIs for end-of-day stock prices, options chains, and financial news suitable for a daily GitHub Action?
2.  **[Technical Indicators Selection](spikes/technicals.md):** Which specific technical indicators (e.g., RSI, MACD) are most effective for identifying swing trade setups and sector rotations?
3.  **[Trading Strategies (Swing/Options)](spikes/trading_strategies.md):** How do we structure the LLM prompts to identify high-probability swing trades and basic options strategies (e.g., cash-secured puts, covered calls, long calls/puts on SPY/ETFs)?
4.  **[Market Seasonality & Regimes](spikes/seasonalities.md):** How do we programmatically define and calculate market seasonality (e.g., midterm election years, "Sell in May") and current market regimes (e.g., High Volatility Downtrend)?

## Future Spikes
*   **LLM Multi-Agent Orchestration:** Evaluate libraries like `litellm`, LangChain, or simple custom Python scripts for managing parallel LLM calls to different providers (Gemini, Anthropic, OpenAI).
*   **GitHub Actions Secrets & Workflow:** Test setting up a daily cron job in GitHub Actions, securely injecting API keys, and automatically committing the generated Markdown files back to the repository.
*   **MkDocs & GitHub Pages Deployment:** Create a basic MkDocs Material site and automate its deployment via GitHub Actions.
*   **Historical Accountability Loop:** Design the mechanism for storing past predictions and feeding them back into the next day's prompt for self-correction.