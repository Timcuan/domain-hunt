import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bot configuration
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
IPINFO_TOKEN = os.getenv('IPINFO_TOKEN')

# Validate required environment variables
if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN environment variable is required")

# IPinfo token is optional, but recommended for better rate limits
if not IPINFO_TOKEN:
    print("Warning: IPINFO_TOKEN not set. Using free tier with limited requests.")