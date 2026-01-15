# Stock Performance Tracking System

This system tracks the performance of top-ranked stocks to validate the composite scoring algorithm improvements.

## Overview

The tracking system:
1. **Captures** top-ranked stocks from Top50 pattern files
2. **Monitors** their price performance over 20 trading days
3. **Validates** predictions by calculating actual returns
4. **Reports** win rates, average returns, and per-tier performance

## Quick Start

### 1. Initialize Tracking

After running analysis and generating a Top50 file, initialize tracking:

```bash
cd /Volumes/1T_ExFAT/StockScan/devcpp/Sarah2/scripts

# Initialize tracking from Top50 file
./track.sh init NYSE_Polygon ../Patterns/Top50_NYSE_Polygon_2026_01_04.txt
```

This creates tracking records in MongoDB (`market_data.performance_tracking`).

### 2. Update Prices (Daily)

Update current prices to track progress:

```bash
# Update NYSE prices
./track.sh update NYSE_Polygon

# Update NASDAQ prices
./track.sh update NASDAQ_Polygon

# Update AMEX prices
./track.sh update AMEX_Polygon
```

**Recommended:** Run daily after market close (or whenever new price data is loaded).

### 3. Check Status

View current tracking status:

```bash
# All markets
./track.sh status

# Specific market
./track.sh status NYSE_Polygon
```

### 4. Finalize & Generate Report (After 20 Days)

After 20 trading days, finalize tracking and generate validation report:

```bash
./track.sh finalize NYSE_Polygon
```

This will:
- Mark completed tracking records
- Calculate final returns
- Generate performance validation report
- Export results to CSV

### 5. View Report Anytime

Generate report for completed tracking:

```bash
./track.sh report NYSE_Polygon
```

## Automation (Optional)

### Daily Price Updates

Add to crontab to update prices daily at 5 PM (after market close):

```bash
# Edit crontab
crontab -e

# Add this line (update path as needed):
0 17 * * 1-5 cd /Volumes/1T_ExFAT/StockScan/devcpp/Sarah2/scripts && ./track.sh update NYSE_Polygon >> ../logs/tracking.log 2>&1
```

### Weekly Status Check

Send weekly status email (requires mail setup):

```bash
# Add to crontab (Mondays at 9 AM)
0 9 * * 1 cd /Volumes/1T_ExFAT/StockScan/devcpp/Sarah2/scripts && ./track.sh status NYSE_Polygon | mail -s "Stock Tracking Status" your@email.com
```

## Understanding the Output

### Tracking Initialization

```
✅ Tracking initialized: 50 stocks
   Entry Date: 2026-01-04
   Target Exit: 2026-01-30

📈 Top 10 Tracked Stocks:
Rank  Symbol  Pattern     Entry $   Score   Tier
1     BA      CupHandle   $227.77   75.8    2
```

- **Entry Date**: When stocks were identified
- **Target Exit**: 20 trading days later
- **Score**: Composite score (0-100)
- **Tier**: 1=Strong Buy, 2=Selective Buy, 3=Watchlist, 4=Monitor

### Price Updates

```
📈 Fetching latest prices...
   BA       $227.77 → $235.50 ( +3.4%)
   MSB      $ 35.84 → $ 37.20 ( +3.8%)
```

Shows current return for each tracked stock.

### Validation Report

```
Overall Performance (20-day forward returns):
Total Trades:     50
Winners:          35 (70.0%)
Losers:           15
Avg Return:       +5.2%
Avg Win:          +12.3%
Avg Loss:         -4.1%

Per-Tier Performance:
Tier  Count   Win Rate    Avg Return  Expected
2     2       100.0%      +15.2%      55%
3     30      73.3%       +6.5%       50%
4     18      61.1%       +2.1%       45%
```

- **Win Rate**: % of stocks with positive returns
- **Expected**: Target win rate for each tier
- **Success**: Actual win rate ≥ Expected win rate

## Database Schema

Tracking records stored in `market_data.performance_tracking`:

```javascript
{
  symbol: "BA",
  market: "NYSE_Polygon",
  entry_date: "2026-01-04",
  entry_price: 227.77,
  pattern_type: "CupHandle",
  rank: 1,
  tier: 2,
  composite_score: 75.8,
  pattern_score: 76.1,
  momentum_score: 73.6,
  volatility_score: 79.7,
  volume_score: 41.2,
  risk_penalty: 3.7,
  tracking_period_days: 20,
  status: "active",  // or "completed"
  price_updates: [
    {date: "2026-01-05", price: 230.50, return: 1.2},
    {date: "2026-01-06", price: 235.50, return: 3.4}
  ],
  final_price: null,
  final_return: null,
  win: null
}
```

## Troubleshooting

### "No price data found"

**Cause**: Symbol not in exchange database or missing tick data

**Solution**:
- Ensure Polygon data is loaded for the date range
- Check MongoDB connection
- Verify symbol exists in database

### "No active tracking records found"

**Cause**: Tracking not initialized or already finalized

**Solution**:
- Run `init` command to start tracking
- Check status with `./track.sh status`

### MongoDB connection error

**Cause**: MongoDB not running

**Solution**:
```bash
# Check MongoDB status
ps aux | grep mongod

# Restart MongoDB
cd /Volumes/1T_ExFAT/StockScan/devcpp/Sarah2
./bin/restart_mongo_mac.sh
```

## Files

- `track_performance.py` - Main tracking script
- `track.sh` - Convenient shell wrapper
- `TRACKING_README.md` - This file

## Current Tracking

### NYSE_Polygon (Initialized: 2026-01-04)

**Top 10 Stocks Being Tracked:**
1. BA - Boeing (CupHandle, Score: 75.8, Tier 2)
2. MSB - Mesabi Trust (CupHandle, Score: 75.0, Tier 3)
3. MUR - Murphy Oil (CupHandle, Score: 71.1, Tier 3)
4. IRS - IRSA Inversiones (CupHandle, Score: 70.2, Tier 3)
5. MEC - Mayville Engineering (CupHandle, Score: 69.6, Tier 3)
6. DAN - Dana Inc (CupHandle, Score: 68.9, Tier 3)
7. SNDR - Schneider National (CupHandle, Score: 68.4, Tier 3)
8. SSL - Sasol Limited (CupHandle, Score: 68.0, Tier 3)
9. MATV - Mativ Holdings (CupHandle, Score: 67.0, Tier 3)
10. ARR - ARMOUR Residential (CupHandle, Score: 66.4, Tier 3)

**Target Exit Date:** 2026-01-30 (20 trading days)

**Next Steps:**
1. Run daily price updates: `./track.sh update NYSE_Polygon`
2. After Jan 30, finalize tracking: `./track.sh finalize NYSE_Polygon`
3. Review validation report to confirm scoring improvements
