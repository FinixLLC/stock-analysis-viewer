# Database Configuration

## Tracking Database Location

**Database:** `stock_tracking`
**Collection:** `performance_tracking`

## Why Separate Database?

The tracking system uses the `stock_tracking` database (not `market_data`) for these reasons:

1. **Isolation:** `stock_analysis` cleans specific collections in `market_data` database
2. **Safety:** Your tracking data will never be accidentally deleted
3. **Clear separation:** Analysis results vs tracking data

## What's in Each Database

### `market_data` (Analysis Results)
Collections cleaned by `stock_analysis`:
- macd_results
- ma_results
- rsi_results
- composite_scores
- aggregated_signals
- (and 18 other analysis collections)

### `stock_tracking` (Your Tracking Data)
Collections:
- `performance_tracking` - Your 105 tracked stocks (NYSE, NASDAQ, AMEX)

### Price Data Databases (Never Touched)
- `NYSE_Polygon` - NYSE stock price data (per-symbol collections)
- `NASDAQ_Polygon` - NASDAQ stock price data (per-symbol collections)
- `AMEX_Polygon` - AMEX stock price data (per-symbol collections)

## Migration Completed

**Date:** January 7, 2026
**Action:** Migrated 105 tracking records from `market_data.performance_tracking` to `stock_tracking.performance_tracking`
**Status:** ✅ Complete

## Viewing Your Tracking Data

```bash
# Check tracking records
mongosh stock_tracking --eval "db.performance_tracking.countDocuments({})"

# View by market
mongosh stock_tracking --eval "
  db.performance_tracking.aggregate([
    {\$group: {_id: '\$market', count: {\$sum: 1}}},
    {\$sort: {_id: 1}}
  ]).forEach(doc => print(doc._id + ': ' + doc.count))
"
```

## Safety Check

If you ever lose tracking data again:
1. Check `stock_tracking` database first: `mongosh stock_tracking`
2. If empty, re-initialize from latest Top50 files
3. `stock_analysis` will NOT touch this database

---

**Last Updated:** January 7, 2026
