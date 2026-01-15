# Polygon Data Loader

## 📥 Overview

The system uses a Python-based Polygon data loader that fetches the latest stock data from Polygon.io API and stores it in MongoDB.

**Location:** `/Volumes/1T_ExFAT/StockScan/devcpp/Sarah2/Polygon/Scripts/polygon_loader_claude.py`

---

## 🚀 How It Works

The loader processes all three markets (NYSE, NASDAQ, AMEX) in a **single run** with these features:

### **Key Features**

1. **Auto-Resume with Checkpointing** 🔁
   - Saves progress every 10 symbols
   - Automatically resumes if interrupted
   - No need to start from scratch after failures

2. **Concurrent Symbol Processing** ⚡
   - Uses 2 worker threads per market
   - Processes multiple symbols simultaneously
   - Includes rate limiting to stay within API limits

3. **Error Handling** 🛡️
   - Retries failed requests (max 2 attempts)
   - Logs empty symbols separately
   - Continues processing even if individual symbols fail

4. **Market Coverage** 🌐
   - NYSE_Polygon database (~2,500 symbols)
   - NASDAQ_Polygon database (~3,800 symbols)
   - AMEX_Polygon database (~450 symbols)

---

## 💡 Usage

### **Automatic (Recommended)**

```bash
cd /Volumes/1T_ExFAT/StockScan/devcpp/Sarah2/scripts
./complete_daily_update.sh
```

This runs the loader automatically and then updates tracking.

### **Manual**

```bash
cd /Volumes/1T_ExFAT/StockScan/devcpp/Sarah2/Polygon/Scripts
./auto_run_polygon_loader.sh
```

**Options:**
- `./auto_run_polygon_loader.sh` - Auto-resume from last checkpoint
- `./auto_run_polygon_loader.sh --reset` - Clear checkpoint and start fresh
- `./auto_run_polygon_loader.sh --resume SYMBOL` - Resume from specific symbol

---

## 📊 Performance

**Typical Load Times:**
- NYSE: ~2-3 minutes (2,500 symbols)
- NASDAQ: ~3-4 minutes (3,800 symbols)
- AMEX: ~1-2 minutes (450 symbols)
- **Total: ~6-9 minutes** for all markets

**Processing Speed:**
- ~15-20 symbols per minute (with rate limiting)
- Concurrent requests within API limits (5 req/sec)
- Automatic throttling to avoid rate limit errors

---

## 🔧 Configuration

The loader is configured in `polygon_loader_claude.py`:

```python
DEBUG = False  # Use production databases
DB_NAMES = ["NASDAQ_Polygon", "NYSE_Polygon", "AMEX_Polygon"]

MAX_THREADS = 2  # Concurrent symbol processing
REQUEST_INTERVAL = 0.5  # Rate limiting (2 req/sec per thread)
CHECKPOINT_FREQUENCY = 10  # Save progress every 10 symbols
```

---

## 📝 Logs and Output

### **Console Output**
Shows real-time progress:
```
Loading symbols for NASDAQ_Polygon...
  Processed: 100/3800 symbols
  Success: 98, Failed: 2, Empty: 0
```

### **Log File**
Detailed logs saved to: `polygon_loader.log`

```bash
# View recent activity
tail -50 polygon_loader.log

# Search for errors
grep ERROR polygon_loader.log
```

### **Checkpoint File**
Progress saved to: `polygon_checkpoint.txt`

Contains the last successfully processed symbol per market.

---

## ⚠️ Important Notes

### **API Requirements**
- Requires `POLYGON_API_KEY` environment variable
- Uses free tier limits (5 requests/second)
- Fetches daily bars (OHLCV data)

### **MongoDB Databases**
Each market has its own database:
- `NYSE_Polygon` → `ticks` collection
- `NASDAQ_Polygon` → `ticks` collection
- `AMEX_Polygon` → `ticks` collection

### **Data Freshness**
- Polygon data available ~1 hour after market close
- Run loader after 5:00 PM ET for same-day data
- Each symbol gets latest bar (yesterday's close if today unavailable)

---

## 🔍 Troubleshooting

### **"POLYGON_API_KEY not set"**
```bash
export POLYGON_API_KEY="your_key_here"
# Add to ~/.bashrc or ~/.zshrc for persistence
```

### **"Rate limit exceeded"**
The loader automatically handles this with:
- Request throttling (0.5s between requests)
- Retry logic with backoff
- Just let it continue - it will recover

### **Interrupted Mid-Run**
No problem! Just run again:
```bash
./auto_run_polygon_loader.sh
# Automatically resumes from checkpoint
```

### **Start Fresh**
```bash
./auto_run_polygon_loader.sh --reset
```

---

## 📈 Integration with Tracking

The complete workflow:

```
1. Polygon API
      ↓
2. polygon_loader_claude.py
      ↓ (stores in MongoDB)
3. MongoDB: NYSE_Polygon, NASDAQ_Polygon, AMEX_Polygon
      ↓ (read by)
4. track_performance.py
      ↓ (calculates returns)
5. MongoDB: market_data.performance_tracking
```

**Command:**
```bash
./complete_daily_update.sh  # Does steps 2-4 automatically
```

---

## ✅ Summary

**What it does:**
- Fetches latest stock data from Polygon.io
- Stores in MongoDB (separate database per market)
- Auto-resumes if interrupted
- Handles errors gracefully

**When to run:**
- Daily after market close (5:30 PM ET recommended)
- Before running tracking updates

**How long it takes:**
- ~6-9 minutes for all three markets

---

**Last Updated:** January 5, 2026
