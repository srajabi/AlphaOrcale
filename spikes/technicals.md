# Spike: Technical Indicators & Market Regimes

**Objective:** Determine which technical indicators to calculate via Python (`pandas_ta`) before passing data to the LLM. The goal is to provide objective mathematical context, reducing LLM hallucination and focusing on swing trading setups.

## Core Philosophy
LLMs are bad at raw math over large datasets. We must pre-calculate technicals and feed them as definitive statements (e.g., "SPY RSI is 32. It is below the 200 SMA.") rather than asking the LLM to look at 100 days of prices and guess the trend.

## Recommended Indicators for Swing Trading

### 1. Trend Identification (Moving Averages)
*   **200-day Simple Moving Average (SMA):** The ultimate baseline. Are we in a long-term bull or bear market?
*   **50-day SMA:** Medium-term trend.
*   **20-day Exponential Moving Average (EMA):** Short-term momentum.
*   *Setup Signal:* "Golden Cross" (50 crosses above 200) or "Death Cross". Price distance from the 200 SMA (mean reversion).

### 2. Momentum & Overbought/Oversold
*   **Relative Strength Index (RSI - 14 period):**
    *   *Use:* Identify extremes. RSI < 30 (Oversold - potential bounce). RSI > 70 (Overbought - potential pullback).
    *   *Advanced:* Bullish/Bearish Divergence (price makes a lower low, but RSI makes a higher low). *Note: Hard to calculate programmatically, better suited for the LLM to identify if given the data points.*
*   **MACD (Moving Average Convergence Divergence):**
    *   *Use:* Trend changes and momentum shifts. Look for MACD line crossing the signal line.

### 3. Volatility & Risk
*   **Bollinger Bands (20 SMA, 2 Std Dev):**
    *   *Use:* Volatility expansion/contraction. "Squeezes" indicate impending large moves. Price touching the lower band often signals a short-term bounce in a bull market.
*   **Average True Range (ATR):**
    *   *Use:* Measures daily volatility. Crucial for setting stop-losses and position sizing.
*   **VIX (CBOE Volatility Index):**
    *   *Use:* The "Fear Gauge." VIX > 30 = High fear/volatility (often bottoms). VIX < 15 = Complacency.

## Defining Market Regimes Programmatically
Instead of asking the LLM "What is the market doing?", the Python script should define the regime based on the SPY (S&P 500 ETF) and prepend this to the prompt.

**Example Logic:**
1.  **Bull Volatile:** Price > 200 SMA AND VIX > 20. (Fast corrections, strong dip buying).
2.  **Bull Quiet:** Price > 200 SMA AND VIX < 20. (Steady grind higher, typical buy-and-hold).
3.  **Bear Volatile:** Price < 200 SMA AND VIX > 25. (Aggressive selloffs, sharp bear market rallies).
4.  **Bear Quiet:** Price < 200 SMA AND VIX < 20. (Slow bleed, low liquidity).

## Implementation
Use the `pandas_ta` library in Python. It's fast, reliable, and covers all the indicators listed above. Output the results into a clean, readable text summary for the LLM context.