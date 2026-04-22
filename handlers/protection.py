# ═══════════════════════════════════════════════════════════════
# Geo Protection Bot - Protection Handlers
# ═══════════════════════════════════════════════════════════════

from pyrogram import Client, filters
from pyrogram.types import Message, ChatMemberUpdated, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ChatType
from datetime import datetime
import logging

from config.config import config
from database.database import db
from database.cache import cache
from utils.decorators import admin_only, handle_errors, log_command
from utils.helpers import (
    is_spam, is_scam, contains_url, get_username, 
    extract_urls, format_duration, get_mention
)
from i18n.translations import get_text

logger = logging.getLogger(__name__)


class ProtectionHandlers:
    """Handle all protection-related commands and events"""
    
    def __init__(self, app: Client):
        self.app = app
        self._register_handlers()
    
    def _register_handlers(self):
        """Register message handlers"""
        # Anti-spam commands
        @self.app.on_message(filters.command("antispam") & filters.group)
        @log_command
        @handle_errors
        async def antispam_handler(client, message: Message):
            await self.handle_antispam(client, message)
        
        @self.app.on_message(filters.command("antiflood") & filters.group)
        @log_command
        @handle_errors
        async def antiflood_handler(client, message: Message):
            await self.handle_antiflood(client, message)
        
        @self.app.on_message(filters.command("antibot") & filters.group)
        @log_command
        @handle_errors
        async def antibot_handler(client, message: Message):
            await self.handle_antibot(client, message)
        
        @self.app.on_message(filters.command("antiraid") & filters.group)
        @log_command
        @handle_errors
        async def antiraid_handler(client, message: Message):
            await self.handle_antiraid(client, message)
        
        @self.app.on_message(filters.command("antiscam") & filters.group)
        @log_command
        @handle_errors
        async def antiscam_handler(client, message: Message):
            await self.handle_antiscam(client, message)
        
        @self.app.on_message(filters.command("antiporn") & filters.group)
        @log_command
        @handle_errors
        async def antiporn_handler(client, message: Message):
            await self.handle_antiporn(client, message)
        
        # Protection settings
        @self.app.on_message(filters.command("setantispamtime") & filters.group)
        @admin_only
        @log_command
        @handle_errors
        async def set_antispam_time_handler(client, message: Message):
            await self.handle_set_antispam_time(client, message)
        
        @self.app.on_message(filters.command("setfloodtime") & filters.group)
        @admin_only
        @log_command
        @handle_errors
        async def set_flood_time_handler(client, message: Message):
            await self.handle_set_flood_time(client, message)
        
        # Auto-protection checks
        @self.app.on_message(filters.group)
        async def check_protection(client, message: Message):
            await self.check_all_protections(client, message)
        
        # Welcome/Goodbye handlers
        @self.app.on_chat_member_updated()
        async def member_update_handler(client, update: ChatMemberUpdated):
            await self.handle_member_update(client, update)
    
    async def handle_antispam(self, client: Client, message: Message):
        """Toggle anti-spam protection"""
        chat_id = message.chat.id
        settings = await db.get_group_settings(chat_id)
        
        if not settings:
            settings = await self.create_default_settings(chat_id)
        
        # Toggle
        settings.antispam_enabled = not settings.antispam_enabled
        await db.save_group_settings(settings)
        
        status = get_text("antispam_enabled" if settings.antispam_enabled else "antispam_disabled")
        await message.reply_text(f"🛡️ {status}", disable_notification=True)
    
    async def handle_antiflood(self, client: Client, message: Message):
        """Toggle anti-flood protection"""
        chat_id = message.chat.id
        settings = await db.get_group_settings(chat_id)
        
        if not settings:
            settings = await self.create_default_settings(chat_id)
        
        settings.flood_enabled = not settings.flood_enabled
        await db.save_group_settings(settings)
        
        status = get_text("antiflood_enabled" if settings.flood_enabled else "antiflood_disabled")
        await message.reply_text(f"🛡️ {status}", disable_notification=True)
    
    async def handle_antibot(self, client: Client, message: Message):
        """Toggle anti-bot protection"""
        chat_id = message.chat.id
        settings = await db.get_group_settings(chat_id)
        
        if not settings:
            settings = await self.create_default_settings(chat_id)
        
        # Toggle in cache (using lock_antibot as proxy)
        current = await cache.get(f"antibot:{chat_id}")
        new_value = not (current or settings.lock_spam)
        await cache.set(f"antibot:{chat_id}", new_value, ex=86400)
        
        status = get_text("antibot_enabled" if new_value else "antibot_disabled")
        await message.reply_text(f"🛡️ {status}", disable_notification=True)
    
    async def handle_antiraid(self, client: Client, message: Message):
        """Toggle anti-raid protection"""
        chat_id = message.chat.id
        settings = await db.get_group_settings(chat_id)
        
        if not settings:
            settings = await self.create_default_settings(chat_id)
        
        settings.raid_protection_enabled = not settings.raid_protection_enabled
        await db.save_group_settings(settings)
        
        status = get_text("antiraid_enabled" if settings.raid_protection_enabled else "antiraid_disabled")
        await message.reply_text(f"🛡️ {status}", disable_notification=True)
    
    async def handle_antiscam(self, client: Client, message: Message):
        """Toggle anti-scam protection"""
        chat_id = message.chat.id
        settings = await db.get_group_settings(chat_id)
        
        if not settings:
            settings = await self.create_default_settings(chat_id)
        
        # Toggle in cache
        current = await cache.get(f"antiscam:{chat_id}")
        new_value = not (current or False)
        await cache.set(f"antiscam:{chat_id}", new_value, ex=86400)
        
        status = get_text("antiscam_enabled" if new_value else "antiscam_disabled")
        await message.reply_text(f"🛡️ {status}", disable_notification=True)
    
    async def handle_antiporn(self, client: Client, message: Message):
        """Toggle anti-porn filter"""
        chat_id = message.chat.id
        settings = await db.get_group_settings(chat_id)
        
        if not settings:
            settings = await self.create_default_settings(chat_id)
        
        # Toggle in cache
        current = await cache.get(f"antiporn:{chat_id}")
        new_value = not (current or False)
        await cache.set(f"antiporn:{chat_id}", new_value, ex=86400)
        
        status = get_text("antiporn_enabled" if new_value else "antiporn_disabled")
        await message.reply_text(f"🛡️ {status}", disable_notification=True)
    
    async def handle_set_antispam_time(self, client: Client, message: Message):
        """Set anti-spam time window"""
        args = message.text.split()[1:]
        
        if not args:
            await message.reply_text("Usage: /setantispamtime <seconds>")
            return
        
        try:
            seconds = int(args[0])
            if seconds < 1 or seconds > 1000:
                await message.reply_text("Time must be between 1 and 1000 seconds")
                return
            
            chat_id = message.chat.id
            settings = await db.get_group_settings(chat_id)
            
            if not settings:
                settings = await self.create_default_settings(chat_id)
            
            settings.antispam_time = seconds
            await db.save_group_settings(settings)
            
            await message.reply_text(
                f"🕐 Anti-Spam time set to {seconds} seconds",
                disable_notification=True
            )
        except ValueError:
            await message.reply_text("Invalid time format!")
    
    async def handle_set_flood_time(self, client: Client, message: Message):
        """Set flood check time window"""
        args = message.text.split()[1:]
        
        if not args:
            await message.reply_text("Usage: /setfloodtime <seconds>")
            return
        
        try:
            seconds = int(args[0])
            if seconds < 1 or seconds > 100:
                await message.reply_text("Time must be between 1 and 100 seconds")
                return
            
            chat_id = message.chat.id
            settings = await db.get_group_settings(chat_id)
            
            if not settings:
                settings = await self.create_default_settings(chat_id)
            
            settings.flood_time = seconds
            await db.save_group_settings(settings)
            
            await message.reply_text(
                f"🕐 Anti-Flood time set to {seconds} seconds",
                disable_notification=True
            )
        except ValueError:
            await message.reply_text("Invalid time format!")
    
    async def check_all_protections(self, client: Client, message: Message):
        """Check all protections for a message"""
        # Skip if from admin
        try:
            member = await client.get_chat_member(message.chat.id, message.from_user.id)
            if member.status in ['creator', 'administrator']:
                return
        except:
            pass
        
        chat_id = message.chat.id
        settings = await db.get_group_settings(chat_id)
        
        if not settings:
            return
        
        text = message.text or ""
        user_id = message.from_user.id
        
        # Anti-Spam check
        if settings.antispam_enabled and is_spam(text):
            await self.handle_spam_violation(client, message)
            return
        
        # Anti-Scam check
        if await cache.get(f"antiscam:{chat_id}") and is_scam(text):
            await self.handle_scam_violation(client, message)
            return
        
        # Anti-Porn check (basic pattern matching)
        if await cache.get(f"antiporn:{chat_id}") and self.check_nsfw_content(message):
            await self.handle_porn_violation(client, message)
            return
        
        # Anti-Flood check
        if settings.flood_enabled:
            is_flooding = await cache.check_flood(
                user_id, chat_id, 
                limit=5, 
                window=settings.flood_time
            )
            if not is_flooding:
                await self.handle_flood_violation(client, message)
                return
        
        # Link lock check
        if settings.lock_links and contains_url(text):
            await self.handle_link_violation(client, message)
            return
        
        # Filtered words check
        filtered_words = await db.get_filtered_words(chat_id)
        if filtered_words:
            text_lower = text.lower()
            for word in filtered_words:
                if word.lower() in text_lower:
                    await self.handle_filtered_word(client, message, word)
                    return
    
    async def handle_spam_violation(self, client: Client, message: Message):
        """Handle spam violation"""
        try:
            await message.delete()
            await client.restrict_chat_member(
                message.chat.id,
                message.from_user.id,
                until_date=datetime.now().timestamp() + 300
            )
            await message.reply_text(
                f"🚫 {get_mention(message.from_user)} spam detected! Muted for 5 minutes.",
                disable_notification=True
            )
        except Exception as e:
            logger.error(f"Error handling spam: {e}")
    
    async def handle_scam_violation(self, client: Client, message: Message):
        """Handle scam violation"""
        try:
            await message.delete()
            await client.ban_chat_member(message.chat.id, message.from_user.id)
            await message.reply_text(
                f"🚨 {get_mention(message.from_user)} scam content detected! User banned.",
                disable_notification=True
            )
        except Exception as e:
            logger.error(f"Error handling scam: {e}")
    
    async def handle_porn_violation(self, client: Client, message: Message):
        """Handle NSFW content violation"""
        try:
            await message.delete()
            await client.restrict_chat_member(
                message.chat.id,
                message.from_user.id,
                until_date=datetime.now().timestamp() + 3600
            )
            await message.reply_text(
                f"🔞 {get_mention(message.from_user)} NSFW content detected! Muted for 1 hour.",
                disable_notification=True
            )
        except Exception as e:
            logger.error(f"Error handling NSFW: {e}")
    
    async def handle_flood_violation(self, client: Client, message: Message):
        """Handle flood violation"""
        try:
            await client.restrict_chat_member(
                message.chat.id,
                message.from_user.id,
                until_date=datetime.now().timestamp() + 60
            )
            await message.reply_text(
                f"🌊 {get_mention(message.from_user)} flooding detected! Muted for 1 minute.",
                disable_notification=True
            )
        except Exception as e:
            logger.error(f"Error handling flood: {e}")
    
    async def handle_link_violation(self, client: Client, message: Message):
        """Handle link violation"""
        try:
            await message.delete()
            await message.reply_text(
                f"🔗 {get_mention(message.from_user)} links are not allowed in this chat!",
                disable_notification=True
            )
        except Exception as e:
            logger.error(f"Error handling link: {e}")
    
    async def handle_filtered_word(self, client: Client, message: Message, word: str):
        """Handle filtered word violation"""
        try:
            await message.delete()
            await message.reply_text(
                f"🚫 {get_mention(message.from_user)} filtered word detected: {word}",
                disable_notification=True
            )
        except Exception as e:
            logger.error(f"Error handling filtered word: {e}")
    
    def check_nsfw_content(self, message: Message) -> bool:
        """Check if message contains NSFW content"""
        text = message.text or ""
        nsfw_patterns = [
            r'(?i)\b(porn|nsfw|nude|naked|sex)\b',
            r'(?i)\b(pussy|dick|cock|ass)\b',
            r'(?i)\b(xxx|hardcore|erotic)\b',
        ]
        
        import re
        for pattern in nsfw_patterns:
            if re.search(pattern, text):
                return True
        
        # Check for media
        if message.photo or message.video or message.document:
            return True
        
        return False
    
    async def handle_member_update(self, client: Client, update: ChatMemberUpdated):
        """Handle member updates (join/leave)"""
        if not update.new_chat_member:
            return
        
        chat_id = update.chat.id
        new_member = update.new_chat_member
        
        # Check if it's a join
        if new_member.status == "member":
            settings = await db.get_group_settings(chat_id)
            
            if not settings:
                return
            
            user_id = new_member.user.id
            
            # Anti-Bot check
            antibot = await cache.get(f"antibot:{chat_id}")
            if antibot and new_member.user.is_bot:
                try:
                    await client.ban_chat_member(chat_id, user_id)
                    await update.reply_text(
                        "🤖 Bots are not allowed in this chat!",
                        disable_notification=True
                    )
                except Exception as e:
                    logger.error(f"Error banning bot: {e}")
                return
            
            # Anti-Raid check
            if settings.raid_protection_enabled:
                raid_count = await cache.get(f"raid:{chat_id}") or 0
                await cache.set(f"raid:{chat_id}", raid_count + 1, ex=settings.raid_protection_time)
                
                if raid_count > 10:  # More than 10 joins in window
                    await self.activate_raid_protection(client, update)
            
            # Anti-Global-Ban check
            if await db.is_globally_banned(user_id):
                try:
                    await client.ban_chat_member(chat_id, user_id)
                    await update.reply_text(
                        f"🚫 User is globally banned!",
                        disable_notification=True
                    )
                except Exception as e:
                    logger.error(f"Error banning gban user: {e}")
                return
            
            # Welcome message
            if settings.welcome_enabled:
                await self.send_welcome(client, update, settings)
        
        # Check if it's a leave
        elif new_member.status == "left" or new_member.status == "banned":
            settings = await db.get_group_settings(chat_id)
            
            if settings and settings.goodbye_enabled:
                await self.send_goodbye(client, update, settings)
    
    async def activate_raid_protection(self, client: Client, update: ChatMemberUpdated):
        """Activate raid protection mode"""
        try:
            await update.reply_text(
                "🚨 Raid detected! Enabling maximum protection mode for "
                f"{format_duration(300)}.",
                disable_notification=True
            )
            # Set raid mode for 5 minutes
            await cache.set(f"raid_mode:{update.chat.id}", True, ex=300)
        except Exception as e:
            logger.error(f"Error activating raid protection: {e}")
    
    async def send_welcome(self, client: Client, update: ChatMemberUpdated, settings):
        """Send welcome message"""
        user = update.new_chat_member.user
        message = settings.welcome_message.format(user=get_username(user))
        
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📋 Rules", callback_data=f"rules_{update.chat.id}"),
                InlineKeyboardButton("💡 Help", callback_data=f"help_{update.chat.id}")
            ]
        ])
        
        try:
            await client.send_message(
                update.chat.id,
                message,
                reply_markup=keyboard
            )
        except Exception as e:
            logger.error(f"Error sending welcome: {e}")
    
    async def send_goodbye(self, client: Client, update: ChatMemberUpdated, settings):
        """Send goodbye message"""
        user = update.new_chat_member.user
        message = settings.goodbye_message.format(user=get_username(user))
        
        try:
            await client.send_message(
                update.chat.id,
                message,
                disable_notification=True
            )
        except Exception as e:
            logger.error(f"Error sending goodbye: {e}")
    
    async def create_default_settings(self, chat_id: int):
        """Create default settings for a chat"""
        from database.database import GroupSettings
        
        chat = await self.app.get_chat(chat_id)
        settings = GroupSettings(
            chat_id=chat_id,
            chat_title=chat.title,
            warns_limit=config.defaults.default_warns,
            antispam_time=config.defaults.default_antispam_time,
            flood_time=config.defaults.default_flood_time,
            mute_time=config.defaults.default_mute_time,
            language=config.language.default_language
        )
        await db.save_group_settings(settings)
        return settings