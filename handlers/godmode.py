# ═══════════════════════════════════════════════════════════════
# Geo Protection Bot - God Mode Handler
# ═══════════════════════════════════════════════════════════════

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from datetime import datetime
import asyncio
import subprocess
import sys
import os
import logging

from config.config import config
from database.database import db
from database.cache import cache
from utils.decorators import god_mode, handle_errors, log_command
from utils.helpers import get_mention, format_number, format_timestamp, get_timestamp
from i18n.translations import get_text

logger = logging.getLogger(__name__)


class GodModeHandler:
    """Handle God Mode (developer) commands"""
    
    def __init__(self, app: Client):
        self.app = app
        self._register_handlers()
    
    def _register_handlers(self):
        """Register God Mode command handlers"""
        
        @self.app.on_message(filters.command("god") & filters.private)
        @god_mode
        @log_command
        @handle_errors
        async def god_handler(client, message: Message):
            await self.handle_god(client, message)
        
        @self.app.on_message(filters.command("status") & filters.private)
        @god_mode
        @log_command
        @handle_errors
        async def status_handler(client, message: Message):
            await self.handle_status(client, message)
        
        @self.app.on_message(filters.command("stats") & filters.private)
        @god_mode
        @log_command
        @handle_errors
        async def god_stats_handler(client, message: Message):
            await self.handle_stats(client, message)
        
        @self.app.on_message(filters.command("broadcast") & filters.private)
        @god_mode
        @log_command
        @handle_errors
        async def broadcast_handler(client, message: Message):
            await self.handle_broadcast(client, message)
        
        @self.app.on_message(filters.command("groups") & filters.private)
        @god_mode
        @log_command
        @handle_errors
        async def groups_handler(client, message: Message):
            await self.handle_groups(client, message)
        
        @self.app.on_message(filters.command("leave") & filters.private)
        @god_mode
        @log_command
        @handle_errors
        async def leave_handler(client, message: Message):
            await self.handle_leave(client, message)
        
        @self.app.on_message(filters.command("restart") & filters.private)
        @god_mode
        @log_command
        @handle_errors
        async def restart_handler(client, message: Message):
            await self.handle_restart(client, message)
        
        @self.app.on_message(filters.command("shutdown") & filters.private)
        @god_mode
        @log_command
        @handle_errors
        async def shutdown_handler(client, message: Message):
            await self.handle_shutdown(client, message)
        
        @self.app.on_message(filters.command("backup") & filters.private)
        @god_mode
        @log_command
        @handle_errors
        async def backup_handler(client, message: Message):
            await self.handle_backup(client, message)
        
        @self.app.on_message(filters.command("eval") & filters.private)
        @god_mode
        @log_command
        @handle_errors
        async def eval_handler(client, message: Message):
            await self.handle_eval(client, message)
        
        @self.app.on_message(filters.command("exec") & filters.private)
        @god_mode
        @log_command
        @handle_errors
        async def exec_handler(client, message: Message):
            await self.handle_exec(client, message)
        
        @self.app.on_message(filters.command("logs") & filters.private)
        @god_mode
        @log_command
        @handle_errors
        async def logs_handler(client, message: Message):
            await self.handle_logs(client, message)
        
        @self.app.on_message(filters.command("gc") & filters.private)
        @god_mode
        @log_command
        @handle_errors
        async def gc_handler(client, message: Message):
            await self.handle_gc(client, message)
        
        @self.app.on_message(filters.command("chatlist") & filters.private)
        @god_mode
        @log_command
        @handle_errors
        async def chatlist_handler(client, message: Message):
            await self.handle_chatlist(client, message)
        
        @self.app.on_message(filters.command("userinfo") & filters.private)
        @god_mode
        @log_command
        @handle_errors
        async def userinfo_handler(client, message: Message):
            await self.handle_userinfo(client, message)
        
        @self.app.on_message(filters.command("banall") & filters.private)
        @god_mode
        @log_command
        @handle_errors
        async def banall_handler(client, message: Message):
            await self.handle_banall(client, message)
        
        @self.app.on_message(filters.command("unbanall") & filters.private)
        @god_mode
        @log_command
        @handle_errors
        async def unbanall_handler(client, message: Message):
            await self.handle_unbanall(client, message)
        
        @self.app.on_message(filters.command("refresh") & filters.private)
        @god_mode
        @log_command
        @handle_errors
        async def refresh_handler(client, message: Message):
            await self.handle_refresh(client, message)
        
        @self.app.on_message(filters.command("clearcache") & filters.private)
        @god_mode
        @log_command
        @handle_errors
        async def clearcache_handler(client, message: Message):
            await self.handle_clearcache(client, message)
        
        @self.app.on_message(filters.command("memory") & filters.private)
        @god_mode
        @log_command
        @handle_errors
        async def memory_handler(client, message: Message):
            await self.handle_memory(client, message)
        
        @self.app.on_message(filters.command("sysinfo") & filters.private)
        @god_mode
        @log_command
        @handle_errors
        async def sysinfo_handler(client, message: Message):
            await self.handle_sysinfo(client, message)
        
        @self.app.on_message(filters.command("update") & filters.private)
        @god_mode
        @log_command
        @handle_errors
        async def update_handler(client, message: Message):
            await self.handle_update(client, message)
    
    async def handle_god(self, client: Client, message: Message):
        """Show God Mode dashboard"""
        god_text = f"""
╔═══════════════════════════════════════════╗
║                                           ║
║     👑 Welcome {config.bot.god_status} Developer! 👑     ║
║                                           ║
║       Access Level: ULTIMATE               ║
║                                           ║
╚═══════════════════════════════════════════╝

🌟 **Available Commands:**

📊 **Monitoring:**
• `/status` - Bot status
• `/stats` - Statistics
• `/groups` - Active groups
• `/chatlist` - Chat list
• `/userinfo` - User info
• `/logs` - View logs
• `/memory` - Memory usage
• `/sysinfo` - System info

🔧 **Management:**
• `/broadcast` - Broadcast message
• `/restart` - Restart bot
• `/shutdown` - Shutdown bot
• `/backup` - Backup database
• `/leave` - Leave chat
• `/refresh` - Refresh data
• `/clearcache` - Clear cache

⚡ **Advanced:**
• `/eval` - Execute Python
• `/exec` - Execute command
• `/gc` - Garbage collection
• `/update` - Update bot

🎯 **Moderation:**
• `/banall` - Global ban
• `/unbanall` - Remove global ban
"""
        
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📊 Status", callback_data="god_status"),
                InlineKeyboardButton("📡 Broadcast", callback_data="god_broadcast")
            ],
            [
                InlineKeyboardButton("🔄 Restart", callback_data="god_restart"),
                InlineKeyboardButton("💾 Backup", callback_data="god_backup")
            ],
            [
                InlineKeyboardButton("⚡ Eval", callback_data="god_eval"),
                InlineKeyboardButton("📜 Logs", callback_data="god_logs")
            ],
            [
                InlineKeyboardButton("🛑 Shutdown", callback_data="god_shutdown")
            ]
        ])
        
        await message.reply_text(god_text, reply_markup=keyboard)
    
    async def handle_status(self, client: Client, message: Message):
        """Show bot status"""
        import psutil
        import time
        
        # Get bot info
        me = await client.get_me()
        
        # Get system info
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        uptime = time.time() - psutil.boot_time()
        days = int(uptime // 86400)
        hours = int((uptime % 86400) // 3600)
        minutes = int((uptime % 3600) // 60)
        
        status_text = f"""
╔═══════════════════════════════════════════╗
║                                           ║
║       👑 {config.bot.god_status} Status Panel 👑      ║
║                                           ║
╚═══════════════════════════════════════════╝

🤖 **Bot Information:**
• Name: {me.first_name}
• Username: @{me.username}
• ID: `{me.id}`
• Status: 🟢 Online

💻 **System Information:**
• CPU: {cpu_percent}%
• RAM: {memory.percent}% ({format_number(memory.used)}/{format_number(memory.total)})
• Disk: {disk.percent}% ({format_number(disk.used)}/{format_number(disk.total)})
• Uptime: {days}d {hours}h {minutes}m

⚙️ **Bot Configuration:**
• God Mode: {'✅' if config.bot.god_mode else '❌'} {config.bot.god_status}
• Workers: {config.performance.workers}
• Max Load: {config.performance.max_load}
• Database: {config.database.url.split('///')[-1]}
"""
        
        await message.reply_text(status_text)
    
    async def handle_stats(self, client: Client, message: Message):
        """Show comprehensive stats"""
        stats = await db.get_all_stats()
        
        text = f"""
📊 **God Mode Statistics**

👥 **Database Stats:**
• Total Users: {stats.get('total_users', 0)}
• Total Chats: {stats.get('total_chats', 0)}
• Warnings: {stats.get('total_warnings', 0)}
• Global Bans: {stats.get('global_bans', 0)}

📈 **Growth:**
• Messages: {stats.get('messages', 0)}
• Commands: {stats.get('commands', 0)}
• Reports: {stats.get('reports', 0)}
• Errors: {stats.get('errors', 0)}

🔐 **Security:**
• Spam Blocked: {stats.get('spam_blocked', 0)}
• Scam Blocked: {stats.get('scam_blocked', 0)}
• Raid Events: {stats.get('raid_events', 0)}
• Flood Events: {stats.get('flood_events', 0)}

🕐 Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        await message.reply_text(text)
    
    async def handle_broadcast(self, client: Client, message: Message):
        """Broadcast message to all chats"""
        args = message.text.split(maxsplit=1)
        
        if len(args) < 2:
            await message.reply_text("Usage: /broadcast <message>")
            return
        
        broadcast_text = args[1]
        
        # Get all chats
        sent_count = 0
        failed_count = 0
        
        async for dialog in client.iter_dialogs():
            if dialog.chat.type in ['group', 'supergroup']:
                try:
                    await client.send_message(
                        dialog.chat.id,
                        f"📢 **Broadcast from Developer:**\n\n{broadcast_text}"
                    )
                    sent_count += 1
                    await asyncio.sleep(0.5)  # Rate limit
                except Exception as e:
                    logger.error(f"Broadcast failed for {dialog.chat.id}: {e}")
                    failed_count += 1
        
        await message.reply_text(
            f"✅ Broadcast completed!\n\n📤 Sent: {sent_count}\n❌ Failed: {failed_count}"
        )
    
    async def handle_groups(self, client: Client, message: Message):
        """Show active groups"""
        groups = []
        
        async for dialog in client.iter_dialogs():
            if dialog.chat.type in ['group', 'supergroup']:
                try:
                    groups.append({
                        'id': dialog.chat.id,
                        'title': dialog.chat.title,
                        'members': dialog.chat.members_count or 0
                    })
                except:
                    pass
        
        if not groups:
            await message.reply_text("No groups found!")
            return
        
        # Sort by members
        groups.sort(key=lambda x: x['members'], reverse=True)
        
        text = f"👥 **Active Groups ({len(groups)}):**\n\n"
        
        for i, group in enumerate(groups[:30], 1):
            text += f"{i}. **{group['title']}**\n"
            text += f"   👥 {group['members']} | ID: `{group['id']}`\n\n"
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📤 Export List", callback_data="god_export_groups")]
        ])
        
        await message.reply_text(text, reply_markup=keyboard)
    
    async def handle_leave(self, client: Client, message: Message):
        """Leave a chat"""
        args = message.text.split()[1:]
        
        if not args:
            await message.reply_text("Usage: /leave <chat_id>")
            return
        
        try:
            chat_id = int(args[0])
            await client.leave_chat(chat_id)
            await message.reply_text(f"✅ Left chat {chat_id}")
        except Exception as e:
            await message.reply_text(f"❌ Error: {e}")
    
    async def handle_restart(self, client: Client, message: Message):
        """Restart the bot"""
        await message.reply_text("🔄 Bot is restarting...")
        
        # Save state
        await db.backup("restart_backup.db")
        
        # Restart script
        python = sys.executable
        os.execl(python, python, *sys.argv)
    
    async def handle_shutdown(self, client: Client, message: Message):
        """Shutdown the bot"""
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("⚠️ Confirm Shutdown", callback_data="god_confirm_shutdown"),
                InlineKeyboardButton("❌ Cancel", callback_data="god_cancel")
            ]
        ])
        
        await message.reply_text(
            "⚠️ **Are you sure you want to shutdown the bot?**",
            reply_markup=keyboard
        )
    
    async def handle_backup(self, client: Client, message: Message):
        """Backup the database"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = f"backup_{timestamp}.db"
            
            await db.backup(backup_path)
            
            await message.reply_text(
                f"✅ Database backed up to `{backup_path}`"
            )
        except Exception as e:
            await message.reply_text(f"❌ Backup failed: {e}")
    
    async def handle_eval(self, client: Client, message: Message):
        """Execute Python code"""
        args = message.text.split(maxsplit=1)
        
        if len(args) < 2:
            await message.reply_text("Usage: /eval <code>")
            return
        
        code = args[1]
        
        try:
            import ast
            
            # Safe evaluation
            result = eval(code, {"__builtins__": {}}, {
                "client": client,
                "message": message,
                "db": db,
                "cache": cache,
                "config": config
            })
            
            if result is not None:
                await message.reply_text(f"✅ Result:\n```\n{result}\n```")
            else:
                await message.reply_text("✅ Code executed successfully!")
        except Exception as e:
            await message.reply_text(f"❌ Error:\n```\n{e}\n```")
    
    async def handle_exec(self, client: Client, message: Message):
        """Execute shell command"""
        args = message.text.split(maxsplit=1)
        
        if len(args) < 2:
            await message.reply_text("Usage: /exec <command>")
            return
        
        command = args[1]
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            output = result.stdout or result.stderr or "No output"
            
            if len(output) > 4000:
                output = output[:4000] + "\n... (truncated)"
            
            await message.reply_text(
                f"```bash\n{output}\n```",
                disable_notification=True
            )
        except Exception as e:
            await message.reply_text(f"❌ Error: {e}")
    
    async def handle_logs(self, client: Client, message: Message):
        """Show bot logs"""
        args = message.text.split()[1:]
        
        # Read last lines of log file
        try:
            with open(config.logging.file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            count = int(args[0]) if args else 50
            lines = lines[-count:]
            
            text = ''.join(lines)
            
            if len(text) > 4000:
                text = text[-4000:]
            
            await message.reply_text(
                f"📜 Last {count} log lines:\n```\n{text}\n```",
                disable_notification=True
            )
        except FileNotFoundError:
            await message.reply_text("No log file found!")
        except Exception as e:
            await message.reply_text(f"❌ Error: {e}")
    
    async def handle_gc(self, client: Client, message: Message):
        """Run garbage collection"""
        import gc
        
        before = gc.collect()
        
        await message.reply_text(
            f"✅ Garbage collection completed!\n\n"
            f"Collected: {before} objects"
        )
    
    async def handle_chatlist(self, client: Client, message: Message):
        """Export chat list"""
        chats = []
        
        async for dialog in client.iter_dialogs():
            if dialog.chat.type in ['group', 'supergroup', 'channel']:
                chats.append({
                    'id': dialog.chat.id,
                    'title': dialog.chat.title,
                    'type': dialog.chat.type.value
                })
        
        if not chats:
            await message.reply_text("No chats found!")
            return
        
        text = f"📋 **Chat List ({len(chats)}):**\n\n"
        
        for chat in chats[:50]:
            text += f"• [{chat['type']}] {chat['title']} - `{chat['id']}`\n"
        
        await message.reply_text(text)
    
    async def handle_userinfo(self, client: Client, message: Message):
        """Get user info"""
        args = message.text.split()[1:]
        
        if not args:
            await message.reply_text("Usage: /userinfo <user_id>")
            return
        
        try:
            user_id = int(args[0])
            user = await client.get_users(user_id)
            
            text = f"""
👤 **User Info:**

• Name: {get_mention(user)}
• ID: `{user.id}`
• Username: @{user.username or 'None'}
• First Name: {user.first_name or 'N/A'}
• Last Name: {user.last_name or 'N/A'}
• Is Bot: {'Yes' if user.is_bot else 'No'}
• DC ID: {user.dc_id or 'N/A'}
"""
            
            await message.reply_text(text)
        except Exception as e:
            await message.reply_text(f"❌ Error: {e}")
    
    async def handle_banall(self, client: Client, message: Message):
        """Global ban user across all chats"""
        args = message.text.split()[1:]
        
        if not args:
            await message.reply_text("Usage: /banall <user_id> [reason]")
            return
        
        try:
            user_id = int(args[0])
            reason = ' '.join(args[1:]) if len(args) > 1 else "Violated rules"
            
            await db.add_global_ban(user_id, config.bot.developer_id, reason)
            
            await message.reply_text(
                f"🚫 User {user_id} globally banned!\nReason: {reason}"
            )
        except Exception as e:
            await message.reply_text(f"❌ Error: {e}")
    
    async def handle_unbanall(self, client: Client, message: Message):
        """Remove global ban"""
        args = message.text.split()[1:]
        
        if not args:
            await message.reply_text("Usage: /unbanall <user_id>")
            return
        
        try:
            user_id = int(args[0])
            await db.remove_global_ban(user_id)
            
            await message.reply_text(f"🔓 User {user_id} globally unbanned!")
        except Exception as e:
            await message.reply_text(f"❌ Error: {e}")
    
    async def handle_refresh(self, client: Client, message: Message):
        """Refresh bot data"""
        try:
            await db.initialize()
            await cache.connect()
            
            await message.reply_text("✅ Data refreshed!")
        except Exception as e:
            await message.reply_text(f"❌ Error: {e}")
    
    async def handle_clearcache(self, client: Client, message: Message):
        """Clear Redis cache"""
        try:
            await cache.flush_pattern("*")
            
            await message.reply_text("✅ Cache cleared!")
        except Exception as e:
            await message.reply_text(f"❌ Error: {e}")
    
    async def handle_memory(self, client: Client, message: Message):
        """Show memory usage"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        mem_info = process.memory_info()
        
        text = f"""
💾 **Memory Usage:**

🟢 RSS: {format_number(mem_info.rss)} ({mem_info.rss / 1024 / 1024:.2f} MB)
🟡 VMS: {format_number(mem_info.vms)} ({mem_info.vms / 1024 / 1024:.2f} MB)

📊 **System Memory:**
• Used: {format_number(psutil.virtual_memory().used)}
• Free: {format_number(psutil.virtual_memory().free)}
• Percent: {psutil.virtual_memory().percent}%
"""
        
        await message.reply_text(text)
    
    async def handle_sysinfo(self, client: Client, message: Message):
        """Show system information"""
        import psutil
        import platform
        
        text = f"""
🖥️ **System Information:**

💻 **Platform:**
• System: {platform.system()}
• Release: {platform.release()}
• Version: {platform.version()}
• Machine: {platform.machine()}
• Processor: {platform.processor()}

⚙️ **CPU:**
• Cores: {psutil.cpu_count(logical=False)} Physical / {psutil.cpu_count(logical=True)} Logical
• Usage: {psutil.cpu_percent(interval=1)}%
• Frequency: {psutil.cpu_freq().current if psutil.cpu_freq() else 'N/A'} MHz

💾 **Memory:**
• Total: {format_number(psutil.virtual_memory().total)}
• Available: {format_number(psutil.virtual_memory().available)}
• Usage: {psutil.virtual_memory().percent}%

💿 **Disk:**
• Total: {format_number(psutil.disk_usage('/').total)}
• Used: {format_number(psutil.disk_usage('/').used)}
• Free: {format_number(psutil.disk_usage('/').free)}
• Usage: {psutil.disk_usage('/').percent}%
"""
        
        await message.reply_text(text)
    
    async def handle_update(self, client: Client, message: Message):
        """Update bot from git"""
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("⚠️ Confirm Update", callback_data="god_confirm_update"),
                InlineKeyboardButton("❌ Cancel", callback_data="god_cancel")
            ]
        ])
        
        await message.reply_text(
            "⚠️ **Are you sure you want to update the bot?**",
            reply_markup=keyboard
        )