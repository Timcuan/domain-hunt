# 🚀 Quick Start Guide

Get your DomainIntelBot running in 5 minutes!

## 1. Get Telegram Bot Token

1. Open Telegram and message [@BotFather](https://t.me/botfather)
2. Send `/newbot`
3. Choose a name for your bot (e.g., "My Domain Intel Bot")
4. Choose a username (e.g., "mydomainintelbot")
5. Copy the token you receive

## 2. Setup Environment

```bash
# Copy environment template
cp .env.example .env

# Edit with your token
nano .env
```

Add your token:
```env
TELEGRAM_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
IPINFO_TOKEN=your_ipinfo_token_here  # Optional
```

## 3. Run the Bot

### Option A: Using the run script (Recommended)
```bash
./run.sh
```

### Option B: Manual setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run the bot
python bot.py
```

### Option C: Using Docker
```bash
# Build and run
docker-compose up --build
```

## 4. Test Your Bot

1. Open Telegram
2. Search for your bot username
3. Send `/start` to begin
4. Try `/check google.com`

## 🎯 Commands

- `/start` - Welcome message
- `/help` - Show help  
- `/check <domain>` - Analyze domain

## 🔧 Troubleshooting

**"TELEGRAM_TOKEN not set"**
→ Make sure you edited the `.env` file with your real token

**"Module not found"**
→ Run `pip install -r requirements.txt`

**"Permission denied: ./run.sh"**
→ Run `chmod +x run.sh`

## ✅ Success!

If you see "🤖 DomainIntelBot is starting..." - you're ready to go!

Your bot will now respond to domain analysis requests in Telegram.

---

For detailed documentation, see [README.md](README.md)