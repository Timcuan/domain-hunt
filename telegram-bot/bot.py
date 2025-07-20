import logging
import asyncio
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.constants import ParseMode
from domain_checker import DomainChecker
from config import TELEGRAM_TOKEN

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class DomainIntelBot:
    def __init__(self):
        self.domain_checker = DomainChecker()
        self.application = Application.builder().token(TELEGRAM_TOKEN).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup command handlers"""
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("check", self.check_command))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        welcome_message = """
🤖 *Welcome to DomainIntelBot!*

I can help you gather comprehensive information about any domain including:
• 🔍 WHOIS data (registrar, dates, nameservers)
• 🌐 DNS records (A, MX, NS, TXT)
• ⚙️ Technology stack detection
• 📍 IP geolocation & hosting info

*Usage:*
`/check example.com` - Analyze a domain
`/help` - Show this help message

Let's start exploring! 🚀
        """
        await update.message.reply_text(
            welcome_message, 
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_message = """
🔧 *DomainIntelBot Commands*

`/check <domain>` - Analyze domain information
  Example: `/check google.com`

*What I analyze:*
• 🔍 WHOIS: Registrar, creation/expiry dates, nameservers
• 🌐 DNS Records: A, MX, NS, TXT records
• ⚙️ Tech Stack: Web servers, CMS, frameworks
• 📍 IP Info: Geolocation, ISP, ASN details

*Tips:*
• Use domain name without http:// or www
• Analysis may take 5-10 seconds
• Some data might be unavailable for certain domains

Need help? Contact the developer! 👨‍💻
        """
        await update.message.reply_text(
            help_message,
            parse_mode=ParseMode.MARKDOWN
        )
    
    def validate_domain(self, domain: str) -> str:
        """Validate and clean domain name"""
        # Remove protocol and www
        domain = re.sub(r'^https?://', '', domain)
        domain = re.sub(r'^www\.', '', domain)
        
        # Remove trailing slash
        domain = domain.rstrip('/')
        
        # Basic domain validation
        domain_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
        
        if not re.match(domain_pattern, domain):
            raise ValueError("Invalid domain format")
        
        return domain.lower()
    
    async def check_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /check command"""
        # Check if domain is provided
        if not context.args:
            await update.message.reply_text(
                "❌ Please provide a domain to check.\n"
                "Usage: `/check example.com`",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        domain = ' '.join(context.args)
        
        try:
            # Validate domain
            domain = self.validate_domain(domain)
        except ValueError:
            await update.message.reply_text(
                f"❌ Invalid domain format: `{domain}`\n"
                "Please provide a valid domain name (e.g., example.com)",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # Send "analyzing" message
        status_message = await update.message.reply_text(
            f"🔍 Analyzing domain `{domain}`...\n"
            "This may take a few seconds ⏳",
            parse_mode=ParseMode.MARKDOWN
        )
        
        try:
            # Perform domain analysis
            results = await self.domain_checker.check_domain_async(domain)
            
            # Format and send results
            formatted_message = self.domain_checker.format_results(domain, results)
            
            # Delete status message and send results
            await status_message.delete()
            await update.message.reply_text(
                formatted_message,
                parse_mode=ParseMode.MARKDOWN
            )
            
        except Exception as e:
            logger.error(f"Error checking domain {domain}: {str(e)}")
            await status_message.edit_text(
                f"❌ Error analyzing domain `{domain}`\n"
                "Please try again later or check if the domain is valid.",
                parse_mode=ParseMode.MARKDOWN
            )
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        logger.error(f"Update {update} caused error {context.error}")
        
        if update and update.message:
            await update.message.reply_text(
                "❌ An unexpected error occurred. Please try again later."
            )
    
    def run(self):
        """Start the bot"""
        # Add error handler
        self.application.add_error_handler(self.error_handler)
        
        logger.info("Starting DomainIntelBot...")
        print("🤖 DomainIntelBot is starting...")
        print("Press Ctrl+C to stop the bot")
        
        # Run the bot
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

def main():
    """Main function"""
    try:
        bot = DomainIntelBot()
        bot.run()
    except KeyboardInterrupt:
        print("\n👋 Bot stopped gracefully")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"❌ Fatal error: {e}")

if __name__ == "__main__":
    main()