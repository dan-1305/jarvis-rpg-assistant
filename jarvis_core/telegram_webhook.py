import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import logging
from jarvis_core.config import Config

logger = logging.getLogger(__name__)

class TelegramWebhookBot:
    """
    Telegram bot với hỗ trợ webhook cho deployment trên Render/Heroku
    """
    
    def __init__(self):
        self.config = Config()
        self.token = self.config.get("TELEGRAM_BOT_TOKEN")
        self.webhook_url = self.config.get("WEBHOOK_URL", "")
        self.use_webhook = self.config.get("USE_WEBHOOK", "false").lower() == "true"
        self.port = int(self.config.get("PORT", "8443"))
        
        if not self.token:
            raise ValueError("TELEGRAM_BOT_TOKEN not configured")
        
        self.application = Application.builder().token(self.token).build()
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup command and message handlers"""
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        await update.message.reply_text(
            "👋 Xin chào! Tôi là Jarvis RPG Assistant.\n"
            "Sử dụng /help để xem danh sách lệnh."
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
🤖 <b>Jarvis RPG Assistant Commands</b>

/start - Khởi động bot
/help - Hiển thị trợ giúp
/stats - Xem thống kê của bạn
/tasks - Xem danh sách nhiệm vụ
/learn - Học từ vựng mới

📝 Bạn cũng có thể gửi tin nhắn thường để chat với AI!
        """
        await update.message.reply_text(help_text, parse_mode='HTML')
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular text messages"""
        user_message = update.message.text
        logger.info(f"Received message from {update.effective_user.id}: {user_message}")
        
        await update.message.reply_text(f"Bạn đã nói: {user_message}")
    
    def run_polling(self):
        """Run bot with polling (for local development)"""
        logger.info("Starting bot with polling mode...")
        self.application.run_polling()
    
    async def setup_webhook(self):
        """Setup webhook for production deployment"""
        if not self.webhook_url:
            raise ValueError("WEBHOOK_URL not configured for webhook mode")
        
        webhook_path = f"{self.webhook_url}/webhook/{self.token}"
        
        await self.application.bot.set_webhook(
            url=webhook_path,
            drop_pending_updates=True
        )
        logger.info(f"Webhook set to: {webhook_path}")
    
    def run_webhook(self, listen="0.0.0.0"):
        """Run bot with webhook (for production)"""
        logger.info(f"Starting bot with webhook mode on port {self.port}...")
        
        import asyncio
        asyncio.run(self.setup_webhook())
        
        self.application.run_webhook(
            listen=listen,
            port=self.port,
            url_path=f"webhook/{self.token}",
            webhook_url=f"{self.webhook_url}/webhook/{self.token}"
        )
    
    def run(self):
        """Run bot with appropriate mode based on configuration"""
        if self.use_webhook:
            self.run_webhook()
        else:
            self.run_polling()


def main():
    """Main entry point"""
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    
    bot = TelegramWebhookBot()
    bot.run()


if __name__ == '__main__':
    main()
