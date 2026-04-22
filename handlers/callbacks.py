# ═══════════════════════════════════════════════════════════════
# Geo Protection Bot - Central Callback Handlers
# ═══════════════════════════════════════════════════════════════

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.enums import ChatType
from datetime import datetime
import logging

from config.config import config
from database.database import db
from utils.decorators import handle_errors
from utils.helpers import get_mention, format_duration

logger = logging.getLogger(__name__)


class CallbackHandlers:
    """Central callback handlers for all inline keyboard buttons"""
    
    def __init__(self, app: Client):
        self.app = app
        self._register_callbacks()
        logger.info("✓ Callback handlers loaded")
    
    def _register_callbacks(self):
        """Register all callback query handlers"""
        
        # ==================== NAVIGATION ====================
        
        @self.app.on_callback_query(filters.regex(r"^start$"))
        @handle_errors
        async def cb_start(client, callback: CallbackQuery):
            """Main menu"""
            await self.show_main_menu(callback)
        
        @self.app.on_callback_query(filters.regex(r"^start_main$"))
        @handle_errors
        async def cb_start_main(client, callback: CallbackQuery):
            """Main menu"""
            await self.show_main_menu(callback)
        
        @self.app.on_callback_query(filters.regex(r"^help_main$"))
        @handle_errors
        async def cb_help_main(client, callback: CallbackQuery):
            """Help/Commands menu"""
            await self.show_help_menu(callback)
        
        @self.app.on_callback_query(filters.regex(r"^back_main$"))
        @handle_errors
        async def cb_back_main(client, callback: CallbackQuery):
            """Back to main menu"""
            await self.show_main_menu(callback)
        
        @self.app.on_callback_query(filters.regex(r"^back_help$"))
        @handle_errors
        async def cb_back_help(client, callback: CallbackQuery):
            """Back to help menu"""
            await self.show_help_menu(callback)
        
        @self.app.on_callback_query(filters.regex(r"^protection_main$"))
        @handle_errors
        async def cb_protection_main(client, callback: CallbackQuery):
            """Protection commands menu"""
            await self.show_protection_menu(callback)
        
        @self.app.on_callback_query(filters.regex(r"^admin_main$"))
        @handle_errors
        async def cb_admin_main(client, callback: CallbackQuery):
            """Admin commands menu"""
            await self.show_admin_menu(callback)
        
        @self.app.on_callback_query(filters.regex(r"^locks_main$"))
        @handle_errors
        async def cb_locks_main(client, callback: CallbackQuery):
            """Locks commands menu"""
            await self.show_locks_menu(callback)
        
        @self.app.on_callback_query(filters.regex(r"^staff_main$"))
        @handle_errors
        async def cb_staff_main(client, callback: CallbackQuery):
            """Staff menu"""
            await self.show_staff_menu(callback)
        
        @self.app.on_callback_query(filters.regex(r"^general_main$"))
        @handle_errors
        async def cb_general_main(client, callback: CallbackQuery):
            """General commands menu"""
            await self.show_general_menu(callback)
        
        # ==================== LANGUAGES ====================
        
        @self.app.on_callback_query(filters.regex(r"^languages_main$"))
        @handle_errors
        async def cb_languages_main(client, callback: CallbackQuery):
            """Languages menu"""
            await self.show_languages_menu(callback)
        
        @self.app.on_callback_query(filters.regex(r"^setlang_"))
        @handle_errors
        async def cb_setlang(client, callback: CallbackQuery):
            """Set language"""
            lang_code = callback.data.replace("setlang_", "")
            await self.set_language(callback, lang_code)
        
        # ==================== STATS ====================
        
        @self.app.on_callback_query(filters.regex(r"^stats_main$"))
        @handle_errors
        async def cb_stats_main(client, callback: CallbackQuery):
            """Stats menu"""
            await self.show_stats(callback)
        
        @self.app.on_callback_query(filters.regex(r"^stats_refresh$"))
        @handle_errors
        async def cb_stats_refresh(client, callback: CallbackQuery):
            """Refresh stats"""
            await self.show_stats(callback)
        
        # ==================== SETTINGS ====================
        
        @self.app.on_callback_query(filters.regex(r"^settings_main$"))
        @handle_errors
        async def cb_settings_main(client, callback: CallbackQuery):
            """Settings menu"""
            await self.show_settings(callback)
        
        @self.app.on_callback_query(filters.regex(r"^toggle_"))
        @handle_errors
        async def cb_toggle_setting(client, callback: CallbackQuery):
            """Toggle a setting"""
            setting = callback.data.replace("toggle_", "")
            await self.toggle_setting(callback, setting)
        
        # ==================== LOCKS ====================
        
        @self.app.on_callback_query(filters.regex(r"^locktypes_refresh$"))
        @handle_errors
        async def cb_locktypes_refresh(client, callback: CallbackQuery):
            """Refresh locktypes"""
            await self.show_locktypes(callback)
        
        @self.app.on_callback_query(filters.regex(r"^locktoggle_"))
        @handle_errors
        async def cb_lock_toggle(client, callback: CallbackQuery):
            """Toggle a lock"""
            lock_type = callback.data.replace("locktoggle_", "")
            await self.toggle_lock(callback, lock_type)
        
        # ==================== GENERAL COMMANDS ====================
        
        @self.app.on_callback_query(filters.regex(r"^general_main$"))
        @handle_errors
        async def cb_general_main(client, callback: CallbackQuery):
            """General commands menu"""
            await self.show_general_menu(callback)
        
        # ==================== COMMAND INFO ====================
        
        @self.app.on_callback_query(filters.regex(r"^cmd_"))
        @handle_errors
        async def cb_command_info(client, callback: CallbackQuery):
            """Show command info"""
            command = callback.data.replace("cmd_", "")
            await self.show_command_info(callback, command)
        
        # ==================== STAFF & LISTS ====================
        
        @self.app.on_callback_query(filters.regex(r"^staff_refresh$"))
        @handle_errors
        async def cb_staff_refresh(client, callback: CallbackQuery):
            """Refresh staff list"""
            await self.show_staff_list(callback)
        
        @self.app.on_callback_query(filters.regex(r"^gban_refresh$"))
        @handle_errors
        async def cb_gban_refresh(client, callback: CallbackQuery):
            """Refresh gban list"""
            await self.show_gban_list(callback)
        
        @self.app.on_callback_query(filters.regex(r"^approved_refresh$"))
        @handle_errors
        async def cb_approved_refresh(client, callback: CallbackQuery):
            """Refresh approved list"""
            await self.show_approved_list(callback)
        
        # ==================== USER ACTIONS ====================
        
        @self.app.on_callback_query(filters.regex(r"^warns_"))
        @handle_errors
        async def cb_show_warns(client, callback: CallbackQuery):
            """Show user warnings"""
            user_id = int(callback.data.replace("warns_", ""))
            await self.show_user_warns(callback, user_id)
        
        @self.app.on_callback_query(filters.regex(r"^resetwarns_"))
        @handle_errors
        async def cb_reset_warns(client, callback: CallbackQuery):
            """Reset user warnings"""
            user_id = int(callback.data.replace("resetwarns_", ""))
            await self.reset_user_warns(callback, user_id)
        
        @self.app.on_callback_query(filters.regex(r"^ban_"))
        @handle_errors
        async def cb_ban_user(client, callback: CallbackQuery):
            """Ban user from menu"""
            user_id = int(callback.data.replace("ban_", ""))
            await self.ban_user(callback, user_id)
        
        @self.app.on_callback_query(filters.regex(r"^unban_"))
        @handle_errors
        async def cb_unban_user(client, callback: CallbackQuery):
            """Unban user from menu"""
            user_id = int(callback.data.replace("unban_", ""))
            await self.unban_user(callback, user_id)
        
        # ==================== PING ====================
        
        @self.app.on_callback_query(filters.regex(r"^ping_retry$"))
        @handle_errors
        async def cb_ping_retry(client, callback: CallbackQuery):
            """Retry ping"""
            await self.show_ping(callback)
        
        # ==================== CLOSE ====================
        
        @self.app.on_callback_query(filters.regex(r"^close_message$"))
        @handle_errors
        async def cb_close_message(client, callback: CallbackQuery):
            """Close message"""
            try:
                await callback.message.delete()
            except:
                await callback.message.edit_text("✅ Message closed.")
            await callback.answer()
        
        # ==================== DEFAULT ====================
        
        @self.app.on_callback_query()
        @handle_errors
        async def cb_default(client, callback: CallbackQuery):
            """Default callback handler"""
            await callback.answer("Coming soon! 🚀", show_alert=False)
    
    # ==================== MENU FUNCTIONS ====================
    
    async def show_main_menu(self, callback: CallbackQuery):
        """Show main menu"""
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📖 Commands", callback_data="help_main"),
                InlineKeyboardButton("🛡️ Protection", callback_data="protection_main")
            ],
            [
                InlineKeyboardButton("⚙️ Settings", callback_data="settings_main"),
                InlineKeyboardButton("👥 Staff", callback_data="staff_main")
            ],
            [
                InlineKeyboardButton("🔒 Locks", callback_data="locks_main"),
                InlineKeyboardButton("👑 Admin", callback_data="admin_main")
            ],
            [
                InlineKeyboardButton("🌐 Language", callback_data="languages_main"),
                InlineKeyboardButton("📊 Stats", callback_data="stats_main")
            ],
            [
                InlineKeyboardButton("📢 Channel", url=config.bot.channel_link),
                InlineKeyboardButton("💬 Support", url=config.bot.support_link)
            ]
        ])
        
        text = f"""Hi, I'm **{config.bot.name}** {config.bot.god_status} Edition 👋

I'm your powerful Telegram protection bot 🛡️

I can help protect your groups from:
• Spam and malicious content
• Unwanted users
• Warning system
• Content locks
• And much more!

Use the buttons below to explore:"""
        
        try:
            await callback.message.edit_text(text, reply_markup=keyboard)
        except:
            await callback.message.reply_text(text, reply_markup=keyboard)
        await callback.answer()
    
    async def show_help_menu(self, callback: CallbackQuery):
        """Show help/commands menu"""
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🛡️ Protection", callback_data="protection_main"),
                InlineKeyboardButton("👑 Admin", callback_data="admin_main")
            ],
            [
                InlineKeyboardButton("🔒 Locks", callback_data="locks_main"),
                InlineKeyboardButton("👥 Staff", callback_data="staff_main")
            ],
            [
                InlineKeyboardButton("🌐 General", callback_data="general_main"),
                InlineKeyboardButton("🔙 Back", callback_data="back_main")
            ]
        ])
        
        text = """Here are all my available commands, organized by category:

🛡️ **Protection** - Anti-spam, anti-flood, anti-bot
👑 **Admin** - Ban, mute, warn, kick, etc.
🔒 **Locks** - Lock chat features
👥 **Staff** - Manage staff members
🌐 **General** - Info, stats, language

Click on a category above to see the commands! 👆"""
        
        try:
            await callback.message.edit_text(text, reply_markup=keyboard)
        except:
            await callback.message.reply_text(text, reply_markup=keyboard)
        await callback.answer()
    
    async def show_protection_menu(self, callback: CallbackQuery):
        """Show protection commands"""
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🛡️ Anti-Spam", callback_data="cmd_antispam"),
                InlineKeyboardButton("🌊 Anti-Flood", callback_data="cmd_antiflood")
            ],
            [
                InlineKeyboardButton("🤖 Anti-Bot", callback_data="cmd_antibot"),
                InlineKeyboardButton("⚔️ Anti-Raid", callback_data="cmd_antiraid")
            ],
            [
                InlineKeyboardButton("🎭 Anti-Scam", callback_data="cmd_antiscam"),
                InlineKeyboardButton("🔞 Anti-Porn", callback_data="cmd_antiporn")
            ],
            [
                InlineKeyboardButton("🔙 Back", callback_data="back_help")
            ]
        ])
        
        text = """**🛡️ Protection Commands**

Here are the protection features available:

• **Anti-Spam** - Automatically block spam messages
• **Anti-Flood** - Prevent message flooding
• **Anti-Bot** - Block users with suspicious usernames
• **Anti-Raid** - Protect against raid attacks
• **Anti-Scam** - Detect and remove scam messages
• **Anti-Porn** - Filter NSFW content

Click a button above to learn more! 👆"""
        
        try:
            await callback.message.edit_text(text, reply_markup=keyboard)
        except:
            await callback.message.reply_text(text, reply_markup=keyboard)
        await callback.answer()
    
    async def show_admin_menu(self, callback: CallbackQuery):
        """Show admin commands"""
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🔨 Ban/Unban", callback_data="cmd_ban"),
                InlineKeyboardButton("👢 Kick", callback_data="cmd_kick")
            ],
            [
                InlineKeyboardButton("🔇 Mute/Unmute", callback_data="cmd_mute"),
                InlineKeyboardButton("⚠️ Warn", callback_data="cmd_warn")
            ],
            [
                InlineKeyboardButton("📌 Pin/Unpin", callback_data="cmd_pin"),
                InlineKeyboardButton("🗑️ Purge", callback_data="cmd_purge")
            ],
            [
                InlineKeyboardButton("🔙 Back", callback_data="back_help")
            ]
        ])
        
        text = """**👑 Admin Commands**

Here are the admin tools available:

• **Ban/Unban** - Permanently ban or unban users
• **Kick** - Remove a user from the group
• **Mute/Unmute** - Temporarily mute a user
• **Warn** - Issue warnings to users
• **Pin/Unpin** - Pin messages in chat
• **Purge** - Delete multiple messages

Click a button above to learn more! 👆"""
        
        try:
            await callback.message.edit_text(text, reply_markup=keyboard)
        except:
            await callback.message.reply_text(text, reply_markup=keyboard)
        await callback.answer()
    
    async def show_locks_menu(self, callback: CallbackQuery):
        """Show locks commands"""
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🔗 Links", callback_data="locktoggle_links"),
                InlineKeyboardButton("🔄 Forwards", callback_data="locktoggle_forward")
            ],
            [
                InlineKeyboardButton("🎵 Audio", callback_data="locktoggle_audio"),
                InlineKeyboardButton("🎬 Video", callback_data="locktoggle_video")
            ],
            [
                InlineKeyboardButton("🖼️ Photos", callback_data="locktoggle_photo"),
                InlineKeyboardButton("📄 Documents", callback_data="locktoggle_document")
            ],
            [
                InlineKeyboardButton("🎭 Stickers", callback_data="locktoggle_sticker"),
                InlineKeyboardButton("📍 Locations", callback_data="locktoggle_location")
            ],
            [
                InlineKeyboardButton("🔄 Refresh", callback_data="locktypes_refresh"),
                InlineKeyboardButton("🔙 Back", callback_data="back_help")
            ]
        ])
        
        text = """**🔒 Lock Commands**

Use the buttons below to lock/unlock content types in your group:

• **Links** - Lock/Unlock sending links
• **Forwards** - Lock/Unlock forwarded messages
• **Audio** - Lock/Unlock audio files
• **Video** - Lock/Unlock video files
• **Photos** - Lock/Unlock photos
• **Documents** - Lock/Unlock documents
• **Stickers** - Lock/Unlock stickers
• **Locations** - Lock/Unlock location sharing

Click any button to toggle! 🔄"""
        
        try:
            await callback.message.edit_text(text, reply_markup=keyboard)
        except:
            await callback.message.reply_text(text, reply_markup=keyboard)
        await callback.answer()
    
    async def show_general_menu(self, callback: CallbackQuery):
        """Show general commands"""
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📊 Stats", callback_data="stats_main"),
                InlineKeyboardButton("🌐 Language", callback_data="languages_main")
            ],
            [
                InlineKeyboardButton("📋 Staff", callback_data="staff_main"),
                InlineKeyboardButton("📜 Rules", callback_data="cmd_rules")
            ],
            [
                InlineKeyboardButton("🔙 Back", callback_data="back_help")
            ]
        ])
        
        text = """
🌐 **General Commands**

These are general commands available to all users:

📊 **Stats** - View bot statistics and info
🌐 **Language** - Change the bot language
📋 **Staff** - View group staff members
📜 **Rules** - View group rules

Use the buttons above to explore! 👆
"""
        
        try:
            await callback.message.edit_text(text, reply_markup=keyboard)
        except:
            await callback.message.reply_text(text, reply_markup=keyboard)
        await callback.answer()
    
    async def show_staff_menu(self, callback: CallbackQuery):
        """Show staff menu"""
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("👥 Staff List", callback_data="staff_refresh"),
                InlineKeyboardButton("🚫 GBan List", callback_data="gban_refresh")
            ],
            [
                InlineKeyboardButton("✅ Approved List", callback_data="approved_refresh")
            ],
            [
                InlineKeyboardButton("🔙 Back", callback_data="back_main")
            ]
        ])
        
        text = """**👥 Staff Menu**

View and manage staff-related lists:

• **Staff List** - View all group admins
• **GBan List** - View globally banned users
• **Approved List** - View approved users

Use the buttons above to explore! 👆"""
        
        try:
            await callback.message.edit_text(text, reply_markup=keyboard)
        except:
            await callback.message.reply_text(text, reply_markup=keyboard)
        await callback.answer()
    
    # ==================== LANGUAGES ====================
    
    async def show_languages_menu(self, callback: CallbackQuery):
        """Show languages menu"""
        from i18n.translations import translator
        languages = translator.get_all_languages()
        
        buttons = []
        row = []
        
        for i, (code, name) in enumerate(languages.items(), 1):
            row.append(
                InlineKeyboardButton(
                    name,
                    callback_data=f"setlang_{code}"
                )
            )
            
            if i % 2 == 0:
                buttons.append(row)
                row = []
        
        if row:
            buttons.append(row)
        
        buttons.append([InlineKeyboardButton("🔙 Back", callback_data="back_main")])
        
        keyboard = InlineKeyboardMarkup(buttons)
        
        text = """**🌐 Select Your Language**

Choose your preferred language for the bot interface.

Click on a language button to change the language! 👆"""
        
        try:
            await callback.message.edit_text(text, reply_markup=keyboard)
        except:
            await callback.message.reply_text(text, reply_markup=keyboard)
        await callback.answer()
    
    async def set_language(self, callback: CallbackQuery, lang_code: str):
        """Set user language"""
        from i18n.translations import translator
        languages = translator.get_all_languages()
        
        if lang_code not in languages:
            await callback.answer("❌ Invalid language!", show_alert=True)
            return
        
        await callback.answer(f"✅ Language set to {languages[lang_code]}!", show_alert=True)
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="back_main")]
        ])
        
        try:
            await callback.message.edit_text(
                f"✅ **Language updated!**\n\nYour language has been set to **{languages[lang_code]}**.",
                reply_markup=keyboard
            )
        except:
            pass
    
    # ==================== STATS ====================
    
    async def show_stats(self, callback: CallbackQuery):
        """Show bot stats"""
        stats = await db.get_all_stats()
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Refresh", callback_data="stats_refresh")],
            [InlineKeyboardButton("🔙 Back", callback_data="back_main")]
        ])
        
        text = f"""**📊 Bot Statistics**

Here's some info about **{config.bot.name}**:

👥 **Total Users:** {stats.get('total_users', 'N/A')}
💬 **Total Chats:** {stats.get('total_chats', 'N/A')}
⚠️ **Total Warnings:** {stats.get('total_warnings', 'N/A')}
🚫 **Global Bans:** {stats.get('global_bans', 'N/A')}
🛡️ **Protected Groups:** {stats.get('protected_groups', 'N/A')}

Use the refresh button to update the stats! 🔄"""
        
        try:
            await callback.message.edit_text(text, reply_markup=keyboard)
        except:
            await callback.message.reply_text(text, reply_markup=keyboard)
        await callback.answer()
    
    # ==================== SETTINGS ====================
    
    async def show_settings(self, callback: CallbackQuery):
        """Show settings menu"""
        # Check if in group
        if callback.message.chat.type == ChatType.PRIVATE:
            await callback.answer("⚠️ Settings are only available in groups!", show_alert=True)
            return
        
        settings = await db.get_group_settings(callback.message.chat.id)
        
        if not settings:
            settings = await self.create_default_settings(callback.message.chat.id)
        
        antispam = "✅" if settings.antispam_enabled else "❌"
        antiflood = "✅" if settings.flood_enabled else "❌"
        welcome = "✅" if settings.welcome_enabled else "❌"
        goodbye = "✅" if settings.goodbye_enabled else "❌"
        locks = "✅" if settings.lock_enabled else "❌"
        reports = "✅" if settings.reports_enabled else "❌"
        
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(f"🛡️ AntiSpam {antispam}", callback_data="toggle_antispam"),
                InlineKeyboardButton(f"🌊 AntiFlood {antiflood}", callback_data="toggle_flood")
            ],
            [
                InlineKeyboardButton(f"👋 Welcome {welcome}", callback_data="toggle_welcome"),
                InlineKeyboardButton(f"👋 Goodbye {goodbye}", callback_data="toggle_goodbye")
            ],
            [
                InlineKeyboardButton(f"🔒 Locks {locks}", callback_data="locks_main"),
                InlineKeyboardButton(f"📝 Reports {reports}", callback_data="toggle_reports")
            ],
            [
                InlineKeyboardButton("🔙 Back", callback_data="back_main")
            ]
        ])
        
        text = f"""**⚙️ Chat Settings**

📢 **Group:** {callback.message.chat.title}

🛡️ **Protection:**
• Anti-Spam: {antispam}
• Anti-Flood: {antiflood}

✨ **Features:**
• Welcome: {welcome}
• Goodbye: {goodbye}
• Locks: {locks}
• Reports: {reports}"""
        
        try:
            await callback.message.edit_text(text, reply_markup=keyboard)
        except:
            await callback.message.reply_text(text, reply_markup=keyboard)
        await callback.answer()
    
    async def toggle_setting(self, callback: CallbackQuery, setting: str):
        """Toggle a chat setting"""
        if callback.message.chat.type == ChatType.PRIVATE:
            await callback.answer("⚠️ Settings are only available in groups!", show_alert=True)
            return
        
        settings = await db.get_group_settings(callback.message.chat.id)
        
        if not settings:
            settings = await self.create_default_settings(callback.message.chat.id)
        
        setting_map = {
            'antispam': 'antispam_enabled',
            'flood': 'flood_enabled',
            'welcome': 'welcome_enabled',
            'goodbye': 'goodbye_enabled',
            'reports': 'reports_enabled',
        }
        
        setting_key = setting_map.get(setting)
        
        if not setting_key:
            await callback.answer("❌ Invalid setting!", show_alert=True)
            return
        
        current_value = getattr(settings, setting_key, False)
        setattr(settings, setting_key, not current_value)
        await db.save_group_settings(settings)
        
        new_state = "Enabled" if not current_value else "Disabled"
        await callback.answer(f"✅ {setting.title()} {new_state}!", show_alert=True)
        
        # Refresh settings menu
        await self.show_settings(callback)
    
    async def create_default_settings(self, chat_id: int):
        """Create default settings for a chat"""
        from database.models import GroupSettings
        settings = GroupSettings(chat_id=chat_id)
        await db.save_group_settings(settings)
        return settings
    
    # ==================== LOCKS ====================
    
    async def show_locktypes(self, callback: CallbackQuery):
        """Show lock types"""
        # Check if in group
        if callback.message.chat.type == ChatType.PRIVATE:
            await callback.answer("⚠️ Locks are only available in groups!", show_alert=True)
            return
        
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
        
        settings = await db.get_group_settings(callback.message.chat.id)
        
        buttons = []
        row = []
        
        for i, (lock_key, lock_name, setting_key) in enumerate(lock_types, 1):
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
        
        buttons.append([InlineKeyboardButton("🔙 Back", callback_data="settings_main")])
        
        keyboard = InlineKeyboardMarkup(buttons)
        
        text = """**🔐 Lock Types**

Click to Lock/Unlock:
🔒 = Locked
🔓 = Unlocked"""
        
        try:
            await callback.message.edit_text(text, reply_markup=keyboard)
        except:
            await callback.message.reply_text(text, reply_markup=keyboard)
        await callback.answer()
    
    async def toggle_lock(self, callback: CallbackQuery, lock_type: str):
        """Toggle a lock"""
        if callback.message.chat.type == ChatType.PRIVATE:
            await callback.answer("⚠️ Locks are only available in groups!", show_alert=True)
            return
        
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
            settings = await self.create_default_settings(callback.message.chat.id)
        
        current_value = getattr(settings, setting_key, False)
        setattr(settings, setting_key, not current_value)
        await db.save_group_settings(settings)
        
        new_state = "Locked" if not current_value else "Unlocked"
        await callback.answer(f"✅ {lock_type.title()} {new_state}!", show_alert=True)
        
        # Refresh locktypes menu
        await self.show_locktypes(callback)
    
    # ==================== COMMAND INFO ====================
    
    async def show_command_info(self, callback: CallbackQuery, command: str):
        """Show info about a command"""
        commands_info = {
            "antispam": ("🛡️ Anti-Spam", "Toggles anti-spam protection.\n\nWhen enabled, the bot will automatically delete spam messages and warn/ban spammers.\n\n**Usage:** `/antispam`"),
            "antiflood": ("🌊 Anti-Flood", "Toggles anti-flood protection.\n\nWhen enabled, users who send too many messages in a short time will be muted.\n\n**Usage:** `/antiflood`"),
            "antibot": ("🤖 Anti-Bot", "Toggles anti-bot protection.\n\nPrevents new users with suspicious usernames from joining.\n\n**Usage:** `/antibot`"),
            "antiraid": ("⚔️ Anti-Raid", "Toggles anti-raid protection.\n\nWhen enabled, the bot will automatically ban users who join in rapid succession.\n\n**Usage:** `/antiraid`"),
            "antiscam": ("🎭 Anti-Scam", "Toggles anti-scam protection.\n\nAutomatically detects and removes known scam messages.\n\n**Usage:** `/antiscam`"),
            "antiporn": ("🔞 Anti-Porn", "Toggles NSFW content filter.\n\nAutomatically detects and removes adult content.\n\n**Usage:** `/antiporn`"),
            "ban": ("🔨 Ban", "Bans a user from the group.\n\nReply to a message or mention a user.\n\n**Usage:** Reply + `/ban`"),
            "kick": ("👢 Kick", "Kicks a user from the group (they can rejoin).\n\n**Usage:** Reply + `/kick`"),
            "mute": ("🔇 Mute", "Mutes a user so they can't send messages.\n\n**Usage:** Reply + `/mute`"),
            "unmute": ("🔊 Unmute", "Unmutes a previously muted user.\n\n**Usage:** Reply + `/unmute`"),
            "warn": ("⚠️ Warn", "Warns a user.\n\nAfter too many warnings, they get banned.\n\n**Usage:** Reply + `/warn`"),
            "pin": ("📌 Pin", "Pins a message in the chat.\n\n**Usage:** Reply + `/pin`"),
            "purge": ("🗑️ Purge", "Deletes multiple messages.\n\n**Usage:** Reply + `/purge`"),
            "rules": ("📜 Rules", "Shows the chat rules.\n\n**Usage:** `/rules`"),
        }
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="back_help")]
        ])
        
        if command in commands_info:
            title, description = commands_info[command]
            
            text = f"""**{title}**

{description}

**Note:** Most commands require admin privileges.
"""
        else:
            text = """**⚠️ Coming Soon!**

Command info is being prepared."""
        
        try:
            await callback.message.edit_text(text, reply_markup=keyboard)
        except:
            await callback.message.reply_text(text, reply_markup=keyboard)
        await callback.answer()
    
    # ==================== STAFF & LISTS ====================
    
    async def show_staff_list(self, callback: CallbackQuery):
        """Show staff list"""
        if callback.message.chat.type == ChatType.PRIVATE:
            await callback.answer("⚠️ Staff list is only available in groups!", show_alert=True)
            return
        
        staff = await db.get_staff(callback.message.chat.id)
        
        text = f"""**👥 Staff List**

📢 **Chat:** {callback.message.chat.title}"""
        
        if not staff:
            text += "\n\n❌ No staff members!"
        else:
            text += f"\n\n**Total:** {len(staff)} staff members\n\n"
            for i, member in enumerate(staff, 1):
                try:
                    user = await callback.client.get_users(member['user_id'])
                    text += f"{i}. {get_mention(user)} - {member.get('rank', 'Staff')}\n"
                except:
                    text += f"{i}. User {member['user_id']} - {member.get('rank', 'Staff')}\n"
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Refresh", callback_data="staff_refresh")],
            [InlineKeyboardButton("🔙 Back", callback_data="staff_main")]
        ])
        
        try:
            await callback.message.edit_text(text, reply_markup=keyboard)
        except:
            await callback.message.reply_text(text, reply_markup=keyboard)
        await callback.answer()
    
    async def show_gban_list(self, callback: CallbackQuery):
        """Show global ban list"""
        gbans = await db.get_global_bans()
        
        text = """**🚫 Global Ban List**"""
        
        if not gbans:
            text += "\n\n✅ No global bans!"
        else:
            text += f"\n\n**Total:** {len(gbans)} banned users\n\n"
            for i, gban in enumerate(gbans[:20], 1):
                try:
                    user = await callback.client.get_users(gban['user_id'])
                    text += f"{i}. {get_mention(user)}\n"
                    text += f"   Reason: {gban.get('reason', 'No reason')}\n\n"
                except:
                    text += f"{i}. User {gban['user_id']}\n"
                    text += f"   Reason: {gban.get('reason', 'No reason')}\n\n"
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Refresh", callback_data="gban_refresh")],
            [InlineKeyboardButton("🔙 Back", callback_data="staff_main")]
        ])
        
        try:
            await callback.message.edit_text(text, reply_markup=keyboard)
        except:
            await callback.message.reply_text(text, reply_markup=keyboard)
        await callback.answer()
    
    async def show_approved_list(self, callback: CallbackQuery):
        """Show approved users list"""
        if callback.message.chat.type == ChatType.PRIVATE:
            await callback.answer("⚠️ Approved list is only available in groups!", show_alert=True)
            return
        
        approved = await db.get_approved_users(callback.message.chat.id)
        
        text = f"""**✅ Approved Users**

📢 **Chat:** {callback.message.chat.title}"""
        
        if not approved:
            text += "\n\n❌ No approved users!"
        else:
            text += f"\n\n**Total:** {len(approved)} approved users\n\n"
            for i, user_data in enumerate(approved[:20], 1):
                try:
                    user = await callback.client.get_users(user_data['user_id'])
                    text += f"{i}. {get_mention(user)}\n"
                except:
                    text += f"{i}. User {user_data['user_id']}\n"
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Refresh", callback_data="approved_refresh")],
            [InlineKeyboardButton("🔙 Back", callback_data="staff_main")]
        ])
        
        try:
            await callback.message.edit_text(text, reply_markup=keyboard)
        except:
            await callback.message.reply_text(text, reply_markup=keyboard)
        await callback.answer()
    
    # ==================== USER ACTIONS ====================
    
    async def show_user_warns(self, callback: CallbackQuery, user_id: int):
        """Show user warnings"""
        if callback.message.chat.type == ChatType.PRIVATE:
            await callback.answer("⚠️ Warnings are only available in groups!", show_alert=True)
            return
        
        try:
            user = await callback.client.get_users(user_id)
        except:
            await callback.answer("❌ User not found!", show_alert=True)
            return
        
        warnings = await db.get_warnings(user_id, callback.message.chat.id)
        
        settings = await db.get_group_settings(callback.message.chat.id)
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
                InlineKeyboardButton("🗑️ Reset Warnings", callback_data=f"resetwarns_{user_id}"),
                InlineKeyboardButton("🔨 Ban", callback_data=f"ban_{user_id}")
            ],
            [InlineKeyboardButton("🔙 Back", callback_data="back_main")]
        ])
        
        try:
            await callback.message.edit_text(text, reply_markup=keyboard)
        except:
            await callback.message.reply_text(text, reply_markup=keyboard)
        await callback.answer()
    
    async def reset_user_warns(self, callback: CallbackQuery, user_id: int):
        """Reset user warnings"""
        if callback.message.chat.type == ChatType.PRIVATE:
            await callback.answer("⚠️ This action is only available in groups!", show_alert=True)
            return
        
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
    
    async def ban_user(self, callback: CallbackQuery, user_id: int):
        """Ban user"""
        if callback.message.chat.type == ChatType.PRIVATE:
            await callback.answer("⚠️ This action is only available in groups!", show_alert=True)
            return
        
        try:
            await callback.client.ban_chat_member(callback.message.chat.id, user_id)
            await callback.answer("✅ User banned!", show_alert=True)
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔓 Unban", callback_data=f"unban_{user_id}")],
                [InlineKeyboardButton("✅ Done", callback_data="close_message")]
            ])
            
            try:
                await callback.message.edit_reply_markup(reply_markup=keyboard)
            except:
                pass
        except Exception as e:
            await callback.answer(f"❌ Error: {str(e)}", show_alert=True)
    
    async def unban_user(self, callback: CallbackQuery, user_id: int):
        """Unban user"""
        if callback.message.chat.type == ChatType.PRIVATE:
            await callback.answer("⚠️ This action is only available in groups!", show_alert=True)
            return
        
        try:
            await callback.client.unban_chat_member(callback.message.chat.id, user_id)
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
    
    # ==================== PING ====================
    
    async def show_ping(self, callback: CallbackQuery):
        """Show ping result"""
        import time
        start_time = time.time()
        
        try:
            await callback.message.edit_text("🏓 Pong!")
        except:
            pass
        
        end_time = time.time()
        latency = round((end_time - start_time) * 1000, 2)
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Re-ping", callback_data="ping_retry")],
            [InlineKeyboardButton("🔙 Back", callback_data="back_main")]
        ])
        
        try:
            await callback.message.edit_text(
                f"🏓 **Pong!**\n\n⏱️ **Latency:** `{latency}ms`",
                reply_markup=keyboard
            )
        except:
            pass
        await callback.answer()
