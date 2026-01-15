# GitHub Pages Deployment Guide

## 🎯 Overview

Deploy your stock analysis outputs to GitHub Pages for free hosting with a beautiful web interface.

**Cost:** FREE ✅
**Time:** 10 minutes
**URL:** `https://FinixLLC.github.io/stock-analysis-viewer`

---

## 🚀 Quick Start

### **Step 1: Initial Setup** (One-time)

```bash
cd /Volumes/1T_ExFAT/StockScan/devcpp/Sarah2/scripts
chmod +x setup_github_pages.sh
./setup_github_pages.sh
```

This creates:
- Beautiful web dashboard
- Auto-generated file listings
- Responsive design (mobile-friendly)
- All your analysis outputs organized

### **Step 2: Create GitHub Repository**

1. Go to https://github.com/organizations/FinixLLC/repositories/new
2. Repository name: `stock-analysis-viewer`
3. Description: `Stock Analysis Viewer with Bayesian Learning`
4. **Public** (required for free GitHub Pages)
5. Click "Create repository"

### **Step 3: Push to GitHub**

```bash
cd /Volumes/1T_ExFAT/StockScan/devcpp/Sarah2/src/stock-analysis-pages

# Add your GitHub repository
git remote add origin https://github.com/FinixLLC/stock-analysis-viewer.git

# Push
git branch -M main
git push -u origin main
```

### **Step 4: Enable GitHub Pages**

1. Go to your repository on GitHub
2. Click **Settings** → **Pages** (in left sidebar)
3. Under "Source":
   - Branch: `main`
   - Folder: `/ (root)`
4. Click **Save**

**🎉 Your site will be live in 1-2 minutes!**

**URL:** `https://FinixLLC.github.io/stock-analysis-viewer`

---

## 🔄 Daily Updates

After running `stock_analysis`, update your site:

```bash
cd /Volumes/1T_ExFAT/StockScan/devcpp/Sarah2/scripts
chmod +x update_github_pages.sh
./update_github_pages.sh
```

This:
- Copies latest Top50 and Pattern files
- Regenerates file listings
- Commits and pushes to GitHub
- Updates live site automatically (30-60 seconds)

---

## 🎨 What You Get

### **Beautiful Dashboard**

Your site includes:

✅ **Modern UI** - Gradient design, glass morphism effects
✅ **Live Stats** - Total stocks analyzed, patterns detected
✅ **File Browsing** - Easy access to all outputs
✅ **Responsive** - Works on desktop, tablet, mobile
✅ **Dark Mode** - Beautiful purple/blue gradient theme
✅ **Fast** - Hosted on GitHub's CDN worldwide

### **Pages Available**

| Page | Content |
|------|---------|
| **Home** | Dashboard with stats and file listings |
| **Top50** | Composite score CSV files |
| **Patterns** | Pattern analysis TXT files |
| **Docs** | Tracking guides, Bayesian analysis docs |

---

## 🔧 Customization

### **Update Site Title**

Edit `/Volumes/1T_ExFAT/StockScan/devcpp/Sarah2/src/stock-analysis-pages/index.html`:

```html
<h1>📊 YOUR CUSTOM TITLE</h1>
<p class="subtitle">Your custom subtitle</p>
```

### **Change Colors**

Edit the CSS gradient in `index.html`:

```css
/* Current: Purple gradient */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Option 2: Blue gradient */
background: linear-gradient(135deg, #3a7bd5 0%, #00d2ff 100%);

/* Option 3: Green gradient */
background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%);
```

### **Add Custom Pages**

```bash
cd /Volumes/1T_ExFAT/StockScan/devcpp/Sarah2/src/stock-analysis-pages

# Create new page
cat > custom-page.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>My Custom Page</title>
</head>
<body>
    <h1>Custom Content</h1>
</body>
</html>
EOF

git add custom-page.html
git commit -m "Add custom page"
git push
```

Access at: `https://FinixLLC.github.io/stock-analysis-viewer/custom-page.html`

---

## 📊 Features

### **Auto File Discovery**

The site automatically finds and lists:
- All `.csv` files in `top50/` folder
- All `.txt` files in `patterns/` folder
- All `.md` files in `tracking/` folder

No manual updates needed!

### **Stats Dashboard**

Edit `file-list.json` to update stats:

```json
{
  "stats": {
    "total_stocks": "105",
    "total_patterns": "50",
    "last_update": "Jan 8, 2026"
  }
}
```

### **Direct File Downloads**

All files are downloadable directly from the web interface. Visitors can:
- Click any file to download
- View CSV files in browser
- Access documentation

---

## 🔒 Privacy & Security

### **Public vs Private**

**GitHub Pages is PUBLIC by default**

If you have sensitive data:

1. **Option A: Keep Private Data Local**
   - Only push Top50 summaries (no full details)
   - Remove sensitive columns from CSVs
   - Don't push MongoDB dumps

2. **Option B: Use GitHub Pro ($4/mo)**
   - Enables private repositories with Pages
   - Still publicly accessible via URL
   - Just hides source code

3. **Option C: Deploy to Private Cloud**
   - See `deploy_to_cloud_vm.md` for alternatives
   - Full control over access

---

## 🌐 Custom Domain (Optional)

Want to use your own domain? (e.g., `stocks.yourdomain.com`)

### **Setup:**

1. Buy domain from Namecheap/GoDaddy (~$12/year)

2. Add DNS records:
   ```
   Type: CNAME
   Name: stocks (or @)
   Value: YOUR_USERNAME.github.io
   ```

3. In your GitHub repository:
   - Settings → Pages
   - Custom domain: `stocks.yourdomain.com`
   - Save

4. Create `CNAME` file:
   ```bash
   cd /Volumes/1T_ExFAT/StockScan/devcpp/Sarah2/src/stock-analysis-pages
   echo "stocks.yourdomain.com" > CNAME
   git add CNAME
   git commit -m "Add custom domain"
   git push
   ```

**Done!** Your site will be at `https://stocks.yourdomain.com` in 10-15 minutes.

---

## 🆘 Troubleshooting

### **"404 Page Not Found"**

- Wait 2-3 minutes after first push
- Check Settings → Pages is enabled
- Verify branch is `main` not `master`
- Clear browser cache (Cmd+Shift+R)

### **"Site Not Updating"**

```bash
# Force rebuild
cd /Volumes/1T_ExFAT/StockScan/devcpp/Sarah2/src/stock-analysis-pages
git commit --allow-empty -m "Rebuild site"
git push
```

### **"Files Not Showing"**

```bash
# Regenerate file list
cd /Volumes/1T_ExFAT/StockScan/devcpp/Sarah2/src/stock-analysis-pages
python3 << 'EOF'
import json
from pathlib import Path
from datetime import datetime

# ... (file discovery code from setup script)
EOF

git add file-list.json
git commit -m "Update file list"
git push
```

### **"Permission Denied"**

```bash
chmod +x /Volumes/1T_ExFAT/StockScan/devcpp/Sarah2/src/stock-analysis-pages/*.sh
```

---

## 📅 Automation

### **Auto-update after each analysis**

Add to your analysis workflow:

```bash
# File: run_analysis_and_deploy.sh
#!/bin/bash

# Run stock analysis
cd /Volumes/1T_ExFAT/StockScan/devcpp/Sarah2
./bin/stock_analyzer NYSE_Polygon

# Update GitHub Pages
cd scripts
./update_github_pages.sh

echo "✅ Analysis complete and deployed!"
```

### **Daily Auto-Deploy (Cron)**

```bash
crontab -e

# Add this line (deploy at 6 PM daily)
0 18 * * * cd /Volumes/1T_ExFAT/StockScan/devcpp/Sarah2/scripts && ./update_github_pages.sh >> ~/deploy.log 2>&1
```

---

## 💰 Cost

| Item | Cost |
|------|------|
| GitHub Pages | **FREE** |
| GitHub repository | **FREE** (public) |
| Custom domain (optional) | $12/year |
| SSL certificate | **FREE** (auto via GitHub) |

**Total:** FREE (or $12/year with custom domain)

---

## 🎯 Benefits

✅ **Free hosting** - No server costs
✅ **Fast CDN** - Global edge network
✅ **Auto HTTPS** - SSL included free
✅ **Easy updates** - One command
✅ **Version control** - Full history in Git
✅ **No maintenance** - GitHub handles everything
✅ **99.9% uptime** - GitHub's infrastructure

---

## 📚 Next Steps

1. **Run initial setup**
   ```bash
   ./setup_github_pages.sh
   ```

2. **Push to GitHub**
   ```bash
   cd /Volumes/1T_ExFAT/StockScan/devcpp/Sarah2/src/stock-analysis-pages
   git remote add origin https://github.com/FinixLLC/stock-analysis-viewer.git
   git push -u origin main
   ```

3. **Enable Pages** (Settings → Pages)

4. **Visit your site!**
   ```
   https://FinixLLC.github.io/stock-analysis-viewer
   ```

5. **Update after each analysis**
   ```bash
   ./update_github_pages.sh
   ```

---

## 🌟 Example Sites

**Your site will look like this:**

```
┌─────────────────────────────────────────────┐
│  📊 Stock Analysis Dashboard               │
│  Real-time pattern recognition             │
│                                             │
│  [105 Stocks] [50 Patterns] [Jan 8, 2026] │
│                                             │
│  📈 Top 50 Composite Scores                │
│  ├─ stock_analysis_NYSE_2026_01_08.csv    │
│  ├─ stock_analysis_NASDAQ_2026_01_08.csv  │
│  └─ stock_analysis_AMEX_2026_01_08.csv    │
│                                             │
│  📉 Pattern Analysis                       │
│  ├─ CupHandle_patterns_2026_01_08.txt     │
│  └─ Spoon_patterns_2026_01_08.txt         │
└─────────────────────────────────────────────┘
```

---

**Last Updated:** January 8, 2026

**Quick Start:** `./setup_github_pages.sh`
