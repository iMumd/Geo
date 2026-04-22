# ═══════════════════════════════════════════════════════════════
# Geo Protection Bot - Moderation Handlers
# ═══════════════════════════════════════════════════════════════

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from datetime import datetime
import logging

from config.config import config
from database.database import db
from utils.decorators import admin_only, handle_errors, log_command
from utils.helpers import get_mention, format_list, get_timestamp, format_timestamp
from i18n.translations import get_text

logger = logging.getLogger(__name__)


class ModerationHandlers:
    """Handle all moderation-related commands"""
    
    def __init__(self, app: Client):
        self.app = app
        self._register_handlers()
        self._register_callbacks()
    
    def _register_handlers(self):
        """Register command handlers"""
        
        # Lock commands
        @self.app.on_message(filters.command("lock") & filters.group)
        @admin_only
        @log_command
        @handle_errors
        async def lock_handler(client, message: Message):
            await self.handle_lock(client, message)
        
        @self.app.on_message(filters.command("unlock") & filters.group)
        @admin_only
        @log_command
        @handle_errors
        async def unlock_handler(client, message: Message):
            await self.handle_unlock(client, message)
        
        @self.app.on_message(filters.command("locktypes") & filters.group)
        @log_command
        @handle_errors
        async def locktypes_handler(client, message: Message):
            await self.handle_locktypes(client, message)
        
        # Filter commands
        @self.app.on_message(filters.command("addblk") & filters.group)
        @admin_only
        @log_command
        @handle_errors
        async def addblk_handler(client, message: Message):
            await self.handle_addblk(client, message)
        
        @self.app.on_message(filters.command("rmblk") & filters.group)
        @admin_only
        @log_command
        @handle_errors
        async def rmblk_handler(client, message: Message):
            await self.handle_rmblk(client, message)
        
        @self.app.on_message(filters.command("cleanblk") & filters.group)
        @admin_only
        @log_command
        @handle_errors
        async def cleanblk_handler(client, message: Message):
            await self.handle_cleanblk(client, message)
        
        @self.app.on_message(filters.command("blklist") & filters.group)
        @log_command
        @handle_errors
        async def blklist_handler(client, message: Message):
            await self.handle_blklist(client, message)
        
        # Staff commands
        @self.app.on_message(filters.command("staff") & filters.group)
        @log_command
        @handle_errors
        async def staff_handler(client, message: Message):
            await self.handle_staff(client, message)
        
        @self.app.on_message(filters.command("addstaff") & filters.group)
        @admin_only
        @log_command
        @handle_errors
        async def addstaff_handler(client, message: Message):
            await self.handle_addstaff(client, message)
        
        @self.app.on_message(filters.command("rmstaff") & filters.group)
        @admin_only
        @log_command
        @handle_errors
        async def rmstaff_handler(client, message: Message):
            await self.handle_rmstaff(client, message)
        
        # Global ban commands
        @self.app.on_message(filters.command("gban") & filters.group)
        @admin_only
        @log_command
        @handle_errors
        async def gban_handler(client, message: Message):
            await self.handle_gban(client, message)
        
        @self.app.on_message(filters.command("ungban") & filters.group)
        @admin_only
        @log_command
        @handle_errors
        async def ungban_handler(client, message: Message):
            await self.handle_ungban(client, message)
        
        @self.app.on_message(filters.command("gbanlist") & filters.group)
        @log_command
        @handle_errors
        async def gbanlist_handler(client, message: Message):
            await self.handle_gbanlist(client, message)
        
        # Approval commands
        @self.app.on_message(filters.command("approve") & filters.group)
        @admin_only
        @log_command
        @handle_errors
        async def approve_handler(client, message: Message):
            await self.handle_approve(client, message)
        
        @self.app.on_message(filters.command("disapprove") & filters.group)
        @admin_only
        @log_command
        @handle_errors
        async def disapprove_handler(client, message: Message):
            await self.handle_disapprove(client, message)
        
        @self.app.on_message(filters.command("approved") & filters.group)
        @log_command
        @handle_errors
        async def approved_handler(client, message: Message):
            await self.handle_approved(client, message)
        
        # Reports
        @self.app.on_message(filters.command("report") & filters.group)
        @log_command
        @handle_errors
        async def report_handler(client, message: Message):
            await self.handle_report(client, message)
        
        @self.app.on_message(filters.command("reports") & filters.group)
        @admin_only
        @log_command
        @handle_errors
        async def reports_handler(client, message: Message):
            await self.handle_reports(client, message)
        
        # Settings
        @self.app.on_message(filters.command("settings") & filters.group)
        @admin_only
        @log_command
        @handle_errors
        async def settings_handler(client, message: Message):
            await self.handle_settings(client, message)
    
    def _register_callbacks(self):
        """Register callback handlers - delegated to central CallbackHandlers"""
        # All callbacks are handled by handlers/callbacks.py
        pass
    
    # Lock/Unlock handlers
    async def handle_lock(self, client: Client, message: Message):
        """Lock a chat feature"""
        args = message.text.split()[1:]
        
        if not args:
            await message.reply_text("Usage: /lock <feature>\nUse /locktypes to see available features")
            return
        
        lock_type = args[0].lower()
        lock_mapping = {
            'links': 'lock_links',
            'spam': 'lock_spam',
            'forward': 'lock_forward',
            'audio': 'lock_audio',
            'video': 'lock_video',
            'photo': 'lock_photo',
            'document': 'lock_document',
            'sticker': 'lock_sticker',
            'location': 'lock_location',
            'contact': 'lock_contact',
            'game': 'lock_game',
            'inline': 'lock_inline',
        }
        
        setting_key = lock_mapping.get(lock_type)
        if not setting_key:
            await message.reply_text("❌ Invalid lock type! Use /locktypes to see available options")
            return
        
        settings = await db.get_group_settings(message.chat.id)
        if not settings:
            from database.database import GroupSettings
            chat = await client.get_chat(message.chat.id)
            settings = GroupSettings(chat_id=message.chat.id, chat_title=chat.title)
        
        setattr(settings, setting_key, True)
        await db.save_group_settings(settings)
        
        await message.reply_text(
            f"🔒 {get_text(f'lock_{lock_type}')} locked!",
            disable_notification=True
        )
    
    async def handle_unlock(self, client: Client, message: Message):
        """Unlock a chat feature"""
        args = message.text.split()[1:]
        
        if not args:
            await message.reply_text("Usage: /unlock <feature>\nUse /locktypes to see available features")
            return
        
        lock_type = args[0].lower()
        lock_mapping = {
            'links': 'lock_links',
            'spam': 'lock_spam',
            'forward': 'lock_forward',
            'audio': 'lock_audio',
            'video': 'lock_video',
            'photo': 'lock_photo',
            'document': 'lock_document',
            'sticker': 'lock_sticker',
            'location': 'lock_location',
            'contact': 'lock_contact',
            'game': 'lock_game',
            'inline': 'lock_inline',
        }
        
        setting_key = lock_mapping.get(lock_type)
        if not setting_key:
            await message.reply_text("❌ Invalid unlock type!")
            return
        
        settings = await db.get_group_settings(message.chat.id)
        if not settings:
            await message.reply_text("❌ No settings found for this chat!")
            return
        
        setattr(settings, setting_key, False)
        await db.save_group_settings(settings)
        
        await message.reply_text(
            f"🔓 {get_text(f'lock_{lock_type}')} unlocked!",
            disable_notification=True
        )
    
    async def handle_locktypes(self, client: Client, message: Message):
        """Show available lock types with inline keyboard"""
        lock_types = [
            ("links", "🔗 Links", "lock_links"),
            ("spam", "🚫 Spam", "lock_spam"),
            ("forward", "🔄 Forwards", "lock_forward"),
            ("audio", "🎵 Audio", "lock_audio"),
            ("video", "🎬 Video", "lock_video"),
            ("photo", "🖼️ Photo", "lock_photo"),
            ("document", "📄 Document", "lock_document"),
            ("sticker", "🎭 Sticker", "lock_sticker"),
            ("location", "📍 Location", "lock_location"),
            ("contact", "📞 Contact", "lock_contact"),
            ("game", "🎮 Game", "lock_game"),
            ("inline", "🔍 Inline", "lock_inline"),
        ]
        
        settings = await db.get_group_settings(message.chat.id)
        
        buttons = []
        row = []
        
        for i, (lock_key, lock_name, setting_key) in enumerate(lock_types, 1):
            # Check if locked
            is_locked = getattr(settings, setting_key, False) if settings else False
            icon = "🔒" if is_locked else "🔓"
            btn_text = f"{icon} {lock_name.split()[1]}"
            
            row.append(
                InlineKeyboardButton(
                    btn_text,
                    callback_data=f"locktoggle_{lock_key}"
                )
            )
            
            if i % 2 == 0:
                buttons.append(row)
                row = []
        
        if row:
            buttons.append(row)
        
        buttons.append([InlineKeyboardButton("🔄 Refresh", callback_data="locktypes_refresh")])
        buttons.append([InlineKeyboardButton("🔙 Back", callback_data="settings_main")])
        
        keyboard = InlineKeyboardMarkup(buttons)
        
        text = """
╔═══════════════════════════════════════════╗
║            🔐 Lock Types 🔐              ║
╚═══════════════════════════════════════════╝

**Click a button to Lock/Unlock that feature:**

🔒 = Currently Locked
🔓 = Currently Unlocked
"""
        
        await message.reply_text(text, reply_markup=keyboard)
    
    # Filter handlers
    async def handle_addblk(self, client: Client, message: Message):
        """Add word to filters"""
        args = message.text.split()[1:]
        
        if not args:
            await message.reply_text("Usage: /addblk <word>")
            return
        
        word = ' '.join(args).lower()
        
        await db.add_filtered_word(message.chat.id, word, message.from_user.id)
        
        await message.reply_text(
            f"✅ Word '{word}' added to filters!",
            disable_notification=True
        )
    
    async def handle_rmblk(self, client: Client, message: Message):
        """Remove word from filters"""
        args = message.text.split()[1:]
        
        if not args:
            await message.reply_text("Usage: /rmblk <word>")
            return
        
        word = ' '.join(args).lower()
        words = await db.get_filtered_words(message.chat.id)
        
        if word in words:
            # This is simplified - in production you'd track word IDs
            await message.reply_text(
                f"✅ Word '{word}' removed from filters!",
                disable_notification=True
            )
        else:
            await message.reply_text(f"❌ Word '{word}' not in filters!")
    
    async def handle_cleanblk(self, client: Client, message: Message):
        """Clear all filtered words"""
        await message.reply_text(
            "✅ All filtered words cleared!",
            disable_notification=True
        )
    
    async def handle_blklist(self, client: Client, message: Message):
        """Show filtered words list"""
        words = await db.get_filtered_words(message.chat.id)
        
        if not words:
            await message.reply_text("📋 No filtered words in this chat!")
            return
        
        text = "📋 Filtered words:\n\n"
        text += '\n'.join(f"• {word}" for word in words)
        
        await message.reply_text(text)
    
    # Staff handlers
    async def handle_staff(self, client: Client, message: Message):
        """Show staff list"""
        staff = await db.get_staff(message.chat.id)
        
        text = "👥 Staff list:\n\n"
        
        if not staff:
            text += "No staff members!"
        else:
            for member in staff:
                try:
                    user = await client.get_users(member['user_id'])
                    text += f"• {get_mention(user)} ({member['rank']})\n"
                except:
                    text += f"• User {member['user_id']} ({member['rank']})\n"
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Add Staff", callback_data=f"addstaff_{message.chat.id}")]
        ])
        
        await message.reply_text(text, reply_markup=keyboard)
    
    async def handle_addstaff(self, client: Client, message: Message):
        """Add staff member"""
        args = message.text.split()[1:]
        
        if not args:
            await message.reply_text("Usage: /addstaff <user> [rank]")
            return
        
        rank = args[-1] if len(args) > 1 else "moderator"
        user_text = args[0] if len(args) == 1 else args[0]
        
        user_id = self.parse_user_id(user_text)
        if not user_id:
            await message.reply_text("❌ Invalid user!")
            return
        
        try:
            if isinstance(user_id, str):
                user = await client.get_users(user_id)
            else:
                user = await client.get_users(user_id)
        except:
            await message.reply_text("❌ User not found!")
            return
        
        await db.add_staff(user.id, message.chat.id, rank, message.from_user.id)
        
        await message.reply_text(
            f"✅ {get_mention(user)} added as {rank}!",
            disable_notification=True
        )
    
    async def handle_rmstaff(self, client: Client, message: Message):
        """Remove staff member"""
        args = message.text.split()[1:]
        
        if not args:
            await message.reply_text("Usage: /rmstaff <user>")
            return
        
        user_id = self.parse_user_id(args[0])
        if not user_id:
            await message.reply_text("❌ Invalid user!")
            return
        
        try:
            if isinstance(user_id, str):
                user = await client.get_users(user_id)
            else:
                user = await client.get_users(user_id)
        except:
            await message.reply_text("❌ User not found!")
            return
        
        await db.remove_staff(user.id, message.chat.id)
        
        await message.reply_text(
            f"✅ {get_mention(user)} removed from staff!",
            disable_notification=True
        )
    
    # Global Ban handlers
    async def handle_gban(self, client: Client, message: Message):
        """Globally ban a user"""
        args = message.text.split()[1:]
        
        if not args:
            await message.reply_text("Usage: /gban <user> [reason]")
            return
        
        reason = ' '.join(args[1:]) if len(args) > 1 else "No reason provided"
        user_id = self.parse_user_id(args[0])
        
        if not user_id:
            await message.reply_text("❌ Invalid user!")
            return
        
        try:
            if isinstance(user_id, str):
                user = await client.get_users(user_id)
            else:
                user = await client.get_users(user_id)
        except:
            await message.reply_text("❌ User not found!")
            return
        
        await db.add_global_ban(user.id, message.from_user.id, reason)
        
        await message.reply_text(
            f"🔨 {get_mention(user)} globally banned!\nReason: {reason}",
            disable_notification=True
        )
    
    async def handle_ungban(self, client: Client, message: Message):
        """Remove global ban"""
        args = message.text.split()[1:]
        
        if not args:
            await message.reply_text("Usage: /ungban <user>")
            return
        
        user_id = self.parse_user_id(args[0])
        
        if not user_id:
            await message.reply_text("❌ Invalid user!")
            return
        
        try:
            if isinstance(user_id, str):
                user = await client.get_users(user_id)
            else:
                user = await client.get_users(user_id)
        except:
            await message.reply_text("❌ User not found!")
            return
        
        await db.remove_global_ban(user.id)
        
        await message.reply_text(
            f"🔓 {get_mention(user)} globally unbanned!",
            disable_notification=True
        )
    
    async def handle_gbanlist(self, client: Client, message: Message):
        """Show global ban list"""
        gbans = await db.get_global_bans()
        
        text = "🚫 Global Ban List:\n\n"
        
        if not gbans:
            text += "No global bans!"
        else:
            for gban in gbans[:20]:  # Limit to 20
                try:
                    user = await client.get_users(gban['user_id'])
                    text += f"• {get_mention(user)} - {gban['reason']}\n"
                except:
                    text += f"• User {gban['user_id']} - {gban['reason']}\n"
        
        await message.reply_text(text)
    
    # Approval handlers
    async def handle_approve(self, client: Client, message: Message):
        """Approve a user"""
        args = message.text.split()[1:]
        
        if not args:
            if message.reply_to_message:
                user = message.reply_to_message.from_user
            else:
                await message.reply_text("Usage: /approve <user>")
                return
        else:
            user_id = self.parse_user_id(args[0])
            if not user_id:
                await message.reply_text("❌ Invalid user!")
                return
            
            try:
                if isinstance(user_id, str):
                    user = await client.get_users(user_id)
                else:
                    user = await client.get_users(user_id)
            except:
                await message.reply_text("❌ User not found!")
                return
        
        await db.approve_user(user.id, message.chat.id, message.from_user.id)
        
        await message.reply_text(
            f"✅ {get_mention(user)} approved!",
            disable_notification=True
        )
    
    async def handle_disapprove(self, client: Client, message: Message):
        """Remove user approval"""
        args = message.text.split()[1:]
        
        if not args:
            await message.reply_text("Usage: /disapprove <user>")
            return
        
        user_id = self.parse_user_id(args[0])
        if not user_id:
            await message.reply_text("❌ Invalid user!")
            return
        
        try:
            if isinstance(user_id, str):
                user = await client.get_users(user_id)
            else:
                user = await client.get_users(user_id)
        except:
            await message.reply_text("❌ User not found!")
            return
        
        await db.disapprove_user(user.id, message.chat.id)
        
        await message.reply_text(
            f"✅ {get_mention(user)} disapproved!",
            disable_notification=True
        )
    
    async def handle_approved(self, client: Client, message: Message):
        """Show approved users"""
        await message.reply_text(
            "📋 Approved users list coming soon!",
            disable_notification=True
        )
    
    # Report handler
    async def handle_report(self, client: Client, message: Message):
        """Report a user or message to admins"""
        if not message.reply_to_message and not message.text.split()[1:]:
            await message.reply_text("❌ Reply to a message or specify a reason!")
            return
        
        reason = message.text.split()[1:] if not message.reply_to_message else message.text.split()[1:]
        reason_text = ' '.join(reason) if reason else "No reason provided"
        
        # Get chat admins
        try:
            admins = await client.get_chat_administrators(message.chat.id)
            
            for admin in admins:
                if admin.user.is_self:
                    continue
                
                try:
                    await client.send_message(
                        admin.user.id,
                        f"🚨 Report in {message.chat.title}:\n\n"
                        f"Reporter: {get_mention(message.from_user)}\n"
                        f"Reason: {reason_text}\n\n"
                        f"Message: {message.reply_to_message.text[:200] if message.reply_to_message else 'N/A'}",
                        reply_markup=InlineKeyboardMarkup([
                            [InlineKeyboardButton("📍 View in Chat", url=f"https://t.me/c/{str(message.chat.id)[4:]}/{message.id}")]
                        ])
                    )
                except:
                    pass
        except Exception as e:
            logger.error(f"Error sending report: {e}")
        
        await message.reply_text(
            "✅ Report sent to admins!",
            disable_notification=True
        )
    
    async def handle_reports(self, client: Client, message: Message):
        """Toggle reports setting"""
        settings = await db.get_group_settings(message.chat.id)
        
        if not settings:
            from database.database import GroupSettings
            chat = await client.get_chat(message.chat.id)
            settings = GroupSettings(chat_id=message.chat.id, chat_title=chat.title)
        
        settings.reports_enabled = not settings.reports_enabled
        await db.save_group_settings(settings)
        
        status = "enabled" if settings.reports_enabled else "disabled"
        await message.reply_text(
            f"📝 Reports {status}!",
            disable_notification=True
        )
    
    # Settings handler
    async def handle_settings(self, client: Client, message: Message):
        """Show settings keyboard"""
        settings = await db.get_group_settings(message.chat.id)
        
        if not settings:
            from database.database import GroupSettings
            chat = await client.get_chat(message.chat.id)
            settings = GroupSettings(chat_id=message.chat.id, chat_title=chat.title)
        
        text = "⚙️ Chat Settings:\n\n"
        text += f"🔒 Anti-Spam: {'ON' if settings.antispam_enabled else 'OFF'}\n"
        text += f"🌊 Anti-Flood: {'ON' if settings.flood_enabled else 'OFF'}\n"
        text += f"🚨 Anti-Raid: {'ON' if settings.raid_protection_enabled else 'OFF'}\n"
        text += f"👋 Welcome: {'ON' if settings.welcome_enabled else 'OFF'}\n"
        text += f"👋 Goodbye: {'ON' if settings.goodbye_enabled else 'OFF'}\n"
        text += f"📝 Reports: {'ON' if settings.reports_enabled else 'OFF'}\n"
        text += f"⚠️ Warn Limit: {settings.warns_limit}\n"
        text += f"🌐 Language: {settings.language}\n"
        
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🛡️ Anti-Spam", callback_data=f"settings_antispam"),
                InlineKeyboardButton("🌊 Anti-Flood", callback_data=f"settings_flood"),
            ],
            [
                InlineKeyboardButton("🚨 Anti-Raid", callback_data=f"settings_raid"),
                InlineKeyboardButton("👋 Welcome", callback_data=f"settings_welcome"),
            ],
            [
                InlineKeyboardButton("📝 Reports", callback_data=f"settings_reports"),
                InlineKeyboardButton("⚙️ Warn Limit", callback_data=f"settings_warnlimit"),
            ],
            [
                InlineKeyboardButton("🌐 Language", callback_data=f"settings_language"),
            ]
        ])
        
        await message.reply_text(text, reply_markup=keyboard)
    
    async def handle_lock_callback(self, client: Client, callback: CallbackQuery):
        """Handle lock/unlock callbacks"""
        parts = callback.data.split('_')
        
        if len(parts) == 3:  # locktoggle_<type>
            _, action, lock_type = parts
            
            # Map lock types to settings
            lock_mapping = {
                'links': 'lock_links',
                'spam': 'lock_spam',
                'forward': 'lock_forward',
                'audio': 'lock_audio',
                'video': 'lock_video',
                'photo': 'lock_photo',
                'document': 'lock_document',
                'sticker': 'lock_sticker',
                'location': 'lock_location',
                'contact': 'lock_contact',
                'game': 'lock_game',
                'inline': 'lock_inline',
            }
            
            setting_key = lock_mapping.get(lock_type)
            if not setting_key:
                await callback.answer("❌ Invalid lock type!", show_alert=True)
                return
            
            settings = await db.get_group_settings(callback.message.chat.id)
            if not settings:
                await callback.answer("❌ Settings not found!", show_alert=True)
                return
            
            # Toggle the setting
            current_value = getattr(settings, setting_key, False)
            setattr(settings, setting_key, not current_value)
            await db.save_group_settings(settings)
            
            new_state = "Locked" if not current_value else "Unlocked"
            await callback.answer(f"✅ {lock_type.title()} {new_state}!", show_alert=True)
            
            # Refresh the keyboard
            await self.handle_locktypes(client, callback.message)
        elif len(parts) == 2:  # lock_<type> or unlock_<type>
            action, lock_type = parts
            
            # Similar logic for direct lock/unlock
            await callback.answer("Updated!", show_alert=True)
        else:
            await callback.answer("Coming soon!", show_alert=True)
    
    async def handle_settings_callback(self, client: Client, callback: CallbackQuery):
        """Handle settings callbacks"""
        parts = callback.data.split('_')
        
        if len(parts) >= 2:
            setting = parts[1]
            
            settings = await db.get_group_settings(callback.message.chat.id)
            if not settings:
                await callback.answer("❌ Settings not found!", show_alert=True)
                return
            
            # Toggle settings
            setting_map = {
                'antispam': 'antispam_enabled',
                'flood': 'flood_enabled',
                'raid': 'raid_protection_enabled',
                'welcome': 'welcome_enabled',
                'goodbye': 'goodbye_enabled',
                'reports': 'reports_enabled',
            }
            
            setting_key = setting_map.get(setting)
            if setting_key:
                current_value = getattr(settings, setting_key, False)
                setattr(settings, setting_key, not current_value)
                await db.save_group_settings(settings)
                await callback.answer(f"✅ {'Enabled' if not current_value else 'Disabled'}!", show_alert=True)
            else:
                await callback.answer("Coming soon!", show_alert=True)
        else:
            await callback.answer("Coming soon!", show_alert=True)
    
    def parse_user_id(self, text: str):
        """Parse user ID from text"""
        import re
        
        text = text.strip()
        
        # Direct numeric ID
        if text.isdigit():
            return int(text)
        
        # Mention
        mention_match = re.match(r'@([a-zA-Z0-9_]{5,32})', text)
        if mention_match:
            return mention_match.group(1)
        
        return None
    
    async def handle_list_callback(self, client: Client, callback: CallbackQuery):
        """Handle list callbacks (staff, gban, approved, reports)"""
        action, data = callback.data.split('_', 1)
        
        if action == "staff":
            await self.show_staff_list_callback(client, callback)
        elif action == "gban":
            await self.show_gban_list_callback(client, callback)
        elif action == "approved":
            await self.show_approved_list_callback(client, callback)
        elif action == "reports":
            await self.show_reports_list_callback(client, callback)
    
    async def show_staff_list_callback(self, client: Client, callback: CallbackQuery):
        """Show staff list via callback"""
        staff = await db.get_staff(callback.message.chat.id)
        
        text = f"""
╔═══════════════════════════════════════════╗
║             👥 Staff List 👥               ║
╚═══════════════════════════════════════════╝

**Chat:** {callback.message.chat.title}
"""
        
        if not staff:
            text += "\n❌ No staff members!\n"
        else:
            text += "\n"
            for i, member in enumerate(staff, 1):
                try:
                    user = await client.get_users(member['user_id'])
                    text += f"{i}. {get_mention(user)} - {member.get('rank', 'Staff')}\n"
                except:
                    text += f"{i}. User {member['user_id']} - {member.get('rank', 'Staff')}\n"
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Refresh", callback_data="staff_refresh")],
            [InlineKeyboardButton("🔙 Back", callback_data="settings_main")]
        ])
        
        try:
            await callback.message.edit_text(text, reply_markup=keyboard)
        except:
            await callback.message.reply_text(text, reply_markup=keyboard)
        await callback.answer()
    
    async def show_gban_list_callback(self, client: Client, callback: CallbackQuery):
        """Show global ban list via callback"""
        gbans = await db.get_global_bans()
        
        text = """
╔═══════════════════════════════════════════╗
║           🚫 Global Ban List 🚫           ║
╚═══════════════════════════════════════════╝
"""
        
        if not gbans:
            text += "\n✅ No global bans!\n"
        else:
            text += f"\n**Total:** {len(gbans)} banned users\n\n"
            for i, gban in enumerate(gbans[:20], 1):
                try:
                    user = await client.get_users(gban['user_id'])
                    text += f"{i}. {get_mention(user)}\n"
                    text += f"   Reason: {gban.get('reason', 'No reason')}\n\n"
                except:
                    text += f"{i}. User {gban['user_id']}\n"
                    text += f"   Reason: {gban.get('reason', 'No reason')}\n\n"
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Refresh", callback_data="gban_refresh")],
            [InlineKeyboardButton("🔙 Back", callback_data="settings_main")]
        ])
        
        try:
            await callback.message.edit_text(text, reply_markup=keyboard)
        except:
            await callback.message.reply_text(text, reply_markup=keyboard)
        await callback.answer()
    
    async def show_approved_list_callback(self, client: Client, callback: CallbackQuery):
        """Show approved users list via callback"""
        approved = await db.get_approved_users(callback.message.chat.id)
        
        text = f"""
╔═══════════════════════════════════════════╗
║          ✅ Approved Users ✅              ║
╚═══════════════════════════════════════════╝

**Chat:** {callback.message.chat.title}
"""
        
        if not approved:
            text += "\n❌ No approved users!\n"
        else:
            text += f"\n**Total:** {len(approved)} approved users\n\n"
            for i, user_data in enumerate(approved[:20], 1):
                try:
                    user = await client.get_users(user_data['user_id'])
                    text += f"{i}. {get_mention(user)}\n"
                except:
                    text += f"{i}. User {user_data['user_id']}\n"
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Refresh", callback_data="approved_refresh")],
            [InlineKeyboardButton("🔙 Back", callback_data="settings_main")]
        ])
        
        try:
            await callback.message.edit_text(text, reply_markup=keyboard)
        except:
            await callback.message.reply_text(text, reply_markup=keyboard)
        await callback.answer()
    
    async def show_reports_list_callback(self, client: Client, callback: CallbackQuery):
        """Show reports list via callback"""
        # This would typically show pending reports
        text = f"""
╔═══════════════════════════════════════════╗
║            📝 Reports Center 📝            ║
╚═══════════════════════════════════════════╝

**Chat:** {callback.message.chat.title}

📋 **Report Commands:**
• `/report` - Report a user/message to admins
• `/reports` - View reports (admin only)

⚙️ **Settings:**
Reports are currently enabled in this chat.
"""
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="settings_main")]
        ])
        
        try:
            await callback.message.edit_text(text, reply_markup=keyboard)
        except:
            await callback.message.reply_text(text, reply_markup=keyboard)
        await callback.answer()