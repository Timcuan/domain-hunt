#!/bin/bash

# DomainIntelBot Runner Script
# This script sets up and runs the Telegram bot

echo "🤖 Starting DomainIntelBot..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from template..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "📝 Please edit .env file with your tokens:"
        echo "   - TELEGRAM_TOKEN (required)"
        echo "   - IPINFO_TOKEN (optional)"
        echo "Then run this script again."
        exit 1
    else
        echo "❌ .env.example not found. Please create .env file manually."
        exit 1
    fi
fi

# Check if virtual environment exists, create if not
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Check if TELEGRAM_TOKEN is set
if grep -q "your_telegram_bot_token_here" .env; then
    echo "❌ Please set your TELEGRAM_TOKEN in .env file"
    echo "Get your token from @BotFather on Telegram"
    exit 1
fi

# Run the bot
echo "🚀 Starting bot..."
python bot.py