# ═══════════════════════════════════════════════════════════════
# Geo Protection Bot - Database Manager
# ═══════════════════════════════════════════════════════════════

import asyncio
import aiosqlite
import json
from pathlib import Path
from typing import Optional, Dict, List, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import threading
from contextlib import asynccontextmanager
import logging

logger = logging.getLogger(__name__)


@dataclass
class GroupSettings:
    """Group settings model"""
    chat_id: int
    chat_title: str = ""
    welcome_enabled: bool = True
    goodbye_enabled: bool = True
    warns_limit: int = 3
    antispam_enabled: bool = True
    antispam_time: int = 100
    flood_enabled: bool = True
    flood_time: int = 5
    raid_protection_enabled: bool = False
    raid_protection_time: int = 300
    mute_time: int = 60
    language: str = "en"
    welcome_message: str = "Welcome {user}!"
    goodbye_message: str = "{user} left the chat"
    lock_links: bool = False
    lock_spam: bool = True
    lock_forward: bool = False
    lock_audio: bool = False
    lock_video: bool = False
    lock_photo: bool = False
    lock_document: bool = False
    lock_sticker: bool = False
    lock_location: bool = False
    lock_contact: bool = False
    lock_game: bool = False
    lock_inline: bool = False
    reports_enabled: bool = True
    clean_service_messages: bool = False


@dataclass
class UserWarning:
    """User warning model"""
    user_id: int
    chat_id: int
    warn_count: int
    warn_reason: str
    warned_by: int
    warned_at: datetime


@dataclass
class GlobalBan:
    """Global ban model"""
    user_id: int
    banned_by: int
    reason: str
    banned_at: datetime
    expires_at: Optional[datetime] = None


@dataclass
class StaffMember:
    """Staff member model"""
    user_id: int
    chat_id: int
    rank: str
    added_by: int
    added_at: datetime


class DatabaseManager:
    """Async SQLite database manager with thread safety"""
    
    def __init__(self, db_path: str = "geo.db"):
        self.db_path = db_path
        self._lock = asyncio.Lock()
        self._connection: Optional[aiosqlite.Connection] = None
        self._db_semaphore = asyncio.Semaphore(50)
        
    async def initialize(self):
        """Initialize database and create tables"""
        async with self._lock:
            self._connection = await aiosqlite.connect(self.db_path)
            self._connection.row_factory = aiosqlite.Row
            await self._create_tables()
            logger.info("Database initialized successfully")
    
    async def _create_tables(self):
        """Create all necessary tables"""
        queries = [
            """CREATE TABLE IF NOT EXISTS groups (
                chat_id INTEGER PRIMARY KEY,
                chat_title TEXT DEFAULT '',
                welcome_enabled INTEGER DEFAULT 1,
                goodbye_enabled INTEGER DEFAULT 1,
                warns_limit INTEGER DEFAULT 3,
                antispam_enabled INTEGER DEFAULT 1,
                antispam_time INTEGER DEFAULT 100,
                flood_enabled INTEGER DEFAULT 1,
                flood_time INTEGER DEFAULT 5,
                raid_protection_enabled INTEGER DEFAULT 0,
                raid_protection_time INTEGER DEFAULT 300,
                mute_time INTEGER DEFAULT 60,
                language TEXT DEFAULT 'en',
                welcome_message TEXT DEFAULT 'Welcome {user}!',
                goodbye_message TEXT DEFAULT '{user} left the chat',
                lock_links INTEGER DEFAULT 0,
                lock_spam INTEGER DEFAULT 1,
                lock_forward INTEGER DEFAULT 0,
                lock_audio INTEGER DEFAULT 0,
                lock_video INTEGER DEFAULT 0,
                lock_photo INTEGER DEFAULT 0,
                lock_document INTEGER DEFAULT 0,
                lock_sticker INTEGER DEFAULT 0,
                lock_location INTEGER DEFAULT 0,
                lock_contact INTEGER DEFAULT 0,
                lock_game INTEGER DEFAULT 0,
                lock_inline INTEGER DEFAULT 0,
                reports_enabled INTEGER DEFAULT 1,
                clean_service_messages INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""",
            """CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                language TEXT DEFAULT 'en',
                warnings INTEGER DEFAULT 0,
                total_warns INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""",
            """CREATE TABLE IF NOT EXISTS warnings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                chat_id INTEGER,
                warn_count INTEGER,
                reason TEXT,
                warned_by INTEGER,
                warned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (chat_id) REFERENCES groups(chat_id)
            )""",
            """CREATE TABLE IF NOT EXISTS global_bans (
                user_id INTEGER PRIMARY KEY,
                banned_by INTEGER,
                reason TEXT,
                banned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                active INTEGER DEFAULT 1
            )""",
            """CREATE TABLE IF NOT EXISTS staff (
                user_id INTEGER,
                chat_id INTEGER,
                rank TEXT,
                added_by INTEGER,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user_id, chat_id),
                FOREIGN KEY (chat_id) REFERENCES groups(chat_id)
            )""",
            """CREATE TABLE IF NOT EXISTS approved_users (
                user_id INTEGER,
                chat_id INTEGER,
                approved_by INTEGER,
                approved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user_id, chat_id)
            )""",
            """CREATE TABLE IF NOT EXISTS muted_users (
                user_id INTEGER,
                chat_id INTEGER,
                muted_by INTEGER,
                muted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                reason TEXT,
                PRIMARY KEY (user_id, chat_id)
            )""",
            """CREATE TABLE IF NOT EXISTS filtered_words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                word TEXT,
                added_by INTEGER,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (chat_id) REFERENCES groups(chat_id)
            )""",
            """CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                user_id INTEGER,
                action TEXT,
                message_id INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (chat_id) REFERENCES groups(chat_id)
            )""",
            """CREATE TABLE IF NOT EXISTS bot_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                stat_name TEXT UNIQUE,
                stat_value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""",
            """CREATE INDEX IF NOT EXISTS idx_warnings_user ON warnings(user_id)""",
            """CREATE INDEX IF NOT EXISTS idx_warnings_chat ON warnings(chat_id)""",
            """CREATE INDEX IF NOT EXISTS idx_global_bans_active ON global_bans(active)""",
            """CREATE INDEX IF NOT EXISTS idx_muted_users_expires ON muted_users(expires_at)""",
            """CREATE INDEX IF NOT EXISTS idx_chat_history_timestamp ON chat_history(timestamp)"""
        ]
        
        for query in queries:
            await self._connection.execute(query)
        
        await self._connection.commit()
    
    @asynccontextmanager
    async def acquire(self):
        """Acquire database connection with semaphore"""
        async with self._db_semaphore:
            yield self._connection
    
    # Group Management
    async def get_group_settings(self, chat_id: int) -> Optional[GroupSettings]:
        """Get group settings"""
        async with self.acquire() as conn:
            cursor = await conn.execute(
                "SELECT * FROM groups WHERE chat_id = ?", (chat_id,)
            )
            row = await cursor.fetchone()
            if row:
                return GroupSettings(**dict(row))
            return None
    
    async def save_group_settings(self, settings: GroupSettings):
        """Save or update group settings"""
        async with self.acquire() as conn:
            data = asdict(settings)
            await conn.execute("""
                INSERT OR REPLACE INTO groups 
                (chat_id, chat_title, welcome_enabled, goodbye_enabled, warns_limit,
                antispam_enabled, antispam_time, flood_enabled, flood_time,
                raid_protection_enabled, raid_protection_time, mute_time, language,
                welcome_message, goodbye_message, lock_links, lock_spam, lock_forward,
                lock_audio, lock_video, lock_photo, lock_document, lock_sticker,
                lock_location, lock_contact, lock_game, lock_inline, reports_enabled,
                clean_service_messages, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, tuple(data.values()))
            await conn.commit()
    
    # User Management
    async def get_user(self, user_id: int) -> Optional[Dict]:
        """Get user data"""
        async with self.acquire() as conn:
            cursor = await conn.execute(
                "SELECT * FROM users WHERE user_id = ?", (user_id,)
            )
            return await cursor.fetchone()
    
    async def save_user(self, user_id: int, username: str = None, 
                       first_name: str = None, last_name: str = None):
        """Save or update user"""
        async with self.acquire() as conn:
            await conn.execute("""
                INSERT OR REPLACE INTO users 
                (user_id, username, first_name, last_name, updated_at)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (user_id, username, first_name, last_name))
            await conn.commit()
    
    # Warnings
    async def add_warning(self, user_id: int, chat_id: int, reason: str, 
                         warned_by: int) -> int:
        """Add warning and return new count"""
        async with self.acquire() as conn:
            await conn.execute("""
                INSERT INTO warnings (user_id, chat_id, reason, warned_by)
                VALUES (?, ?, ?, ?)
            """, (user_id, chat_id, reason, warned_by))
            
            cursor = await conn.execute("""
                SELECT COUNT(*) FROM warnings 
                WHERE user_id = ? AND chat_id = ?
            """, (user_id, chat_id))
            count = (await cursor.fetchone())[0]
            
            await conn.execute("""
                UPDATE users SET warnings = ? WHERE user_id = ?
            """, (count, user_id))
            
            await conn.commit()
            return count
    
    async def get_warnings(self, user_id: int, chat_id: int) -> List[Dict]:
        """Get all warnings for user in chat"""
        async with self.acquire() as conn:
            cursor = await conn.execute("""
                SELECT * FROM warnings 
                WHERE user_id = ? AND chat_id = ?
                ORDER BY warned_at DESC
            """, (user_id, chat_id))
            return await cursor.fetchall()
    
    async def remove_warning(self, warning_id: int):
        """Remove warning by ID"""
        async with self.acquire() as conn:
            await conn.execute(
                "DELETE FROM warnings WHERE id = ?", (warning_id,)
            )
            await conn.commit()
    
    async def clear_warnings(self, user_id: int, chat_id: int):
        """Clear all warnings for user in chat"""
        async with self.acquire() as conn:
            await conn.execute("""
                DELETE FROM warnings WHERE user_id = ? AND chat_id = ?
            """, (user_id, chat_id))
            await conn.execute("""
                UPDATE users SET warnings = 0 WHERE user_id = ?
            """, (user_id,))
            await conn.commit()
    
    # Global Bans
    async def add_global_ban(self, user_id: int, banned_by: int, reason: str,
                           expires_at: datetime = None):
        """Add global ban"""
        async with self.acquire() as conn:
            await conn.execute("""
                INSERT OR REPLACE INTO global_bans 
                (user_id, banned_by, reason, expires_at, active)
                VALUES (?, ?, ?, ?, 1)
            """, (user_id, banned_by, reason, expires_at))
            await conn.commit()
    
    async def remove_global_ban(self, user_id: int):
        """Remove global ban"""
        async with self.acquire() as conn:
            await conn.execute("""
                UPDATE global_bans SET active = 0 WHERE user_id = ?
            """, (user_id,))
            await conn.commit()
    
    async def is_globally_banned(self, user_id: int) -> bool:
        """Check if user is globally banned"""
        async with self.acquire() as conn:
            cursor = await conn.execute("""
                SELECT 1 FROM global_bans 
                WHERE user_id = ? AND active = 1
                AND (expires_at IS NULL OR expires_at > CURRENT_TIMESTAMP)
            """, (user_id,))
            return await cursor.fetchone() is not None
    
    async def get_global_bans(self) -> List[Dict]:
        """Get all active global bans"""
        async with self.acquire() as conn:
            cursor = await conn.execute("""
                SELECT * FROM global_bans WHERE active = 1
                ORDER BY banned_at DESC
            """)
            return await cursor.fetchall()
    
    # Muted Users
    async def mute_user(self, user_id: int, chat_id: int, muted_by: int,
                       duration: int = None, reason: str = None):
        """Mute user temporarily or permanently"""
        expires_at = None
        if duration:
            expires_at = datetime.now() + timedelta(seconds=duration)
        
        async with self.acquire() as conn:
            await conn.execute("""
                INSERT OR REPLACE INTO muted_users 
                (user_id, chat_id, muted_by, expires_at, reason)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, chat_id, muted_by, expires_at, reason))
            await conn.commit()
    
    async def unmute_user(self, user_id: int, chat_id: int):
        """Unmute user"""
        async with self.acquire() as conn:
            await conn.execute("""
                DELETE FROM muted_users 
                WHERE user_id = ? AND chat_id = ?
            """, (user_id, chat_id))
            await conn.commit()
    
    async def is_muted(self, user_id: int, chat_id: int) -> bool:
        """Check if user is muted"""
        async with self.acquire() as conn:
            cursor = await conn.execute("""
                SELECT 1 FROM muted_users 
                WHERE user_id = ? AND chat_id = ?
                AND (expires_at IS NULL OR expires_at > CURRENT_TIMESTAMP)
            """, (user_id, chat_id))
            return await cursor.fetchone() is not None
    
    # Staff Management
    async def add_staff(self, user_id: int, chat_id: int, rank: str, added_by: int):
        """Add staff member"""
        async with self.acquire() as conn:
            await conn.execute("""
                INSERT OR REPLACE INTO staff 
                (user_id, chat_id, rank, added_by)
                VALUES (?, ?, ?, ?)
            """, (user_id, chat_id, rank, added_by))
            await conn.commit()
    
    async def remove_staff(self, user_id: int, chat_id: int):
        """Remove staff member"""
        async with self.acquire() as conn:
            await conn.execute("""
                DELETE FROM staff WHERE user_id = ? AND chat_id = ?
            """, (user_id, chat_id))
            await conn.commit()
    
    async def get_staff(self, chat_id: int) -> List[Dict]:
        """Get all staff in chat"""
        async with self.acquire() as conn:
            cursor = await conn.execute("""
                SELECT * FROM staff WHERE chat_id = ?
                ORDER BY added_at DESC
            """, (chat_id,))
            return await cursor.fetchall()
    
    async def is_staff(self, user_id: int, chat_id: int) -> bool:
        """Check if user is staff"""
        async with self.acquire() as conn:
            cursor = await conn.execute("""
                SELECT 1 FROM staff 
                WHERE user_id = ? AND chat_id = ?
            """, (user_id, chat_id))
            return await cursor.fetchone() is not None
    
    # Approved Users
    async def approve_user(self, user_id: int, chat_id: int, approved_by: int):
        """Approve user"""
        async with self.acquire() as conn:
            await conn.execute("""
                INSERT OR REPLACE INTO approved_users 
                (user_id, chat_id, approved_by)
                VALUES (?, ?, ?)
            """, (user_id, chat_id, approved_by))
            await conn.commit()
    
    async def disapprove_user(self, user_id: int, chat_id: int):
        """Remove user approval"""
        async with self.acquire() as conn:
            await conn.execute("""
                DELETE FROM approved_users 
                WHERE user_id = ? AND chat_id = ?
            """, (user_id, chat_id))
            await conn.commit()
    
    async def is_approved(self, user_id: int, chat_id: int) -> bool:
        """Check if user is approved"""
        async with self.acquire() as conn:
            cursor = await conn.execute("""
                SELECT 1 FROM approved_users 
                WHERE user_id = ? AND chat_id = ?
            """, (user_id, chat_id))
            return await cursor.fetchone() is not None
    
    # Filtered Words
    async def add_filtered_word(self, chat_id: int, word: str, added_by: int):
        """Add filtered word"""
        async with self.acquire() as conn:
            await conn.execute("""
                INSERT INTO filtered_words (chat_id, word, added_by)
                VALUES (?, ?, ?)
            """, (chat_id, word, added_by))
            await conn.commit()
    
    async def remove_filtered_word(self, word_id: int):
        """Remove filtered word"""
        async with self.acquire() as conn:
            await conn.execute("""
                DELETE FROM filtered_words WHERE id = ?
            """, (word_id,))
            await conn.commit()
    
    async def get_filtered_words(self, chat_id: int) -> List[str]:
        """Get all filtered words in chat"""
        async with self.acquire() as conn:
            cursor = await conn.execute("""
                SELECT word FROM filtered_words WHERE chat_id = ?
            """, (chat_id,))
            rows = await cursor.fetchall()
            return [row[0] for row in rows]
    
    # Statistics
    async def increment_stat(self, stat_name: str, value: int = 1):
        """Increment a statistic"""
        async with self.acquire() as conn:
            await conn.execute("""
                INSERT INTO bot_stats (stat_name, stat_value, updated_at)
                VALUES (?, ?)
                ON CONFLICT(stat_name) DO UPDATE SET
                stat_value = stat_value + excluded.stat_value,
                updated_at = CURRENT_TIMESTAMP
            """, (stat_name, str(value)))
            await conn.commit()
    
    async def get_stat(self, stat_name: str) -> Optional[int]:
        """Get a statistic value"""
        async with self.acquire() as conn:
            cursor = await conn.execute("""
                SELECT stat_value FROM bot_stats WHERE stat_name = ?
            """, (stat_name,))
            row = await cursor.fetchone()
            return int(row[0]) if row else None
    
    async def get_all_stats(self) -> Dict[str, int]:
        """Get all statistics"""
        async with self.acquire() as conn:
            cursor = await conn.execute("""
                SELECT stat_name, stat_value FROM bot_stats
            """)
            rows = await cursor.fetchall()
            return {row[0]: int(row[1]) for row in rows}
    
    # Backup
    async def backup(self, backup_path: str = None):
        """Backup database"""
        if not backup_path:
            backup_path = f"geo_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        
        async with self.acquire() as conn:
            await conn.execute(f"VACUUM INTO '{backup_path}'")
            logger.info(f"Database backed up to {backup_path}")
    
    async def close(self):
        """Close database connection"""
        async with self._lock:
            if self._connection:
                await self._connection.close()
                logger.info("Database connection closed")


# Global database instance
db = DatabaseManager()