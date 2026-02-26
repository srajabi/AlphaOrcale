import os
from alpaca.trading.client import TradingClient

def fetch_portfolio():
    api_key = os.getenv("ALPACA_API_KEY")
    secret_key = os.getenv("ALPACA_SECRET_KEY")
    
    if not api_key or not secret_key:
        print("ALPACA_API_KEY or ALPACA_SECRET_KEY not found. Skipping portfolio fetch.")
        
        # Create a placeholder file so MkDocs doesn't crash if secrets aren't set locally
        os.makedirs('docs', exist_ok=True)
        with open('docs/portfolio.md', 'w') as f:
            f.write("# Current Portfolio\n\n*API keys not configured. Cannot display live portfolio data.*")
        return

    try:
        trading_client = TradingClient(api_key, secret_key, paper=True)
        account = trading_client.get_account()
        positions = trading_client.get_all_positions()

        md_content = f"""# Alpaca Paper Trading Portfolio
        
## Account Summary
* **Account Status:** {account.status.value}
* **Cash Balance:** ${float(account.cash):,.2f}
* **Equity:** ${float(account.equity):,.2f}
* **Buying Power:** ${float(account.buying_power):,.2f}

## Current Positions

| Ticker | Quantity | Market Value | Current Price | Avg Entry Price | Unrealized P/L |
| :--- | :--- | :--- | :--- | :--- | :--- |
"""

        if not positions:
            md_content += "| - | - | - | - | - | No open positions |\n"
        else:
            for p in positions:
                pl = float(p.unrealized_pl)
                pl_color = "🟩" if pl >= 0 else "🟥"
                md_content += f"| **{p.symbol}** | {p.qty} | ${float(p.market_value):,.2f} | ${float(p.current_price):,.2f} | ${float(p.avg_entry_price):,.2f} | {pl_color} ${pl:,.2f} |\n"

        os.makedirs('docs', exist_ok=True)
        with open('docs/portfolio.md', 'w') as f:
            f.write(md_content)
            
        print("Successfully fetched and saved Alpaca portfolio to docs/portfolio.md")

    except Exception as e:
        print(f"Error fetching Alpaca portfolio: {e}")
        os.makedirs('docs', exist_ok=True)
        with open('docs/portfolio.md', 'w') as f:
            f.write(f"# Current Portfolio\n\n*Error fetching data: {e}*")

if __name__ == "__main__":
    fetch_portfolio()
