# ═══════════════════════════════════════════════════════════════
# Geo Protection Bot - User Handlers
# ═══════════════════════════════════════════════════════════════

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.enums import ChatType
import logging

from config.config import config
from database.database import db
from utils.decorators import handle_errors, log_command
from utils.helpers import get_mention, get_username
from i18n.translations import get_text, translator

logger = logging.getLogger(__name__)


class UserHandlers:
    """Handle all user-related commands"""
    
    def __init__(self, app: Client):
        self.app = app
        self._register_handlers()
        self._register_callbacks()
    
    def _register_handlers(self):
        """Register command handlers"""
        
        # Start command
        @self.app.on_message(filters.command("start"))
        @log_command
        @handle_errors
        async def start_handler(client, message: Message):
            await self.handle_start(client, message)
        
        # Help command
        @self.app.on_message(filters.command("help"))
        @log_command
        @handle_errors
        async def help_handler(client, message: Message):
            await self.handle_help(client, message)
        
        # Language command
        @self.app.on_message(filters.command("setlang"))
        @log_command
        @handle_errors
        async def setlang_handler(client, message: Message):
            await self.handle_setlang(client, message)
        
        @self.app.on_message(filters.command("languages"))
        @log_command
        @handle_errors
        async def languages_handler(client, message: Message):
            await self.handle_languages(client, message)
        
        # Stats command
        @self.app.on_message(filters.command("stats"))
        @log_command
        @handle_errors
        async def stats_handler(client, message: Message):
            await self.handle_stats(client, message)
        
        # Info command
        @self.app.on_message(filters.command("info"))
        @log_command
        @handle_errors
        async def info_handler(client, message: Message):
            await self.handle_info(client, message)
        
        # ID command
        @self.app.on_message(filters.command("id"))
        @log_command
        @handle_errors
        async def id_handler(client, message: Message):
            await self.handle_id(client, message)
        
        # Ping command
        @self.app.on_message(filters.command("ping"))
        @log_command
        @handle_errors
        async def ping_handler(client, message: Message):
            await self.handle_ping(client, message)
        
        # About command
        @self.app.on_message(filters.command("about"))
        @log_command
        @handle_errors
        async def about_handler(client, message: Message):
            await self.handle_about(client, message)
        
        # Rules command
        @self.app.on_message(filters.command("rules"))
        @log_command
        @handle_errors
        async def rules_handler(client, message: Message):
            await self.handle_rules(client, message)
        
        # Settings command
        @self.app.on_message(filters.command("settings") & filters.group)
        @log_command
        @handle_errors
        async def settings_handler(client, message: Message):
            await self.handle_settings(client, message)
    
    def _register_callbacks(self):
        """Register callback handlers"""
        
        @self.app.on_callback_query(filters.regex(r"^(start|help|setlang|languages|stats|info|about|rules|settings)"))
        @handle_errors
        async def main_callback_handler(client, callback: CallbackQuery):
            await self.handle_callback(client, callback)
        
        # Back button handler
        @self.app.on_callback_query(filters.regex(r"^back_"))
        @handle_errors
        async def back_handler(client, callback: CallbackQuery):
            data = callback.data.replace("back_", "")
            if data == "main":
                await self.show_main_menu(callback)
            elif data == "help":
                await self.show_help_menu(callback)
            elif data == "protection":
                await self.show_protection_menu(callback)
            elif data == "admin":
                await self.show_admin_menu(callback)
    
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
                InlineKeyboardButton("🌐 Language", callback_data="languages_main"),
                InlineKeyboardButton("📊 Stats", callback_data="stats_main")
            ],
            [
                InlineKeyboardButton("📢 Channel", url="https://t.me/iMumd"),
                InlineKeyboardButton("💬 Support", url="https://t.me/iMumd")
            ]
        ])
        
        welcome_text = f"""
╔═══════════════════════════════════════════╗
║                                           ║
║   Welcome to **{config.bot.name}** {config.bot.god_status} Edition!    ║
║                                           ║
║   Your powerful Telegram protection bot   ║
║                                           ║
╚═══════════════════════════════════════════╝

🛡️ **I can help protect your groups from:**
• Spam and malicious content
• Unwanted users
• Warning system
• Content locks
• And much more!

👇 **Select an option below:**
"""
        
        try:
            await callback.message.edit_text(welcome_text, reply_markup=keyboard)
        except:
            await callback.message.reply_text(welcome_text, reply_markup=keyboard)
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
        
        help_text = """
╔═══════════════════════════════════════════╗
║                                           ║
║          📖 Available Commands 📖         ║
║                                           ║
╚═══════════════════════════════════════════╝

**Select a category to view commands:**

🛡️ **Protection** - Anti-spam, anti-flood, anti-bot
👑 **Admin** - Ban, mute, warn, kick, etc.
🔒 **Locks** - Lock chat features
👥 **Staff** - Manage staff members
🌐 **General** - Info, stats, language
"""
        
        try:
            await callback.message.edit_text(help_text, reply_markup=keyboard)
        except:
            await callback.message.reply_text(help_text, reply_markup=keyboard)
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
        
        text = """
╔═══════════════════════════════════════════╗
║          🛡️ Protection Commands 🛡️        ║
╚═══════════════════════════════════════════╝

**Click a command to get info:**
"""
        
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
        
        text = """
╔═══════════════════════════════════════════╗
║            👑 Admin Commands 👑           ║
╚═══════════════════════════════════════════╝

**Click a command to get info:**
"""
        
        try:
            await callback.message.edit_text(text, reply_markup=keyboard)
        except:
            await callback.message.reply_text(text, reply_markup=keyboard)
        await callback.answer()
    
    async def handle_start(self, client: Client, message: Message):
        """Handle /start command"""
        args = message.text.split()[1:]
        
        # Check if PM or group
        if message.chat.type == ChatType.PRIVATE:
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
                    InlineKeyboardButton("🌐 Language", callback_data="languages_main"),
                    InlineKeyboardButton("📊 Stats", callback_data="stats_main")
                ],
                [
                    InlineKeyboardButton("📢 Channel", url="https://t.me/iMumd"),
                    InlineKeyboardButton("💬 Support", url="https://t.me/iMumd")
                ]
            ])
            
            welcome_text = f"""
╔═══════════════════════════════════════════╗
║                                           ║
║   Welcome to **{config.bot.name}** {config.bot.god_status} Edition!    ║
║                                           ║
║   Your powerful Telegram protection bot   ║
║                                           ║
╚═══════════════════════════════════════════╝

🛡️ **I can help protect your groups from:**
• Spam and malicious content
• Unwanted users
• Warning system
• Content locks
• And much more!

👇 **Select an option below:**
"""
            
            await message.reply_text(welcome_text, reply_markup=keyboard)
        else:
            # In group
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("📖 Commands", callback_data="help_main")],
                [InlineKeyboardButton("🛡️ Protection", callback_data="protection_main")]
            ])
            
            await message.reply_text(
                f"👋 Hello! I'm **{config.bot.name}**, your group's protector!\n"
                f"👇 Use the buttons below to explore:",
                reply_markup=keyboard,
                disable_notification=True
            )
    
    async def handle_help(self, client: Client, message: Message):
        """Handle /help command"""
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
                InlineKeyboardButton("🔙 Menu", callback_data="start_main")
            ]
        ])
        
        help_text = """
╔═══════════════════════════════════════════╗
║                                           ║
║          📖 Available Commands 📖         ║
║                                           ║
╚═══════════════════════════════════════════╝

**Select a category to view commands:**

🛡️ **Protection** - Anti-spam, anti-flood, anti-bot
👑 **Admin** - Ban, mute, warn, kick, etc.
🔒 **Locks** - Lock chat features
👥 **Staff** - Manage staff members
🌐 **General** - Info, stats, language
"""
        
        await message.reply_text(help_text, reply_markup=keyboard)
    
    async def handle_setlang(self, client: Client, message: Message):
        """Handle /setlang command"""
        await self.show_language_selection(client, message)
    
    async def handle_languages(self, client: Client, message: Message):
        """Handle /languages command"""
        await self.show_language_selection(client, message)
    
    async def show_language_selection(self, client: Client, message: Message):
        """Show language selection keyboard"""
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
        
        buttons.append([InlineKeyboardButton("🔙 Back", callback_data="start_main")])
        
        keyboard = InlineKeyboardMarkup(buttons)
        
        text = """
╔═══════════════════════════════════════════╗
║          🌐 Select Your Language 🌐       ║
╚═══════════════════════════════════════════╝
"""
        
        await message.reply_text(text, reply_markup=keyboard)
    
    async def handle_stats(self, client: Client, message: Message):
        """Handle /stats command"""
        stats = await db.get_all_stats()
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Refresh", callback_data="stats_refresh")],
            [InlineKeyboardButton("🔙 Menu", callback_data="start_main")]
        ])
        
        text = f"""
╔═══════════════════════════════════════════╗
║            📊 Bot Statistics 📊            ║
╚═══════════════════════════════════════════╝

👥 **Total Users:** {stats.get('total_users', 'N/A')}
💬 **Total Chats:** {stats.get('total_chats', 'N/A')}
⚠️ **Total Warnings:** {stats.get('total_warnings', 'N/A')}
🚫 **Global Bans:** {stats.get('global_bans', 'N/A')}
🛡️ **Protected Groups:** {stats.get('protected_groups', 'N/A')}
"""
        
        await message.reply_text(text, reply_markup=keyboard)
    
    async def handle_info(self, client: Client, message: Message):
        """Handle /info command"""
        args = message.text.split()[1:]
        
        # Get user
        if not args:
            target = message.from_user
        elif message.reply_to_message:
            target = message.reply_to_message.from_user
        else:
            user_id = args[0]
            try:
                if user_id.startswith('@'):
                    target = await client.get_users(user_id)
                else:
                    target = await client.get_users(int(user_id))
            except:
                await message.reply_text("❌ User not found!")
                return
        
        # Get user info
        user_info = await db.get_user(target.id)
        
        text = f"""
╔═══════════════════════════════════════════╗
║              👤 User Info 👤              ║
╚═══════════════════════════════════════════╝

**Name:** {get_mention(target)}
**ID:** `{target.id}`
**Username:** @{target.username or 'None'}
**First Name:** {target.first_name or 'N/A'}
"""
        
        if target.last_name:
            text += f"**Last Name:** {target.last_name}\n"
        
        if user_info:
            text += f"**Warnings:** {user_info.get('warnings', 0)}\n"
        
        text += f"**Status:** {'Member' if not user_info else 'Known User'}\n"
        
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("⚠️ Warnings", callback_data=f"warns_{target.id}"),
                InlineKeyboardButton("🔨 Ban", callback_data=f"ban_{target.id}")
            ],
            [InlineKeyboardButton("🔙 Back", callback_data="start_main")]
        ])
        
        await message.reply_text(text, reply_markup=keyboard)
    
    async def handle_id(self, client: Client, message: Message):
        """Handle /id command"""
        if message.chat.type == ChatType.PRIVATE:
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Menu", callback_data="start_main")]
            ])
            
            await message.reply_text(
                f"📎 **Your ID:**\n`{message.from_user.id}`",
                reply_markup=keyboard,
                disable_notification=True
            )
        else:
            text = f"""
╔═══════════════════════════════════════════╗
║                 📎 IDs 📎                  ║
╚═══════════════════════════════════════════╝

**Chat ID:** `{message.chat.id}`
**Your ID:** `{message.from_user.id}`
"""
            
            if message.reply_to_message:
                text += f"**User ID:** `{message.reply_to_message.from_user.id}`\n"
                text += f"**Message ID:** `{message.reply_to_message.id}`\n"
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back", callback_data="start_main")]
            ])
            
            await message.reply_text(text, reply_markup=keyboard, disable_notification=True)
    
    async def handle_ping(self, client: Client, message: Message):
        """Handle /ping command"""
        import time
        start_time = time.time()
        
        msg = await message.reply_text("🏓 Pong!")
        
        end_time = time.time()
        latency = round((end_time - start_time) * 1000, 2)
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Re-ping", callback_data="ping_retry")],
            [InlineKeyboardButton("🔙 Menu", callback_data="start_main")]
        ])
        
        await msg.edit_text(
            f"🏓 **Pong!**\n\n⏱️ **Latency:** `{latency}ms`",
            reply_markup=keyboard
        )
    
    async def handle_about(self, client: Client, message: Message):
        """Handle /about command"""
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📖 Commands", callback_data="help_main"),
                InlineKeyboardButton("📢 Channel", url="https://t.me/iMumd")
            ],
            [
                InlineKeyboardButton("💬 Support", url="https://t.me/iMumd"),
                InlineKeyboardButton("🔙 Menu", callback_data="start_main")
            ]
        ])
        
        about_text = f"""
╔═══════════════════════════════════════════╗
║                                           ║
║          **{config.bot.name} Protection Bot**           ║
║                                           ║
║      {config.bot.god_status} Edition - Premium Security       ║
║                                           ║
╚═══════════════════════════════════════════╝

🤖 **Version:** 1.0.0
👑 **Developer:** iMumd
🌐 **Language:** Python 3.12+
📚 **Framework:** Pyrogram 2.0

✨ **Features:**
• Multi-threaded architecture
• Redis caching
• SQLite database
• 10+ languages
• God Mode support
• Advanced protection
• Admin tools
• Moderation suite

🔗 **Links:**
• GitHub: github.com/iMumd/Geo
• Channel: @iMumd
• Support: @iMumd
"""
        
        await message.reply_text(about_text, reply_markup=keyboard)
    
    async def handle_rules(self, client: Client, message: Message):
        """Handle /rules command"""
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📋 Staff", callback_data=f"staff_{message.chat.id}")],
            [InlineKeyboardButton("🔙 Back", callback_data="start_main")]
        ])
        
        rules_text = """
╔═══════════════════════════════════════════╗
║              📜 Chat Rules 📜             ║
╚═══════════════════════════════════════════╝

**1.** Respect all members
**2.** No spam or advertising
**3.** No NSFW or offensive content
**4.** No personal attacks or harassment
**5.** Follow admin instructions
**6.** Use appropriate language

⚠️ **Breaking rules may result in:**
• Warning
• Temporary mute
• Permanent mute
• Ban
"""
        
        await message.reply_text(rules_text, reply_markup=keyboard)
    
    async def handle_settings(self, client: Client, message: Message):
        """Handle /settings command"""
        settings = await db.get_group_settings(message.chat.id)
        
        if not settings:
            settings = await self.create_default_settings(message.chat.id)
        
        antispam = "✅" if settings.antispam_enabled else "❌"
        antiflood = "✅" if settings.flood_enabled else "❌"
        welcome = "✅" if settings.welcome_enabled else "❌"
        goodbye = "✅" if settings.goodbye_enabled else "❌"
        locks = "✅" if settings.lock_enabled else "❌"
        
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(f"🛡️ AntiSpam {antispam}", callback_data="toggle_antispam"),
                InlineKeyboardButton(f"🌊 AntiFlood {antiflood}", callback_data="toggle_antiflood")
            ],
            [
                InlineKeyboardButton(f"👋 Welcome {welcome}", callback_data="toggle_welcome"),
                InlineKeyboardButton(f"👋 Goodbye {goodbye}", callback_data="toggle_goodbye")
            ],
            [
                InlineKeyboardButton(f"🔒 Locks {locks}", callback_data="locks_main")
            ],
            [
                InlineKeyboardButton("🔙 Back", callback_data="start_main")
            ]
        ])
        
        text = f"""
╔═══════════════════════════════════════════╗
║            ⚙️ Chat Settings ⚙️            ║
╚═══════════════════════════════════════════╝

**Group:** {message.chat.title}
**ID:** `{message.chat.id}`

**Protection Status:**
🛡️ Anti-Spam: {antispam}
🌊 Anti-Flood: {antiflood}

**Features:**
👋 Welcome: {welcome}
👋 Goodbye: {goodbye}
🔒 Locks: {locks}
"""
        
        await message.reply_text(text, reply_markup=keyboard)
    
    async def create_default_settings(self, chat_id: int):
        """Create default settings for a chat"""
        from database.models import GroupSettings
        settings = GroupSettings(chat_id=chat_id)
        await db.save_group_settings(settings)
        return settings
    
    async def handle_callback(self, client: Client, callback: CallbackQuery):
        """Handle callback queries"""
        data = callback.data
        
        # Main menu navigation
        if data == "start_main":
            await self.show_main_menu(callback)
            return
        
        if data == "help_main":
            await self.show_help_menu(callback)
            return
        
        if data == "protection_main":
            await self.show_protection_menu(callback)
            return
        
        if data == "admin_main":
            await self.show_admin_menu(callback)
            return
        
        if data == "languages_main":
            await self.show_language_selection(client, callback.message)
            return
        
        if data == "stats_main":
            await self.show_stats_menu(callback)
            return
        
        if data == "settings_main":
            await self.show_settings_menu(callback)
            return
        
        # Language selection
        if data.startswith("setlang_"):
            lang_code = data.replace("setlang_", "")
            languages = translator.get_all_languages()
            
            if lang_code in languages:
                await callback.answer(f"✅ Language set to {languages[lang_code]}!", show_alert=True)
                await callback.message.edit_text(
                    f"✅ **Language updated!**\n\nYour language has been set to **{languages[lang_code]}**.\n\nClick below to go back:",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🔙 Back", callback_data="start_main")]
                    ])
                )
            else:
                await callback.answer("❌ Invalid language!", show_alert=True)
            return
        
        # Ping retry
        if data == "ping_retry":
            await self.handle_ping_retry(callback)
            return
        
        # Stats refresh
        if data == "stats_refresh":
            await self.show_stats_menu(callback)
            return
        
        # Command info buttons
        if data.startswith("cmd_"):
            await self.show_command_info(callback, data.replace("cmd_", ""))
            return
        
        # Unknown callback
        await callback.answer("Coming soon! 🚀", show_alert=True)
    
    async def show_stats_menu(self, callback: CallbackQuery):
        """Show stats with refresh button"""
        stats = await db.get_all_stats()
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Refresh", callback_data="stats_refresh")],
            [InlineKeyboardButton("🔙 Menu", callback_data="start_main")]
        ])
        
        text = f"""
╔═══════════════════════════════════════════╗
║            📊 Bot Statistics 📊            ║
╚═══════════════════════════════════════════╝

👥 **Total Users:** {stats.get('total_users', 'N/A')}
💬 **Total Chats:** {stats.get('total_chats', 'N/A')}
⚠️ **Total Warnings:** {stats.get('total_warnings', 'N/A')}
🚫 **Global Bans:** {stats.get('global_bans', 'N/A')}
🛡️ **Protected Groups:** {stats.get('protected_groups', 'N/A')}
"""
        
        try:
            await callback.message.edit_text(text, reply_markup=keyboard)
        except:
            await callback.message.reply_text(text, reply_markup=keyboard)
        await callback.answer()
    
    async def show_settings_menu(self, callback: CallbackQuery):
        """Show settings menu"""
        # Try to get chat ID from message
        chat_id = callback.message.chat.id if hasattr(callback.message.chat, 'id') else None
        
        if not chat_id or chat_id > 0:
            await callback.answer("⚠️ Settings are only available in groups!", show_alert=True)
            return
        
        settings = await db.get_group_settings(chat_id)
        
        if not settings:
            settings = await self.create_default_settings(chat_id)
        
        antispam = "✅" if settings.antispam_enabled else "❌"
        antiflood = "✅" if settings.flood_enabled else "❌"
        welcome = "✅" if settings.welcome_enabled else "❌"
        goodbye = "✅" if settings.goodbye_enabled else "❌"
        locks = "✅" if settings.lock_enabled else "❌"
        
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(f"🛡️ AntiSpam {antispam}", callback_data="toggle_antispam"),
                InlineKeyboardButton(f"🌊 AntiFlood {antiflood}", callback_data="toggle_antiflood")
            ],
            [
                InlineKeyboardButton(f"👋 Welcome {welcome}", callback_data="toggle_welcome"),
                InlineKeyboardButton(f"👋 Goodbye {goodbye}", callback_data="toggle_goodbye")
            ],
            [
                InlineKeyboardButton(f"🔒 Locks {locks}", callback_data="locks_main")
            ],
            [
                InlineKeyboardButton("🔙 Back", callback_data="start_main")
            ]
        ])
        
        text = f"""
╔═══════════════════════════════════════════╗
║            ⚙️ Chat Settings ⚙️            ║
╚═══════════════════════════════════════════╝

**Protection Status:**
🛡️ Anti-Spam: {antispam}
🌊 Anti-Flood: {antiflood}

**Features:**
👋 Welcome: {welcome}
👋 Goodbye: {goodbye}
🔒 Locks: {locks}

**Toggle features using the buttons below:**
"""
        
        try:
            await callback.message.edit_text(text, reply_markup=keyboard)
        except:
            await callback.message.reply_text(text, reply_markup=keyboard)
        await callback.answer()
    
    async def handle_ping_retry(self, callback: CallbackQuery):
        """Handle ping retry"""
        import time
        start_time = time.time()
        
        await callback.message.edit_text("🏓 Pong!")
        
        end_time = time.time()
        latency = round((end_time - start_time) * 1000, 2)
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Re-ping", callback_data="ping_retry")],
            [InlineKeyboardButton("🔙 Menu", callback_data="start_main")]
        ])
        
        await callback.message.edit_text(
            f"🏓 **Pong!**\n\n⏱️ **Latency:** `{latency}ms`",
            reply_markup=keyboard
        )
        await callback.answer()
    
    async def show_command_info(self, callback: CallbackQuery, command: str):
        """Show info about a specific command"""
        commands_info = {
            "antispam": ("🛡️ Anti-Spam", "Toggles anti-spam protection. When enabled, the bot will automatically delete spam messages and warn/ban spammers.\n\n**Usage:** `/antispam`"),
            "antiflood": ("🌊 Anti-Flood", "Toggles anti-flood protection. When enabled, users who send too many messages in a short time will be muted.\n\n**Usage:** `/antiflood`"),
            "antibot": ("🤖 Anti-Bot", "Toggles anti-bot protection. Prevents new users with suspicious usernames from joining.\n\n**Usage:** `/antibot`"),
            "antiraid": ("⚔️ Anti-Raid", "Toggles anti-raid protection. When enabled, the bot will automatically ban users who join in rapid succession (raid protection).\n\n**Usage:** `/antiraid`"),
            "antiscam": ("🎭 Anti-Scam", "Toggles anti-scam protection. Automatically detects and removes known scam messages.\n\n**Usage:** `/antiscam`"),
            "antiporn": ("🔞 Anti-Porn", "Toggles NSFW content filter. Automatically detects and removes adult content.\n\n**Usage:** `/antiporn`"),
            "ban": ("🔨 Ban", "Bans a user from the group. Reply to a message or mention a user.\n\n**Usage:** Reply to user and send `/ban`"),
            "unban": ("🔨 Unban", "Unbans a previously banned user.\n\n**Usage:** Reply to user and send `/unban`"),
            "kick": ("👢 Kick", "Kicks a user from the group (they can rejoin).\n\n**Usage:** Reply to user and send `/kick`"),
            "mute": ("🔇 Mute", "Mutes a user so they can't send messages.\n\n**Usage:** Reply to user and send `/mute`"),
            "unmute": ("🔊 Unmute", "Unmutes a previously muted user.\n\n**Usage:** Reply to user and send `/unmute`"),
            "warn": ("⚠️ Warn", "Warns a user. After too many warnings, they get banned.\n\n**Usage:** Reply to user and send `/warn`"),
            "pin": ("📌 Pin", "Pins a message in the chat.\n\n**Usage:** Reply to message and send `/pin`"),
            "purge": ("🗑️ Purge", "Deletes multiple messages. Reply to a message and use the command.\n\n**Usage:** Reply to message and send `/purge`")
        }
        
        if command in commands_info:
            title, description = commands_info[command]
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back", callback_data="back_help")]
            ])
            
            text = f"""
╔═══════════════════════════════════════════╗
║              {title}              ║
╚═══════════════════════════════════════════╝

{description}

**Note:** Most commands require admin privileges.
"""
            
            try:
                await callback.message.edit_text(text, reply_markup=keyboard)
            except:
                await callback.message.reply_text(text, reply_markup=keyboard)
        else:
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back", callback_data="back_help")]
            ])
            
            try:
                await callback.message.edit_text(
                    "⚠️ Command info coming soon!",
                    reply_markup=keyboard
                )
            except:
                pass
        
        await callback.answer()
