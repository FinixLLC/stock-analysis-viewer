# Deploy to Cloud VM (DigitalOcean/AWS/Linode)

## 🎯 Overview

Deploy your stock analysis viewer to a cloud VM with automatic updates.

**Cost:** ~$5-10/month
**Time:** 30 minutes setup
**Features:** Full control, can connect to MongoDB, auto-sync

---

## 📋 Prerequisites

1. Cloud VM account (DigitalOcean recommended for simplicity)
2. Domain name (optional, can use IP address)
3. SSH access to your VM

---

## 🚀 Step-by-Step Setup

### **1. Create Cloud VM**

**DigitalOcean:**
```bash
# Create a $6/mo droplet
# OS: Ubuntu 24.04 LTS
# Size: 1 GB RAM, 1 vCPU
# Region: Closest to you
```

**AWS Lightsail:**
```bash
# Create $5/mo instance
# Platform: Linux/Unix
# Blueprint: Ubuntu 24.04 LTS
```

### **2. SSH into VM**

```bash
ssh root@YOUR_VM_IP
```

### **3. Install Required Software**

```bash
# Update system
apt update && apt upgrade -y

# Install nginx (web server)
apt install -y nginx

# Install Python (for scripts)
apt install -y python3 python3-pip

# Install rsync (for file sync)
apt install -y rsync
```

### **4. Configure Nginx**

```bash
# Edit nginx config
nano /etc/nginx/sites-available/stock-analysis

# Add this configuration:
```

```nginx
server {
    listen 80;
    server_name YOUR_DOMAIN_OR_IP;

    root /var/www/stock-analysis;
    index index.html;

    location / {
        autoindex on;  # Directory listing
        autoindex_exact_size off;
        autoindex_localtime on;
        charset utf-8;
    }

    # Protect sensitive files
    location ~ \.(sh|py|ini|log)$ {
        deny all;
    }

    # Allow CSV downloads
    location ~ \.csv$ {
        add_header Content-Type text/csv;
        add_header Content-Disposition 'attachment';
    }
}
```

```bash
# Enable site
ln -s /etc/nginx/sites-available/stock-analysis /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/default

# Test config
nginx -t

# Restart nginx
systemctl restart nginx
```

### **5. Create Web Directory**

```bash
mkdir -p /var/www/stock-analysis
chown -R www-data:www-data /var/www/stock-analysis
```

### **6. Set Up Auto-Sync from Your Mac**

**On your Mac, create sync script:**

```bash
# File: ~/sync_to_cloud.sh
#!/bin/bash

VM_IP="YOUR_VM_IP"
VM_USER="root"
LOCAL_DIR="/Volumes/1T_ExFAT/StockScan/devcpp/Sarah2/"
REMOTE_DIR="/var/www/stock-analysis/"

echo "📤 Syncing to cloud VM..."

rsync -avz --delete \
  --include='Top50/***' \
  --include='Patterns/***' \
  --include='Top/***' \
  --include='scripts/*.md' \
  --exclude='*' \
  "$LOCAL_DIR" "$VM_USER@$VM_IP:$REMOTE_DIR"

echo "✅ Sync complete!"
echo "🌐 View at: http://$VM_IP"
```

```bash
chmod +x ~/sync_to_cloud.sh

# Run manually or add to cron
# crontab -e
# 0 18 * * * /Users/yancheng/sync_to_cloud.sh  # Sync daily at 6 PM
```

### **7. Optional: Add HTTPS (Let's Encrypt)**

```bash
# Install certbot
apt install -y certbot python3-certbot-nginx

# Get SSL certificate (requires domain name)
certbot --nginx -d your-domain.com

# Auto-renewal
certbot renew --dry-run
```

---

## 🔒 Security Enhancements

### **Add Basic Authentication**

```bash
# Install apache2-utils
apt install -y apache2-utils

# Create password file
htpasswd -c /etc/nginx/.htpasswd your_username

# Update nginx config
nano /etc/nginx/sites-available/stock-analysis
```

Add inside `location /` block:
```nginx
auth_basic "Stock Analysis";
auth_basic_user_file /etc/nginx/.htpasswd;
```

```bash
systemctl restart nginx
```

---

## 📊 Monitor Usage

```bash
# Check nginx logs
tail -f /var/log/nginx/access.log

# Check disk usage
df -h

# Check system resources
htop
```

---

## 🔄 Daily Workflow

**After running stock_analysis on your Mac:**

```bash
# Sync to cloud
~/sync_to_cloud.sh

# View online
open http://YOUR_VM_IP
```

---

## 💰 Cost Breakdown

| Provider | Specs | Cost |
|----------|-------|------|
| DigitalOcean | 1GB RAM, 25GB SSD | $6/month |
| AWS Lightsail | 512MB RAM, 20GB SSD | $3.50/month |
| Linode | 1GB RAM, 25GB SSD | $5/month |
| Domain (optional) | .com domain | $12/year |

**Total:** ~$5-10/month

---

## 🎯 Benefits

✅ Full control over server
✅ Can access MongoDB remotely
✅ Custom domain support
✅ HTTPS/SSL support
✅ Password protection
✅ Auto-sync from your Mac
✅ Always online (24/7)

---

## 🆘 Troubleshooting

**Nginx won't start:**
```bash
nginx -t  # Check config errors
systemctl status nginx
```

**Permission denied:**
```bash
chown -R www-data:www-data /var/www/stock-analysis
chmod -R 755 /var/www/stock-analysis
```

**Can't connect:**
```bash
# Check firewall
ufw allow 80
ufw allow 443
```

---

**Last Updated:** January 8, 2026
