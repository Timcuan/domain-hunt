# 🤖 DomainIntelBot

A comprehensive Telegram bot for domain intelligence gathering that provides WHOIS data, DNS records, technology stack detection, and IP geolocation information.

## ✨ Features

- **🔍 WHOIS Lookup**: Registrar information, creation/expiration dates, nameservers
- **🌐 DNS Records**: A, MX, NS, and TXT record analysis
- **⚙️ Technology Detection**: Web servers, CMS, JavaScript frameworks, and more
- **📍 IP Intelligence**: Geolocation, ISP, ASN, and hosting provider details
- **⚡ Fast & Async**: Parallel processing for quick results
- **🎯 Smart Formatting**: Clean, markdown-formatted responses

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8 or higher
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- IPinfo API Token (optional, for better rate limits)

### 2. Installation

```bash
# Clone or create the project directory
cd telegram-bot

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your tokens
nano .env
```

Add your tokens to `.env`:
```env
TELEGRAM_TOKEN=your_telegram_bot_token_here
IPINFO_TOKEN=your_ipinfo_token_here
```

### 4. Run the Bot

```bash
python bot.py
```

## 🎮 Bot Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/start` | Welcome message and bot introduction | `/start` |
| `/help` | Show available commands and usage | `/help` |
| `/check <domain>` | Analyze domain information | `/check google.com` |

## 📊 Sample Output

When you run `/check google.com`, you'll get:

```
🔍 WHOIS
Registrar: MarkMonitor Inc.
Creation: 1997-09-15
Expiry: 2028-09-14
Nameservers: ns1.google.com, ns2.google.com

🌐 DNS Records
A: 172.217.164.142
MX: smtp.google.com (priority: 10)
NS: ns1.google.com, ns2.google.com
TXT: "v=spf1 include:_spf.google.com ~all"

⚙️ Tech Stack
Web Server: gws
Languages: Go

📍 IP Info
IP: 172.217.164.142
Country: US
City: Mountain View
ISP: AS15169 Google LLC
```

## 🛠️ Dependencies

- `python-telegram-bot`: Telegram Bot API wrapper
- `python-whois`: WHOIS data retrieval
- `dnspython`: DNS record queries
- `builtwith`: Technology stack detection
- `ipinfo`: IP geolocation and intelligence
- `python-dotenv`: Environment variable management

## 🔧 Configuration Options

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `TELEGRAM_TOKEN` | ✅ Yes | Your Telegram bot token from BotFather |
| `IPINFO_TOKEN` | ❌ No | IPinfo API token for better rate limits |

### Getting API Tokens

1. **Telegram Bot Token**:
   - Message [@BotFather](https://t.me/botfather) on Telegram
   - Create a new bot with `/newbot`
   - Copy the provided token

2. **IPinfo Token** (Optional):
   - Sign up at [ipinfo.io](https://ipinfo.io/signup)
   - Free tier provides 50,000 requests/month
   - Copy your access token

## 🔍 How It Works

The bot uses parallel processing to gather information efficiently:

1. **WHOIS Lookup**: Uses `python-whois` to get registration details
2. **DNS Analysis**: Queries A, MX, NS, and TXT records with `dnspython`
3. **Tech Detection**: Analyzes website technologies with `builtwith`
4. **IP Intelligence**: Gets geolocation and hosting info via IPinfo API

All operations run concurrently for optimal performance.

## 🚨 Error Handling

- **Unregistered domains**: Shows "Domain *example.com* belum registered, go own it! 🚀"
- **Invalid domains**: Validates format and provides helpful error messages
- **API failures**: Graceful fallbacks with informative error messages
- **Rate limiting**: Built-in handling for API rate limits

## 🎯 Use Cases

- **Domain Research**: Check domain availability and registration details
- **Security Analysis**: Investigate suspicious domains
- **Infrastructure Mapping**: Understand hosting and DNS configuration
- **Competitive Intelligence**: Analyze competitor technology stacks
- **Due Diligence**: Verify domain ownership and legitimacy

## 🔒 Security & Privacy

- No data storage: All queries are processed in real-time
- No logging of sensitive information
- Rate limiting compliance with all APIs
- Input validation for security

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🆘 Support

If you encounter any issues:

1. Check your environment variables are set correctly
2. Ensure your bot token is valid
3. Verify your internet connection
4. Check the bot logs for error details

For additional help, please open an issue in the repository.

## 🚀 Deployment

### Local Development
```bash
python bot.py
```

### Production Deployment
For production, consider using:
- **Systemd service** for Linux servers
- **Docker containers** for containerized deployment
- **Process managers** like PM2 or Supervisor
- **Cloud platforms** like Heroku, Railway, or DigitalOcean

Example systemd service:
```ini
[Unit]
Description=DomainIntelBot
After=network.target

[Service]
Type=simple
User=botuser
WorkingDirectory=/path/to/telegram-bot
ExecStart=/usr/bin/python3 bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

---

**Made with ❤️ for the cybersecurity and domain research community**