# Quick Reference Card

## 🚀 Most Common Commands

### Daily Update (Run Every Weekday)
```bash
cd /Volumes/1T_ExFAT/StockScan/devcpp/Sarah2/scripts
./complete_daily_update.sh
```
**What it does:**
- Updates tracking for all 101 stocks using existing MongoDB data
- Reads latest prices from NYSE_Polygon, NASDAQ_Polygon, AMEX_Polygon databases
- Calculates returns vs entry prices

**Time:** ~5 seconds (no Polygon download)

### Polygon Data Update (Run Periodically)
```bash
cd /Volumes/1T_ExFAT/StockScan/devcpp/Sarah2/Polygon/Scripts
./auto_run_polygon_loader.sh
```
**What it does:** Downloads ALL market data from Polygon API (~6,750 symbols)

**Time:** 1-3 hours (API rate limits)

**When to run:** Weekly or as needed (not daily)

---

### Check Status
```bash
./track.sh status NYSE_Polygon
./track.sh status NASDAQ_Polygon
./track.sh status AMEX_Polygon
```
**What it does:** Shows active tracking count and top stocks

---

### After 20 Days (Jan 30+)
```bash
./track.sh finalize NYSE_Polygon
./track.sh finalize NASDAQ_Polygon
./track.sh finalize AMEX_Polygon
```
**What it does:** Generates validation report with win rates, returns, and CSV export

---

## 📊 Current Tracking

| Market | Stocks | Entry Date | Exit Date |
|--------|--------|------------|-----------|
| NYSE | 50 | Jan 4, 2026 | Jan 30, 2026 |
| NASDAQ | 50 | Jan 4, 2026 | Jan 30, 2026 |
| AMEX | 1 | Jan 4, 2026 | Jan 30, 2026 |

**Total:** 101 stocks being tracked

---

## 🎯 Top Picks

**Highest Conviction (Tier 2):**
- SKYT (NASDAQ) - $22.43, Score: 77.1
- BA (NYSE) - $227.77, Score: 75.8
- ARDX (NASDAQ) - $6.15, Score: 75.5

---

## 📁 Files

- `track.sh` - Main tracking commands
- `daily_update.sh` - Run all daily updates at once
- `TRACKING_README.md` - Full documentation
- `TRACKING_SUMMARY.md` - Detailed tracking summary
- `QUICK_REFERENCE.md` - This file

---

## ⏰ Schedule

**Daily:** Run `./daily_update.sh` after market close (5 PM ET)
**Mid-point:** Jan 15 - Check progress
**Finalization:** Jan 30+ - Generate reports

---

## ✅ Success Criteria

- Overall win rate ≥ 50%
- Tier 2 stocks outperform Tier 4
- Average return > 0%
- Better than old system (2.33% win rate)

---

## 🆘 Help

```bash
./track.sh          # Show usage
cat TRACKING_README.md  # Full documentation
cat TRACKING_SUMMARY.md # Current status
```
