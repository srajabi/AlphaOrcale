# AlphaOracle Development Process

To prevent broken builds and failed GitHub Actions runs, always follow this local validation process before committing and pushing code.

## 1. Local Testing
Before committing any changes, run the entire pipeline locally to ensure there are no syntax errors, missing dependencies, or logic failures.

### Step 1: Install Dependencies
Ensure your local environment matches the `requirements.txt`:
```bash
pip install -r requirements.txt
```

### Step 2: Run Data Ingestion
Verify that the `yfinance` and `ta` libraries are working and that data is successfully saved to `data/market_context.json`:
```bash
python src/data_ingestion.py
```

### Step 3: Run LLM Agents
Verify that your API keys are loaded correctly from your `.env` file and that the LLMs can successfully read the context, debate, and generate the markdown reports and JSON trades.
```bash
python src/llm_agents.py
```
*Check `data/trades.json` to ensure the trades are formatted correctly.*

### Step 4: Test Alpaca Execution (Optional/Dry Run)
If you have modified the execution logic, test it against your Paper Trading account.
```bash
python src/execute_trades.py
```

### Step 5: Test Live Portfolio Fetch
Verify that the portfolio script connects to Alpaca and correctly generates the markdown table.
```bash
python src/fetch_alpaca_portfolio.py
```

### Step 6: Test MkDocs Build
Verify that the static site generates without errors.
```bash
mkdocs build
# Or to preview it locally:
# mkdocs serve
```

## 2. Commit and Push
Only after all local steps succeed without stack traces or errors should you commit and push to `main` to trigger the GitHub Action.