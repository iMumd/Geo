# ═══════════════════════════════════════════════════════════════
# Geo Protection Bot - Core Bot
# ═══════════════════════════════════════════════════════════════

import asyncio
import logging
import sys
from typing import Optional
from pyrogram import Client, filters
from pyrogram.types import Message

from config.config import config
from database.database import db
from database.cache import cache

logger = logging.getLogger(__name__)

# Global bot uptime tracker
_bot_start_time: float = 0


def set_bot_start_time(t: float):
    """Set bot start time from bot.py"""
    global _bot_start_time
    _bot_start_time = t


def get_uptime() -> int:
    """Get bot uptime in seconds"""
    return int(asyncio.get_event_loop().time() - _bot_start_time) if _bot_start_time else 0


class GeoBot:
    """Main Geo Protection Bot class"""
    
    def __init__(self):
        self.app: Optional[Client] = None
        self._running = False
        self.start_time = 0
    
    async def initialize(self):
        """Initialize bot and all components"""
        logger.info("=" * 60)
        logger.info("  Geo Protection Bot - Initializing...")
        logger.info("=" * 60)
        
        # Validate configuration
        try:
            config.validate()
            logger.info("✓ Configuration validated")
        except ValueError as e:
            logger.error(f"Configuration error: {e}")
            raise
        
        # Initialize database
        try:
            await db.initialize()
            logger.info("✓ Database initialized")
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise
        
        # Initialize cache
        try:
            await cache.connect()
            logger.info("✓ Cache connected")
        except Exception as e:
            logger.warning(f"Cache connection failed (running without cache): {e}")
        
        # Validate configuration
        try:
            config.validate()
            logger.info("✓ Configuration validated")
        except ValueError as e:
            logger.error(f"Configuration error: {e}")
            raise
        
        # Initialize database
        try:
            await db.initialize()
            logger.info("✓ Database initialized")
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise
        
        # Initialize cache
        try:
            await cache.connect()
            logger.info("✓ Cache connected")
        except Exception as e:
            logger.warning(f"Cache connection failed (running without cache): {e}")
        
        # Initialize Pyrogram client
        self.app = Client(
            name=config.bot.username,
            api_id=config.telegram.api_id,
            api_hash=config.telegram.api_hash,
            bot_token=config.bot.token,
            plugins=dict(
                root="plugins"
            ),
            workdir=".",
            app_version=config.telegram.app_version,
            device_model=config.telegram.device_model,
            lang_code=config.telegram.lang_code,
        )
        
        logger.info(f"✓ Bot client created: {config.bot.name} (@{config.bot.username})")
        
        # Load handlers
        await self.load_handlers()
        
        logger.info("✓ Handlers loaded")
        logger.info("=" * 60)
        logger.info("  Geo Protection Bot - Ready!")
        logger.info("=" * 60)
        
        # Set bot start time for uptime tracking
        self.start_time = asyncio.get_event_loop().time()
        
        self._running = True
    
    async def load_handlers(self):
        """Load all command handlers"""
        from handlers.protection import ProtectionHandlers
        from handlers.admin import AdminHandlers
        from handlers.moderation import ModerationHandlers
        from handlers.user import UserHandlers
        from handlers.godmode import GodModeHandler
        
        # Initialize handlers
        ProtectionHandlers(self.app)
        AdminHandlers(self.app)
        ModerationHandlers(self.app)
        UserHandlers(self.app)
        GodModeHandler(self.app)
        
        # Global error handler
        @self.app.on_message(filters.command("error"))
        async def error_test(client, message: Message):
            raise Exception("Test error for error handling")
        
        # Version command
        @self.app.on_message(filters.command("version"))
        async def version_handler(client, message: Message):
            await message.reply_text(
                f"**{config.bot.name}** Version 1.0.0\n"
                f"Status: **{config.bot.god_status}** Edition"
            )
        
        # Load callback handlers
        from handlers.callbacks import CallbackHandlers
        CallbackHandlers(self.app)
    
    async def start(self):
        """Start the bot"""
        try:
            await self.app.start()
            logger.info(f"✓ Bot started successfully")
            
            # Send startup notification to developer
            if config.bot.god_mode and config.bot.developer_id:
                try:
                    await self.app.send_message(
                        config.bot.developer_id,
                        f"🤖 **{config.bot.name}** is now online!\n\n"
                        f"🌟 Edition: {config.bot.god_status}\n"
                        f"👥 Workers: {config.performance.workers}\n"
                        f"💾 Database: {config.database.url.split('///')[-1]}"
                    )
                except Exception as e:
                    logger.warning(f"Could not notify developer: {e}")
            
            # Run idle
            logger.info("Bot is running. Press Ctrl+C to stop.")
            await self.idle()
            
        except Exception as e:
            logger.error(f"Error starting bot: {e}")
            raise
    
    async def stop(self):
        """Stop the bot"""
        logger.info("Stopping bot...")
        
        self._running = False
        
        if self.app:
            await self.app.stop()
            logger.info("✓ Bot stopped")
        
        await db.close()
        logger.info("✓ Database closed")
        
        await cache.disconnect()
        logger.info("✓ Cache disconnected")
        
        logger.info("=" * 60)
        logger.info("  Geo Protection Bot - Stopped")
        logger.info("=" * 60)
    
    async def idle(self):
        """Keep the bot running"""
        try:
            while self._running:
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            pass


# Global bot instance
bot = GeoBot()


async def main():
    """Main entry point"""
    # Configure logging with Unicode support
    logging.basicConfig(
        level=getattr(logging, config.logging.level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(config.logging.file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    # Fix StreamHandler encoding for Windows
    for handler in logging.root.handlers:
        if isinstance(handler, logging.StreamHandler):
            handler.stream = sys.stdout
    
    try:
        await bot.initialize()
        await bot.start()
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
    finally:
        await bot.stop()


if __name__ == "__main__":
    asyncio.run(main())