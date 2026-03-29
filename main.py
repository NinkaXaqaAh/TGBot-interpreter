import asyncio
import logging
import signal
import sys
from aiogram import Bot, Dispatcher
from app.config import config
from app.handlers import translation

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

bot_instance = None

async def notify_admin(text: str):
    if config.admin_chat_id:
        try:
            bot = Bot(token=config.bot_token.get_secret_value())
            await bot.send_message(config.admin_chat_id, text)
            await bot.session.close()
        except Exception as e:
            logger.error(f"Failed to notify admin: {e}")

async def main():
    global bot_instance
    
    logger.info("Bot starting...")
    await notify_admin("🚀 Bot started")
    
    bot_instance = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()
    dp.include_router(translation.router)

    try:
        await dp.start_polling(bot_instance)
    finally:
        await bot_instance.session.close()

def signal_handler(signum, frame):
    logger.info(f"Received signal {signum}, shutting down...")
    if bot_instance:
        asyncio.create_task(bot_instance.session.close())
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed: {e}", exc_info=True)
        asyncio.run(notify_admin(f"⚠️ Bot crashed:\n{e}"))
        sys.exit(1)
