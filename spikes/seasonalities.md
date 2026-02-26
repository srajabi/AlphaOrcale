# Spike: Market Seasonality & Historical Tendencies

**Objective:** Document known historical market patterns (seasonality) and determine how to inject them into the AlphaOracle system as hard facts.

## Key Seasonality Concepts

### 1. The Presidential Cycle (4-Year Cycle)
The US stock market historically exhibits specific behavior based on the presidential term.
*   **Year 1 (Post-Election):** Often volatile as new policies are introduced. Average returns.
*   **Year 2 (Midterm Year):** Historically the weakest year. **Crucial:** The period from Q2 through Q3 (Summer) is often marked by significant drawdowns, culminating in a low around October before the midterm elections.
*   **Year 3 (Pre-Election):** Historically the strongest year. Markets generally rally.
*   **Year 4 (Election Year):** Generally positive, but with high volatility in September/October leading up to the election.

### 2. Monthly Seasonality ("Sell in May")
*   **November to April:** Historically the strongest six months of the year for equities.
*   **May to October:** Historically the weakest six months. "Sell in May and go away."
*   **September:** Statistically the worst performing month of the year for the S&P 500.
*   **The "Santa Claus Rally":** A tendency for the market to rise during the last five trading days of the year and the first two of the new year.

### 3. Structural and Tax-Driven Events
*   **Tax-Loss Harvesting (November/December):** Investors sell losing positions to offset gains for tax purposes, putting further downward pressure on already struggling stocks. (Followed by the "January Effect" where these stocks often bounce).
*   **Options Expiration (OpEx):** The third Friday of every month. Large options expirations can cause significant market volatility and pin prices to certain strike levels.
*   **Window Dressing (End of Quarter):** Institutional fund managers buy winning stocks and sell losers near the end of the quarter to make their portfolios look better in reports.

### 4. Global Equity Seasonality
While US markets often dictate global trends, international markets have their own distinct seasonal quirks.
*   **Canada (TSX):** Exhibits strong Q4 performance (Nov-Jan) similar to the US, but the "Sell in May" effect can sometimes be muted. Canadian markets are heavily weighted towards commodities and financials. Strength in late summer is sometimes observed if commodity prices (gold, oil) rise. However, September remains historically a very weak month.
*   **Europe:** Exhibits a very statistically significant "Halloween Effect" (Nov-Apr outperformance) and a strong "Sell in May" effect. The "Turn-of-the-month" effect is also notably strong in European equities.
*   **Australia (ASX):** Australia's financial year ends in June. Consequently, July is historically one of the strongest months for the ASX due to fresh capital allocation after tax-loss selling in June. April and December are also historically very strong, while May and June often see negative returns. The "January Effect" is less pronounced than in the US.

### 5. Commodity Seasonality: Gold in Asia
Gold has significant cultural and seasonal demand drivers outside of Western macroeconomics (like the US Dollar or real yields), primarily driven by the Asian physical market.
*   **Diwali (India):** Typically falls between October and November. It is highly auspicious to purchase gold during this "Festival of Lights," leading to a significant spike in physical demand. Wholesalers build inventory in the weeks prior, often providing a seasonal tailwind for gold prices in late Q3/early Q4.
*   **Lunar New Year (China/East Asia):** Usually falls in late January or February. Gold is a traditional gift symbolizing prosperity. This creates a surge in retail bullion and jewelry demand leading up to the holiday, often supporting gold prices early in the calendar year.

## Implementation in AlphaOracle

Do not rely on the LLM to randomly remember these statistics. The Python ingestion script should use the current date to calculate the seasonal context and explicitly feed it to the LLMs.

**Example Python Logic Output (Injected into Prompt):**
```text
[SEASONALITY CONTEXT]
Current Date: 2026-02-25
Presidential Cycle: Year 2 (Midterm Year)
Historical Tendency Note: Midterm years historically experience significant volatility and drawdowns during the summer months (Q2-Q3), often bottoming in October.
Current Month: February. Statistically mixed performance.
Upcoming Events: Triple Witching Options Expiration in 3 weeks.
```

By providing this explicitly, the "Macro Strategist" LLM can factor the upcoming (predicted) midterm summer slump into its current recommendations (e.g., suggesting taking profits in March/April to prepare).