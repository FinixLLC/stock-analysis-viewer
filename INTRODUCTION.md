# Stock Analysis Engine

An automated, end-to-end stock analysis system that scans 8,500+ stocks across NASDAQ, NYSE, and AMEX daily. It combines a high-performance C++ technical analysis engine with Python-based ML ranking, chart pattern detection, and SEC fundamental analysis to surface the best trading opportunities each day.

## How It Works

Data Collection — Yahoo Finance price data is downloaded daily after market close for all three exchanges, stored in MongoDB.

Technical Analysis — A multi-threaded C++ engine evaluates each stock using 22 technical indicators across four categories: trend (MA, MACD, MAMA), momentum (RSI, MFI, RVI), volume (PVT, KVO, RVOL, Volume Profile), and statistical (Bollinger Bands, Linear Regression, FFT cycle detection, Z-Score). Each indicator is validated using Information Coefficient (IC) analysis against forward returns — weak predictors are automatically downweighted.

Pattern Detection — Five geometric chart patterns are identified: Cup & Handle, V-Bottom, Spoon, Darvas Box, and Point-of-Sell reversals. Pattern confidence is scored based on shape quality, volume confirmation, and momentum alignment.

ML Ranking — An Elastic Net model re-ranks the top stocks using 30+ features. Built-in health checks (correlation, variance, feature quality) ensure the ML layer adds value; if checks fail, the system gracefully falls back to the baseline C++ ranking.

Fundamental Scoring — SEC EDGAR filings (10-Q/10-K) are processed through local LLMs (Llama 3.1 8b for data extraction, DeepSeek R1 14b for investment reasoning) to assess revenue growth, profitability, debt levels, and cash flow. The final ranking blends 60% technical + 40% fundamental scores.

## Output

- Top 50 stocks per exchange, ranked by composite score (0-100) with confidence tiers
- Top 20 momentum and Top 20 volume leaders
- Pattern detection lists (Cup & Handle, V-Bottom, Spoon, Darvas Box)
- Full analysis CSV with all indicator values for further research

## Distribution

Results are published automatically to:
- Web viewer: [stock-analysis-viewer](https://finixllc.github.io/stock-analysis-viewer/) (GitHub Pages, updated nightly)
- iOS app: [Top Stock Analysis](https://apps.apple.com/app/top-stock-analysis/id6757944042) (reads from the same data)
- Reddit posts: Daily summaries with top picks and market commentary

## Daily Schedule (Weekdays, Pacific Time)

| Time | Step |
|------|------|
| 3-5 PM | Yahoo data download (AMEX, NYSE, NASDAQ) |
| 6 PM | Full analysis pipeline + GitHub Pages push |
| 9 PM | Portfolio update |
| 9:30 PM | Reddit post generation |

## Tech Stack

- C++ — Core analysis engine (22 indicators, 5 pattern detectors, multi-threaded)
- Python — ML ranking, data pipeline, portfolio tracking, Reddit/web publishing
- MongoDB — Price data and analysis results storage
- Ollama — Local LLM inference (Llama 3.1 8b, DeepSeek R1 14b) for fundamental analysis
- GitHub Pages + SwiftUI — Web and iOS distribution
