# Bayesian Analysis - Quick Reference

## 📅 Timeline

```
Jan 4-30:  Track 105 stocks daily
           → ./daily_update.sh (every day)

Jan 30:    Finalize tracking
           → ./track.sh finalize NYSE_Polygon
           → ./track.sh finalize NASDAQ_Polygon
           → ./track.sh finalize AMEX_Polygon

Jan 31:    Analyze results
           → python3 bayesian_analysis.py

Feb 1:     Apply updates
           → Update config.ini weights
           → Rebuild stock_analyzer
           → Start Round 2 tracking
```

---

## 🎯 What You'll Learn

| Analysis | Question Answered |
|----------|-------------------|
| **Pattern Success** | Which patterns actually win? CupHandle vs Spoon vs VBottom |
| **Tier Validation** | Does Tier 2 really outperform Tier 3? |
| **Weight Optimization** | Which components (pattern/momentum/volume) predict wins? |
| **Risk Calibration** | Does risk penalty correctly predict losses? |

---

## 📊 Example Output

```
Pattern Success Rates:
├─ CupHandle: 70% → Boost by 40% (1.4x multiplier)
├─ Spoon: 60% → Boost by 20% (1.2x multiplier)
└─ VBottom: 45% → No boost (1.0x multiplier)

Tier Performance:
├─ Tier 2 (75-84): 60% win rate
└─ Tier 3 (65-74): 62.5% win rate ❌ Better!
   → Action: Raise Tier 2 threshold to 77

Weight Correlations:
├─ Pattern: +12.3 points → Increase weight 30% → 40%
├─ Momentum: +8.1 points → Increase weight 25% → 30%
├─ Volatility: +2.4 points → Decrease weight 25% → 20%
└─ Volume: +1.2 points → Decrease weight 20% → 10%
```

---

## 🔧 How to Apply Results

### 1. Update Weights (config.ini)
```ini
[Composite]
weightPattern = 0.40      # Was 0.30
weightMomentum = 0.30     # Was 0.25
weightVolatility = 0.20   # Was 0.25
weightVolume = 0.10       # Was 0.20
```

### 2. Adjust Tier Thresholds (CompositeScorer.cpp)
```cpp
// OLD
if (score >= 75.0) tier = 2;

// NEW (if Tier 3 outperforms)
if (score >= 77.0) tier = 2;
```

### 3. Add Pattern Multipliers (Optional)
```cpp
// BayesianAdjustments.h
static const std::map<std::string, double> multipliers = {
    {"CupHandle", 1.40},  // 70% win rate
    {"Spoon", 1.20},      // 60% win rate
    {"VBottom", 1.00}     // 50% win rate
};
```

---

## 🔄 Iterative Learning

```
Round 1 (Jan): Default settings → Collect data → Analyze
                ↓
Round 2 (Feb): Updated settings → More data → Stronger priors
                ↓
Round 3 (Mar): Refined settings → Even more data → High confidence
```

**Each round makes the system smarter!**

---

## 🚀 Commands

```bash
# Daily (Jan 4-30)
./daily_update.sh

# Finalize (Jan 30)
./track.sh finalize NYSE_Polygon
./track.sh finalize NASDAQ_Polygon
./track.sh finalize AMEX_Polygon

# Analyze (Jan 31)
python3 bayesian_analysis.py

# View detailed guide
cat BAYESIAN_ANALYSIS.md
```

---

## 💡 Key Insights

**Bayesian = Learning from Evidence**

- Prior: "I think CupHandle wins 50%" (guess)
- Data: 35/50 CupHandle patterns won (70%)
- Posterior: "CupHandle wins 70% ± 8%" (confident!)
- Action: Boost CupHandle scores by 40% next round

---

## 📈 Expected Improvements

| Before | After |
|--------|-------|
| Win rate: ~50% (unknown) | Win rate: 60-65% (optimized) |
| Weights: Guessed | Weights: Data-driven |
| Tiers: Assumed | Tiers: Validated |
| Patterns: Equal | Winners boosted 1.4x |

---

## ✅ Success Criteria

After Round 2 (with Bayesian updates):

- [ ] Overall win rate improves by 10-15%
- [ ] Tier 2 clearly outperforms Tier 3
- [ ] CupHandle patterns show higher returns
- [ ] Risk penalty correlates with actual losses
- [ ] Fewer false positives (high-scoring losers)

---

**Full Documentation:** `BAYESIAN_ANALYSIS.md`

**Last Updated:** January 7, 2026
