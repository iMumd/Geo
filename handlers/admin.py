# ═══════════════════════════════════════════════════════════════
# Geo Protection Bot - Admin Handlers
# ═══════════════════════════════════════════════════════════════

from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.enums import ChatType
from datetime import datetime, timedelta
import logging

from config.config import config
from database.database import db
from utils.decorators import admin_only, handle_errors, log_command, requires_args
from utils.helpers import (
    get_mention, get_username, parse_user_id, parse_duration,
    format_duration, get_timestamp, format_timestamp
)
from i18n.translations import get_text

logger = logging.getLogger(__name__)


class AdminHandlers:
    """Handle all admin-related commands"""
    
    def __init__(self, app: Client):
        self.app = app
        self._register_handlers()
        self._register_callbacks()
    
    def _register_handlers(self):
        """Register command handlers"""
        
        # Ban/Unban commands
        @self.app.on_message(filters.command("ban") & filters.group)
        @admin_only
        @log_command
        @handle_errors
        async def ban_handler(client, message: Message):
            await self.handle_ban(client, message)
        
        @self.app.on_message(filters.command("unban") & filters.group)
        @admin_only
        @log_command
        @handle_errors
        async def unban_handler(client, message: Message):
            await self.handle_unban(client, message)
        
        # Kick command
        @self.app.on_message(filters.command("kick") & filters.group)
        @admin_only
        @log_command
        @handle_errors
        async def kick_handler(client, message: Message):
            await self.handle_kick(client, message)
        
        # Mute commands
        @self.app.on_message(filters.command("mute") & filters.group)
        @admin_only
        @log_command
        @handle_errors
        async def mute_handler(client, message: Message):
            await self.handle_mute(client, message)
        
        @self.app.on_message(filters.command("unmute") & filters.group)
        @admin_only
        @log_command
        @handle_errors
        async def unmute_handler(client, message: Message):
            await self.handle_unmute(client, message)
        
        @self.app.on_message(filters.command("tmute") & filters.group)
        @admin_only
        @log_command
        @handle_errors
        async def tmute_handler(client, message: Message):
            await self.handle_tmute(client, message)
        
        # Warn commands
        @self.app.on_message(filters.command("warn") & filters.group)
        @admin_only
        @log_command
        @handle_errors
        async def warn_handler(client, message: Message):
            await self.handle_warn(client, message)
        
        @self.app.on_message(filters.command("dwarn") & filters.group)
        @admin_only
        @log_command
        @handle_errors
        async def dwarn_handler(client, message: Message):
            await self.handle_dwarn(client, message)
        
        @self.app.on_message(filters.command("warns") & filters.group)
        @log_command
        @handle_errors
        async def warns_handler(client, message: Message):
            await self.handle_warns(client, message)
        
        @self.app.on_message(filters.command("resetwarns") & filters.group)
        @admin_only
        @log_command
        @handle_errors
        async def resetwarns_handler(client, message: Message):
            await self.handle_resetwarns(client, message)
        
        # Pin/Unpin commands
        @self.app.on_message(filters.command("pin") & filters.group)
        @admin_only
        @log_command
        @handle_errors
        async def pin_handler(client, message: Message):
            await self.handle_pin(client, message)
        
        @self.app.on_message(filters.command("unpin") & filters.group)
        @admin_only
        @log_command
        @handle_errors
        async def unpin_handler(client, message: Message):
            await self.handle_unpin(client, message)
        
        # Purge command
        @self.app.on_message(filters.command("purge") & filters.group)
        @admin_only
        @log_command
        @handle_errors
        async def purge_handler(client, message: Message):
            await self.handle_purge(client, message)
        
        # Set welcome/goodbye
        @self.app.on_message(filters.command("setwelcome") & filters.group)
        @admin_only
        @log_command
        @handle_errors
        async def set_welcome_handler(client, message: Message):
            await self.handle_set_welcome(client, message)
        
        @self.app.on_message(filters.command("setgoodbye") & filters.group)
        @admin_only
        @log_command
        @handle_errors
        async def set_goodbye_handler(client, message: Message):
            await self.handle_set_goodbye(client, message)
        
        # Set warn limit
        @self.app.on_message(filters.command("setwarnlimit") & filters.group)
        @admin_only
        @log_command
        @handle_errors
        async def set_warn_limit_handler(client, message: Message):
            await self.handle_set_warn_limit(client, message)
    
    def _register_callbacks(self):
        """Register callback handlers - delegated to central CallbackHandlers"""
        # All callbacks are handled by handlers/callbacks.py
        pass
    
    async def handle_admin_callback(self, client: Client, callback: CallbackQuery):
        """Handle admin-related callbacks"""
        parts = callback.data.split('_')
        
        if len(parts) == 2:
            action, user_id = parts
            user_id = int(user_id)
            
            if action == "resetwarns":
                # Reset all warnings for user
                try:
                    await db.clear_warnings(user_id, callback.message.chat.id)
                    await callback.answer("✅ All warnings reset!", show_alert=True)
                    
                    keyboard = InlineKeyboardMarkup([
                        [InlineKeyboardButton("✅ Done", callback_data="close_message")]
                    ])
                    
                    try:
                        await callback.message.edit_reply_markup(reply_markup=keyboard)
                    except:
                        pass
                except Exception as e:
                    await callback.answer(f"❌ Error: {str(e)}", show_alert=True)
            
            elif action == "unban":
                # Unban user
                try:
                    await client.unban_chat_member(callback.message.chat.id, user_id)
                    await callback.answer("✅ User unbanned!", show_alert=True)
                    
                    keyboard = InlineKeyboardMarkup([
                        [InlineKeyboardButton("✅ Done", callback_data="close_message")]
                    ])
                    
                    try:
                        await callback.message.edit_reply_markup(reply_markup=keyboard)
                    except:
                        pass
                except Exception as e:
                    await callback.answer(f"❌ Error: {str(e)}", show_alert=True)
        else:
            await callback.answer("Coming soon!", show_alert=True)
    
    async def handle_ban(self, client: Client, message: Message):
        """Ban a user"""
        user, reason = await self.parse_target(message)
        
        if not user:
            await message.reply_text("❌ User not found or invalid format!")
            return
        
        try:
            await client.ban_chat_member(message.chat.id, user.id)
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔓 Unban", callback_data=f"unban_{user.id}")]
            ])
            
            await message.reply_text(
                f"🔨 {get_mention(user)} has been banned!\n"
                f"📝 Reason: {reason or 'No reason provided'}",
                reply_markup=keyboard,
                disable_notification=True
            )
        except Exception as e:
            logger.error(f"Error banning user: {e}")
            await message.reply_text(f"❌ Error: {e}")
    
    async def handle_unban(self, client: Client, message: Message):
        """Unban a user"""
        user, _ = await self.parse_target(message)
        
        if not user:
            await message.reply_text("❌ User not found!")
            return
        
        try:
            await client.unban_chat_member(message.chat.id, user.id)
            await message.reply_text(
                f"🔓 {get_mention(user)} has been unbanned!",
                disable_notification=True
            )
        except Exception as e:
            logger.error(f"Error unbanning user: {e}")
            await message.reply_text(f"❌ Error: {e}")
    
    async def handle_kick(self, client: Client, message: Message):
        """Kick a user (ban and unban)"""
        user, reason = await self.parse_target(message)
        
        if not user:
            await message.reply_text("❌ User not found!")
            return
        
        try:
            await client.ban_chat_member(message.chat.id, user.id)
            await client.unban_chat_member(message.chat.id, user.id)
            
            await message.reply_text(
                f"👢 {get_mention(user)} has been kicked!\n"
                f"📝 Reason: {reason or 'No reason provided'}",
                disable_notification=True
            )
        except Exception as e:
            logger.error(f"Error kicking user: {e}")
            await message.reply_text(f"❌ Error: {e}")
    
    async def handle_mute(self, client: Client, message: Message):
        """Mute a user"""
        user, reason = await self.parse_target(message)
        
        if not user:
            await message.reply_text("❌ User not found!")
            return
        
        try:
            await client.restrict_chat_member(
                message.chat.id,
                user.id,
                permissions=ChatPermissions(
                    can_send_messages=False,
                    can_send_media_messages=False,
                    can_send_other_messages=False,
                    can_add_web_page_previews=False
                )
            )
            
            await db.mute_user(user.id, message.chat.id, message.from_user.id, reason=reason)
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔊 Unmute", callback_data=f"unmute_{user.id}")]
            ])
            
            await message.reply_text(
                f"🔇 {get_mention(user)} has been muted!\n"
                f"📝 Reason: {reason or 'No reason provided'}",
                reply_markup=keyboard,
                disable_notification=True
            )
        except Exception as e:
            logger.error(f"Error muting user: {e}")
            await message.reply_text(f"❌ Error: {e}")
    
    async def handle_unmute(self, client: Client, message: Message):
        """Unmute a user"""
        user, _ = await self.parse_target(message)
        
        if not user:
            await message.reply_text("❌ User not found!")
            return
        
        try:
            await client.restrict_chat_member(
                message.chat.id,
                user.id,
                permissions=ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_other_messages=True,
                    can_add_web_page_previews=True
                )
            )
            
            await db.unmute_user(user.id, message.chat.id)
            
            await message.reply_text(
                f"🔊 {get_mention(user)} has been unmuted!",
                disable_notification=True
            )
        except Exception as e:
            logger.error(f"Error unmuting user: {e}")
            await message.reply_text(f"❌ Error: {e}")
    
    async def handle_tmute(self, client: Client, message: Message):
        """Temporarily mute a user"""
        args = message.text.split()[1:]
        
        if len(args) < 1:
            await message.reply_text("Usage: /tmute <user> <duration> (e.g., /tmute @user 5m)")
            return
        
        duration_str = args[-1]
        duration = parse_duration(duration_str)
        
        if duration <= 0:
            await message.reply_text("❌ Invalid duration format!")
            return
        
        # Get user from remaining args
        user_text = ' '.join(args[:-1])
        if not user_text:
            # Check for reply
            if message.reply_to_message:
                user = message.reply_to_message.from_user
            else:
                await message.reply_text("❌ User not found!")
                return
        else:
            user_id = parse_user_id(user_text)
            if not user_id:
                await message.reply_text("❌ Invalid user format!")
                return
            
            try:
                if isinstance(user_id, str):
                    # It's a username
                    user = await client.get_users(user_id)
                else:
                    user = await client.get_users(user_id)
            except:
                await message.reply_text("❌ User not found!")
                return
        
        try:
            await client.restrict_chat_member(
                message.chat.id,
                user.id,
                permissions=ChatPermissions(
                    can_send_messages=False,
                    can_send_media_messages=False,
                    can_send_other_messages=False,
                    can_add_web_page_previews=False
                ),
                until_date=datetime.now() + timedelta(seconds=duration)
            )
            
            await db.mute_user(
                user.id, message.chat.id, message.from_user.id,
                duration=duration
            )
            
            await message.reply_text(
                f"🔇 {get_mention(user)} has been muted for {format_duration(duration)}!",
                disable_notification=True
            )
        except Exception as e:
            logger.error(f"Error muting user: {e}")
            await message.reply_text(f"❌ Error: {e}")
    
    async def handle_warn(self, client: Client, message: Message):
        """Warn a user"""
        user, reason = await self.parse_target(message)
        
        if not user:
            await message.reply_text("❌ User not found!")
            return
        
        settings = await db.get_group_settings(message.chat.id)
        warn_limit = settings.warns_limit if settings else config.defaults.default_warns
        
        warn_count = await db.add_warning(
            user.id, message.chat.id, reason or "No reason", message.from_user.id
        )
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📋 View Warnings", callback_data=f"warns_{user.id}")]
        ])
        
        await message.reply_text(
            f"⚠️ {get_mention(user)} has been warned!\n"
            f"📊 Warnings: {warn_count}/{warn_limit}\n"
            f"📝 Reason: {reason or 'No reason provided'}",
            reply_markup=keyboard,
            disable_notification=True
        )
        
        # Check if user should be banned
        if warn_count >= warn_limit:
            try:
                await client.ban_chat_member(message.chat.id, user.id)
                await db.clear_warnings(user.id, message.chat.id)
                await message.reply_text(
                    f"🔨 {get_mention(user)} has reached maximum warnings and has been banned!",
                    disable_notification=True
                )
            except Exception as e:
                logger.error(f"Error banning user after max warnings: {e}")
    
    async def handle_dwarn(self, client: Client, message: Message):
        """Delete a warning"""
        args = message.text.split()[1:]
        
        if not args:
            await message.reply_text("Usage: /dwarn <user> [warning_id]")
            return
        
        user_text = ' '.join(args)
        user_id = parse_user_id(user_text)
        
        if not user_id:
            await message.reply_text("❌ Invalid user format!")
            return
        
        try:
            if isinstance(user_id, str):
                user = await client.get_users(user_id)
            else:
                user = await client.get_users(user_id)
        except:
            await message.reply_text("❌ User not found!")
            return
        
        warnings = await db.get_warnings(user.id if hasattr(user, 'id') else user_id, message.chat.id)
        
        if not warnings:
            await message.reply_text("✅ No warnings to delete!")
            return
        
        # Delete the most recent warning
        await db.remove_warning(warnings[0]['id'])
        
        await message.reply_text(
            f"✅ Warning removed for {get_mention(user)}!",
            disable_notification=True
        )
    
    async def handle_warns(self, client: Client, message: Message):
        """View user warnings"""
        args = message.text.split()[1:]
        
        # If no args, check for reply or self
        if not args:
            if message.reply_to_message:
                user = message.reply_to_message.from_user
            else:
                user = message.from_user
        else:
            user_text = ' '.join(args)
            user_id = parse_user_id(user_text)
            
            if not user_id:
                await message.reply_text("❌ Invalid user format!")
                return
            
            try:
                if isinstance(user_id, str):
                    user = await client.get_users(user_id)
                else:
                    user = await client.get_users(user_id)
            except:
                await message.reply_text("❌ User not found!")
                return
        
        warnings = await db.get_warnings(user.id, message.chat.id)
        
        settings = await db.get_group_settings(message.chat.id)
        warn_limit = settings.warns_limit if settings else config.defaults.default_warns
        
        text = f"""
╔═══════════════════════════════════════════╗
║           ⚠️ User Warnings ⚠️              ║
╚═══════════════════════════════════════════╝

👤 **User:** {get_mention(user)}
📊 **Total:** {len(warnings)}/{warn_limit} warnings
"""
        
        if not warnings:
            text += "\n✅ This user has no warnings!"
        else:
            text += "\n**Warning List:**\n"
            for i, warn in enumerate(warnings, 1):
                from utils.helpers import time_ago
                warn_time = time_ago(int(datetime.now().timestamp() - (datetime.now() - warn['warned_at']).total_seconds()))
                text += f"\n{i}. 📝 {warn['reason']}\n"
                text += f"   ⏰ {warn_time} ago\n"
        
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🗑️ Reset Warnings", callback_data=f"resetwarns_{user.id}"),
                InlineKeyboardButton("❌ Close", callback_data="close_message")
            ]
        ]) if warnings else InlineKeyboardMarkup([
            [InlineKeyboardButton("❌ Close", callback_data="close_message")]
        ])
        
        await message.reply_text(text, reply_markup=keyboard)
    
    async def handle_resetwarns(self, client: Client, message: Message):
        """Reset all warnings for a user"""
        args = message.text.split()[1:]
        
        if not args:
            await message.reply_text("Usage: /resetwarns <user>")
            return
        
        user_text = ' '.join(args)
        user_id = parse_user_id(user_text)
        
        if not user_id:
            await message.reply_text("❌ Invalid user format!")
            return
        
        try:
            if isinstance(user_id, str):
                user = await client.get_users(user_id)
            else:
                user = await client.get_users(user_id)
        except:
            await message.reply_text("❌ User not found!")
            return
        
        await db.clear_warnings(user.id if hasattr(user, 'id') else user_id, message.chat.id)
        
        await message.reply_text(
            f"✅ All warnings reset for {get_mention(user)}!",
            disable_notification=True
        )
    
    async def handle_pin(self, client: Client, message: Message):
        """Pin a message"""
        if not message.reply_to_message:
            await message.reply_text("❌ Reply to a message to pin it!")
            return
        
        disable_notification = "loud" not in message.text.lower()
        
        try:
            await client.pin_chat_message(
                message.chat.id,
                message.reply_to_message.id,
                disable_notification=disable_notification
            )
            await message.reply_text(
                "📌 Message pinned!",
                disable_notification=True
            )
        except Exception as e:
            logger.error(f"Error pinning message: {e}")
            await message.reply_text(f"❌ Error: {e}")
    
    async def handle_unpin(self, client: Client, message: Message):
        """Unpin a message"""
        if message.reply_to_message:
            try:
                await client.unpin_chat_message(
                    message.chat.id,
                    message.reply_to_message.id
                )
                await message.reply_text(
                    "📌 Message unpinned!",
                    disable_notification=True
                )
            except Exception as e:
                logger.error(f"Error unpinning message: {e}")
                await message.reply_text(f"❌ Error: {e}")
        else:
            try:
                await client.unpin_all_chat_messages(message.chat.id)
                await message.reply_text(
                    "📌 All messages unpinned!",
                    disable_notification=True
                )
            except Exception as e:
                logger.error(f"Error unpinning all messages: {e}")
                await message.reply_text(f"❌ Error: {e}")
    
    async def handle_purge(self, client: Client, message: Message):
        """Purge messages"""
        if not message.reply_to_message:
            await message.reply_text("❌ Reply to a message to start purging!")
            return
        
        if message.reply_to_message.from_user.id != (await client.get_me()).id:
            await message.reply_text("❌ Reply to a bot message!")
            return
        
        deleted_count = 0
        current_msg_id = message.reply_to_message.id
        
        try:
            while True:
                await client.delete_messages(message.chat.id, current_msg_id)
                deleted_count += 1
                
                # Get next message
                messages = await client.get_messages(message.chat.id, current_msg_id + 1)
                if not messages:
                    break
                
                current_msg_id = messages.id
                
                # Safety limit
                if deleted_count >= 100:
                    break
        except Exception as e:
            logger.error(f"Error purging messages: {e}")
        
        await message.reply_text(
            f"🗑️ Purged {deleted_count} messages!",
            disable_notification=True
        )
    
    async def handle_set_welcome(self, client: Client, message: Message):
        """Set welcome message"""
        args = message.text.split(maxsplit=1)
        
        if len(args) < 2:
            await message.reply_text("Usage: /setwelcome <message>\nUse {user} for username")
            return
        
        welcome_text = args[1]
        
        settings = await db.get_group_settings(message.chat.id)
        if not settings:
            from database.database import GroupSettings
            chat = await client.get_chat(message.chat.id)
            settings = GroupSettings(chat_id=message.chat.id, chat_title=chat.title)
        
        settings.welcome_message = welcome_text
        await db.save_group_settings(settings)
        
        await message.reply_text(
            "✅ Welcome message set!",
            disable_notification=True
        )
    
    async def handle_set_goodbye(self, client: Client, message: Message):
        """Set goodbye message"""
        args = message.text.split(maxsplit=1)
        
        if len(args) < 2:
            await message.reply_text("Usage: /setgoodbye <message>\nUse {user} for username")
            return
        
        goodbye_text = args[1]
        
        settings = await db.get_group_settings(message.chat.id)
        if not settings:
            from database.database import GroupSettings
            chat = await client.get_chat(message.chat.id)
            settings = GroupSettings(chat_id=message.chat.id, chat_title=chat.title)
        
        settings.goodbye_message = goodbye_text
        await db.save_group_settings(settings)
        
        await message.reply_text(
            "✅ Goodbye message set!",
            disable_notification=True
        )
    
    async def handle_set_warn_limit(self, client: Client, message: Message):
        """Set warning limit"""
        args = message.text.split()[1:]
        
        if not args:
            await message.reply_text("Usage: /setwarnlimit <number>")
            return
        
        try:
            limit = int(args[0])
            if limit < 1 or limit > 10:
                await message.reply_text("Limit must be between 1 and 10")
                return
            
            settings = await db.get_group_settings(message.chat.id)
            if not settings:
                from database.database import GroupSettings
                chat = await client.get_chat(message.chat.id)
                settings = GroupSettings(chat_id=message.chat.id, chat_title=chat.title)
            
            settings.warns_limit = limit
            await db.save_group_settings(settings)
            
            await message.reply_text(
                f"✅ Warning limit set to {limit}!",
                disable_notification=True
            )
        except ValueError:
            await message.reply_text("❌ Invalid number!")
    
    async def parse_target(self, message: Message):
        """Parse target user and reason from message"""
        args = message.text.split()[1:]
        
        if not args:
            if message.reply_to_message:
                user = message.reply_to_message.from_user
                reason = self._extract_reason(message.text)
            else:
                return None, None
        else:
            # Check if last arg looks like a reason (not @user or number or id format)
            user_args = args.copy()
            reason = None
            
            # Look for reason after user mention/ID
            for i, arg in enumerate(args):
                if i == 0:
                    continue
                # If arg doesn't start with @ or id, it's likely part of reason
                if not arg.startswith(('@', 'id')) and not arg.lstrip('-').isdigit():
                    reason = ' '.join(args[i:])
                    user_args = args[:i]
                    break
            
            user_text = user_args[0] if user_args else None
            if not user_text:
                return None, None
            
            # Try to parse user from mention, username, or ID
            user = await self._resolve_user(user_text)
            if not user:
                return None, None
        
        return user, reason
    
    async def _resolve_user(self, user_text: str):
        """Resolve user from various formats: @username, user ID, or id123"""
        try:
            # Direct numeric ID
            if user_text.lstrip('-').isdigit():
                users = await self.app.get_users(int(user_text))
                return users[0] if isinstance(users, list) else users
            
            # Username or mention (starts with @)
            if user_text.startswith('@'):
                users = await self.app.get_users(user_text)
                return users[0] if isinstance(users, list) else users
            
            # ID mention format (id123456)
            id_match = re.match(r'id(\d+)', user_text, re.IGNORECASE)
            if id_match:
                user_id = int(id_match.group(1))
                users = await self.app.get_users(user_id)
                return users[0] if isinstance(users, list) else users
            
            # Try as username directly
            users = await self.app.get_users(user_text)
            return users[0] if isinstance(users, list) else users
            
        except Exception as e:
            logger.debug(f"Could not resolve user '{user_text}': {e}")
            return None
    
    def _extract_reason(self, text: str) -> Optional[str]:
        """Extract reason from command text (after the command)"""
        # Split by space and get everything after the command
        parts = text.split(maxsplit=1)
        if len(parts) > 1:
            return parts[1] if parts[1].strip() else None
        return None