# Daily Tracking Workflow

## 📊 Complete Daily Process

```
┌─────────────────────────────────────────────────────────────────┐
│                    DAILY UPDATE WORKFLOW                        │
└─────────────────────────────────────────────────────────────────┘

   STEP 1: Load Latest Market Data
   ════════════════════════════════════════════════════════════

   Polygon API
      │
      │ (fetch latest prices)
      ↓
   polygon_loader
      │
      │ (store in MongoDB)
      ↓
   MongoDB Databases:
      ├─ NYSE_Polygon.ticks
      ├─ NASDAQ_Polygon.ticks
      └─ AMEX_Polygon.ticks

   ✅ Fresh price data now in database


   STEP 2: Update Tracking
   ════════════════════════════════════════════════════════════

   MongoDB (ticks)
      │
      │ (read latest prices)
      ↓
   track_performance.py
      │
      │ (calculate returns)
      ↓
   MongoDB:
      market_data.performance_tracking
      ├─ entry_price: $227.77
      ├─ latest_price: $235.50
      └─ latest_return: +3.4%

   ✅ Tracking updated with current returns

```

---

## 🎯 **Two-Part Workflow**

### **Part 1: Daily Tracking Update** (Run Daily)

```bash
cd /Volumes/1T_ExFAT/StockScan/devcpp/Sarah2/scripts
./complete_daily_update.sh
```

**What happens:**
- ✅ Reads latest prices from MongoDB for 101 tracked stocks
- ✅ Calculates current returns vs entry prices
- ✅ Shows summary status

**Time:** ~5 seconds
**When:** Daily after market close (5:00 PM ET)

---

### **Part 2: Polygon Data Refresh** (Run Periodically)

```bash
cd /Volumes/1T_ExFAT/StockScan/devcpp/Sarah2/Polygon/Scripts
./auto_run_polygon_loader.sh
```

**What happens:**
- 📥 Downloads ALL market data from Polygon API
- 💾 Updates MongoDB with latest bars (~6,750 symbols)
- 🔄 Incremental updates (only fetches new bars since last run)

**Time:** 1-3 hours (API rate limits)
**When:** Weekly, or as needed (not daily)

**Why separate?**
- Polygon has rate limits (5 req/sec)
- Full download takes hours for all markets
- Daily tracking only needs data already in MongoDB
- Most stocks don't need daily re-downloads (data doesn't change retroactively)

---

## ⚙️ **What Each Component Does**

### **polygon_loader_claude.py**
- 📥 Fetches latest bars from Polygon API
- 💾 Stores in MongoDB `ticks` collection (all 3 markets: NYSE, NASDAQ, AMEX)
- 🔄 Updates existing symbols with new data
- ⏰ Run ONCE per day after market close
- 🔁 Auto-resume with checkpointing

**Location:** `/Volumes/1T_ExFAT/StockScan/devcpp/Sarah2/Polygon/Scripts/polygon_loader_claude.py`

**Example:**
```bash
cd Polygon/Scripts
./auto_run_polygon_loader.sh
# Output: Processes all markets automatically
```

---

### **track_performance.py**
- 📊 Reads latest tick from MongoDB
- 📈 Calculates current return vs entry
- 💾 Updates tracking records
- ⏰ Run AFTER polygon_loader

**Location:** `/Volumes/1T_ExFAT/StockScan/devcpp/Sarah2/scripts/track_performance.py`

**Example:**
```bash
./track.sh update NYSE_Polygon
# Output: Updated 50 stock prices
#   BA  $227.77 → $235.50 (+3.4%)
```

---

## 📅 **Daily Schedule**

### **Recommended Timing**

```
4:00 PM ET  │ Market Close
            ↓
5:00 PM ET  │ Polygon data available (wait ~1 hour)
            ↓
5:30 PM ET  │ Run: ./complete_daily_update.sh
            ↓
5:35 PM ET  │ Tracking updated ✅
```

---

## 🔄 **Automated Setup**

### **Cron Job (Recommended)**

```bash
# Edit crontab
crontab -e

# Add this line (runs daily at 5:30 PM ET)
30 17 * * 1-5 cd /Volumes/1T_ExFAT/StockScan/devcpp/Sarah2/scripts && ./complete_daily_update.sh >> ../logs/daily_tracking.log 2>&1
```

**Benefits:**
- ✅ Runs automatically every weekday
- ✅ Logs output for review
- ✅ Never forget to update

---

## ⚠️ **Common Issues**

### **Issue: "No price data found"**

**Cause:** MongoDB doesn't have latest data

**Solution:**
```bash
# Run polygon_loader first!
cd Polygon/Scripts
./auto_run_polygon_loader.sh

# Then update tracking
cd ../../scripts
./daily_update.sh
```

---

### **Issue: Tracking shows yesterday's prices**

**Cause:** Ran tracking before loading new data

**Solution:**
```bash
# Always load data FIRST
./complete_daily_update.sh  # This does it in correct order
```

---

### **Issue: MongoDB connection error**

**Cause:** MongoDB not running

**Solution:**
```bash
# Check MongoDB
ps aux | grep mongod

# Restart if needed
./bin/restart_mongo_mac.sh
```

---

## 📊 **Data Flow Diagram**

```
External Data          Database            Tracking System
─────────────          ────────            ───────────────

Polygon API    →    MongoDB           →   Performance
                    (ticks)                 Tracking
                                            Database

Step 1:             Step 2:
polygon_loader      track.sh update
loads data          reads data &
into MongoDB        calculates returns
```

---

## ✅ **Quick Verification**

After running daily update, verify it worked:

```bash
# Check latest update time
./track.sh status NYSE_Polygon

# Should show today's date in tracking records
# If shows yesterday, data wasn't loaded
```

---

## 🎯 **Summary**

**Daily Command (Run Every Weekday):**
```bash
cd /Volumes/1T_ExFAT/StockScan/devcpp/Sarah2/scripts
./complete_daily_update.sh
```
- Time: ~5 seconds
- Updates tracking using existing MongoDB data

**Periodic Polygon Update (Run Weekly):**
```bash
cd /Volumes/1T_ExFAT/StockScan/devcpp/Sarah2/Polygon/Scripts
./auto_run_polygon_loader.sh
```
- Time: 1-3 hours
- Downloads fresh data from Polygon API

**Remember:**
1. Daily tracking doesn't need Polygon downloads
2. Run Polygon loader weekly or as needed
3. Verify tracking: `./track.sh status NYSE_Polygon`

---

**Last Updated:** January 5, 2026
