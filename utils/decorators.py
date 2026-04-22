# ═══════════════════════════════════════════════════════════════
# Geo Protection Bot - Decorators
# ═══════════════════════════════════════════════════════════════

import asyncio
import functools
from typing import Callable, Optional, Any
from pyrogram.filters import Filter
from pyrogram.types import Message, CallbackQuery
import logging

logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════
# CHECK DECORATORS
# ═══════════════════════════════════════════════════════════════

def handle_errors(func: Callable) -> Callable:
    """Handle errors in command handlers"""
    @functools.wraps(func)
    async def wrapper(client, message: Message, *args, **kwargs):
        try:
            return await func(client, message, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
            try:
                await message.reply(f"❌ Error: {str(e)}")
            except:
                pass
    return wrapper


def admin_only(func: Callable) -> Callable:
    """Decorator to restrict command to admins only"""
    @functools.wraps(func)
    async def wrapper(client, message: Message, *args, **kwargs):
        if message.chat.type in ['private', 'channel']:
            await message.reply("This command can only be used in groups!")
            return
        
        # Check if user is admin
        chat_member = await client.get_chat_member(message.chat.id, message.from_user.id)
        
        if chat_member.status not in ['creator', 'administrator']:
            await message.reply("❌ This command can only be used by admins!")
            return
        
        return await func(client, message, *args, **kwargs)
    
    return wrapper


def owner_only(func: Callable) -> Callable:
    """Decorator to restrict command to chat owner only"""
    @functools.wraps(func)
    async def wrapper(client, message: Message, *args, **kwargs):
        if message.chat.type in ['private', 'channel']:
            await message.reply("This command can only be used in groups!")
            return
        
        # Check if user is owner
        chat_member = await client.get_chat_member(message.chat.id, message.from_user.id)
        
        if chat_member.status != 'creator':
            await message.reply("❌ This command can only be used by the chat owner!")
            return
        
        return await func(client, message, *args, **kwargs)
    
    return wrapper


def god_mode(func: Callable) -> Callable:
    """Decorator to restrict command to God Mode developer only"""
    @functools.wraps(func)
    async def wrapper(client, message: Message, *args, **kwargs):
        from config.config import config
        
        user_id = message.from_user.id
        
        if not config.bot.god_mode:
            await message.reply("God Mode is disabled!")
            return
        
        if user_id != config.bot.developer_id:
            await message.reply("❌ This command is restricted to the bot developer only!")
            return
        
        return await func(client, message, *args, **kwargs)
    
    return wrapper


def private_chat_only(func: Callable) -> Callable:
    """Decorator to restrict command to private chat only"""
    @functools.wraps(func)
    async def wrapper(client, message: Message, *args, **kwargs):
        if message.chat.type != 'private':
            await message.reply("This command can only be used in private chat!")
            return
        
        return await func(client, message, *args, **kwargs)
    
    return wrapper


def group_chat_only(func: Callable) -> Callable:
    """Decorator to restrict command to group chats only"""
    @functools.wraps(func)
    async def wrapper(client, message: Message, *args, **kwargs):
        if message.chat.type == 'private':
            await message.reply("This command can only be used in groups!")
            return
        
        return await func(client, message, *args, **kwargs)
    
    return wrapper


def requires_args(min_args: int = 0, error_message: str = "Missing arguments!"):
    """Decorator to require minimum number of arguments"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(client, message: Message, *args, **kwargs):
            text = message.text or message.caption or ""
            parts = text.split()[1:]  # Remove command
            
            if len(parts) < min_args:
                await message.reply(error_message)
                return
            
            return await func(client, message, *args, **kwargs)
        
        return wrapper
    return decorator


def rate_limit(calls: int = 3, period: int = 60):
    """Rate limit decorator"""
    user_calls = {}
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(client, message: Message, *args, **kwargs):
            user_id = message.from_user.id
            now = asyncio.get_event_loop().time()
            
            # Clean old calls
            if user_id in user_calls:
                user_calls[user_id] = [t for t in user_calls[user_id] if now - t < period]
            else:
                user_calls[user_id] = []
            
            if len(user_calls[user_id]) >= calls:
                await message.reply(f"⚠️ Rate limit exceeded! Please wait {period} seconds.")
                return
            
            user_calls[user_id].append(now)
            return await func(client, message, *args, **kwargs)
        
        return wrapper
    return decorator


# ═══════════════════════════════════════════════════════════════
# CALLBACK HANDLER DECORATORS
# ═══════════════════════════════════════════════════════════════

def callback_data(data_prefix: str):
    """Decorator to handle callback queries with specific data prefix"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(client, callback: CallbackQuery, *args, **kwargs):
            if not callback.data.startswith(data_prefix):
                return
            
            return await func(client, callback, *args, **kwargs)
        
        return wrapper
    return decorator


def handle_callback_error(func: Callable) -> Callable:
    """Handle errors in callback handlers"""
    @functools.wraps(func)
    async def wrapper(client, callback: CallbackQuery, *args, **kwargs):
        try:
            return await func(client, callback, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error in callback {func.__name__}: {e}")
            try:
                await callback.answer(f"Error: {str(e)}", show_alert=True)
            except:
                pass
    
    return wrapper


# ═══════════════════════════════════════════════════════════════
# UTILITY DECORATORS
# ═══════════════════════════════════════════════════════════════

def async_cache(ttl: int = 300):
    """Cache async function results"""
    cache_store = {}
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)
            now = asyncio.get_event_loop().time()
            
            if key in cache_store:
                cached_time, cached_value = cache_store[key]
                if now - cached_time < ttl:
                    return cached_value
            
            value = await func(*args, **kwargs)
            cache_store[key] = (now, value)
            
            # Clean old entries
            cache_store.update({k: v for k, v in cache_store.items() 
                                if now - v[0] < ttl})
            
            return value
        
        return wrapper
    return decorator


def threaded(func: Callable) -> Callable:
    """Run function in thread pool"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        from concurrent.futures import ThreadPoolExecutor
        executor = ThreadPoolExecutor()
        future = executor.submit(func, *args, **kwargs)
        return future.result()
    
    return wrapper


def log_command(func: Callable) -> Callable:
    """Log command execution"""
    @functools.wraps(func)
    async def wrapper(client, message: Message, *args, **kwargs):
        user = message.from_user
        chat = message.chat
        command = message.text.split()[0] if message.text else "Unknown"
        
        logger.info(f"Command '{command}' called by {user.first_name} "
                   f"({user.id}) in {chat.title} ({chat.id})")
        
        return await func(client, message, *args, **kwargs)
    
    return wrapper


def typing_action(func: Callable) -> Callable:
    """Send typing action while processing"""
    @functools.wraps(func)
    async def wrapper(client, message: Message, *args, **kwargs):
        try:
            await message.chat.request("typing")
        except:
            pass
        
        return await func(client, message, *args, **kwargs)
    
    return wrapper


# ═══════════════════════════════════════════════════════════════
# FILTER FACTORIES
# ═══════════════════════════════════════════════════════════════

def create_filter(**kwargs) -> Filter:
    """Create custom filter based on message attributes"""
    async def filter_func(client, message: Message) -> bool:
        for key, value in kwargs.items():
            if hasattr(message, key):
                attr = getattr(message, key)
                if callable(value):
                    if not value(attr):
                        return False
                elif attr != value:
                    return False
        return True
    
    return Filter.create(filter_func)


class GeoFilters:
    """Custom filter classes"""
    
    @staticmethod
    def is_admin(chat_id: int):
        """Filter for admin users"""
        async def func(client, message: Message) -> bool:
            if message.chat.type in ['private', 'channel']:
                return False
            member = await client.get_chat_member(chat_id, message.from_user.id)
            return member.status in ['creator', 'administrator']
        return Filter.create(func)
    
    @staticmethod
    def is_owner(chat_id: int):
        """Filter for chat owner"""
        async def func(client, message: Message) -> bool:
            if message.chat.type in ['private', 'channel']:
                return False
            member = await client.get_chat_member(chat_id, message.from_user.id)
            return member.status == 'creator'
        return Filter.create(func)
    
    @staticmethod
    def has_reply():
        """Filter for messages with reply"""
        async def func(client, message: Message) -> bool:
            return message.reply_to_message is not None
        return Filter.create(func)
    
    @staticmethod
    def is_forwarded():
        """Filter for forwarded messages"""
        async def func(client, message: Message) -> bool:
            return message.forward_from or message.forward_from_chat
        return Filter.create(func)
    
    @staticmethod
    def contains_url():
        """Filter for messages with URLs"""
        from utils.helpers import contains_url
        async def func(client, message: Message) -> bool:
            return contains_url(message.text or "")
        return Filter.create(func)