import logging
import traceback
from typing import Optional
import asyncio
from telegram import Bot
from jarvis_core.config import Config

logger = logging.getLogger(__name__)

class ErrorNotifier:
    def __init__(self):
        self.config = Config()
        self.bot: Optional[Bot] = None
        self.admin_chat_ids = self._get_admin_chat_ids()
        
    def _get_admin_chat_ids(self):
        admin_ids_str = self.config.get("ADMIN_CHAT_IDS", "")
        if not admin_ids_str:
            return []
        return [int(id.strip()) for id in admin_ids_str.split(",") if id.strip()]
    
    async def _get_bot(self) -> Bot:
        if not self.bot:
            token = self.config.get("TELEGRAM_BOT_TOKEN")
            if not token:
                logger.error("No Telegram bot token configured")
                return None
            self.bot = Bot(token=token)
        return self.bot
    
    async def send_error_alert(self, error: Exception, context: str = "", critical: bool = True):
        if not critical or not self.admin_chat_ids:
            return
            
        bot = await self._get_bot()
        if not bot:
            logger.error("Cannot send alert: bot not initialized")
            return
        
        error_type = type(error).__name__
        error_msg = str(error)
        stack_trace = ''.join(traceback.format_tb(error.__traceback__))
        
        message = f"🚨 <b>CRITICAL ERROR</b>\n\n"
        if context:
            message += f"📍 <b>Context:</b> {context}\n"
        message += f"⚠️ <b>Error Type:</b> {error_type}\n"
        message += f"💬 <b>Message:</b> {error_msg}\n\n"
        message += f"<pre>{stack_trace[:1000]}</pre>"
        
        for chat_id in self.admin_chat_ids:
            try:
                await bot.send_message(
                    chat_id=chat_id,
                    text=message,
                    parse_mode='HTML'
                )
                logger.info(f"Error alert sent to admin {chat_id}")
            except Exception as e:
                logger.error(f"Failed to send error alert to {chat_id}: {e}")
    
    def notify_error_sync(self, error: Exception, context: str = "", critical: bool = True):
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(self.send_error_alert(error, context, critical))
            else:
                loop.run_until_complete(self.send_error_alert(error, context, critical))
        except Exception as e:
            logger.error(f"Failed to notify error: {e}")

error_notifier = ErrorNotifier()
