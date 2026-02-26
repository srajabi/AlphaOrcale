import os
import json
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

def execute_trades():
    print("Initializing Alpaca client...")
    # Load API keys from environment variables
    api_key = os.getenv("ALPACA_API_KEY")
    secret_key = os.getenv("ALPACA_SECRET_KEY")
    
    if not api_key or not secret_key:
        print("Error: ALPACA_API_KEY or ALPACA_SECRET_KEY not found in environment. Skipping execution.")
        return

    # Initialize the trading client. paper=True means we are using paper trading.
    trading_client = TradingClient(api_key, secret_key, paper=True)

    # Check if trades.json exists
    trades_file = "data/trades.json"
    if not os.path.exists(trades_file):
        print(f"No {trades_file} found. No trades to execute.")
        return

    with open(trades_file, "r") as f:
        try:
            trades = json.load(f)
        except json.JSONDecodeError:
            print(f"Error parsing {trades_file}. Invalid JSON.")
            return

    if not trades:
        print("No actionable trades found in JSON array.")
        return

    for trade in trades:
        ticker = trade.get("ticker")
        action = trade.get("action", "").lower()
        
        if not ticker or action not in ["buy", "sell"]:
            print(f"Invalid trade block: {trade}. Skipping.")
            continue
            
        side = OrderSide.BUY if action == "buy" else OrderSide.SELL

        print(f"Preparing to {action.upper()} {ticker}...")

        try:
            # Handle closing an entire position
            if action == "sell" and str(trade.get("qty")).lower() == "all":
                print(f"Closing entire position for {ticker}")
                trading_client.close_position(ticker)
                print(f"Successfully sent order to close {ticker}")
                continue

            # Prepare the order request
            order_data = {
                "symbol": ticker,
                "side": side,
                "time_in_force": TimeInForce.DAY
            }

            # Alpaca allows specifying EITHER fractional quantities OR notional dollar amounts
            if "notional_value" in trade:
                order_data["notional"] = float(trade["notional_value"])
            elif "qty" in trade:
                order_data["qty"] = float(trade["qty"])
            else:
                print(f"Trade must specify 'qty' or 'notional_value': {trade}. Skipping.")
                continue
                
            market_order_data = MarketOrderRequest(**order_data)
            
            # Submit the order
            market_order = trading_client.submit_order(order_data=market_order_data)
            print(f"Order submitted successfully: {market_order.id}")

        except Exception as e:
            print(f"Failed to execute trade for {ticker}: {e}")

if __name__ == "__main__":
    execute_trades()
