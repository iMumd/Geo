# ═══════════════════════════════════════════════════════════════
# Geo Protection Bot - Helper Functions
# ═══════════════════════════════════════════════════════════════

import re
import html
import time
from typing import Optional, List, Dict, Any, Union
from datetime import datetime, timedelta
from functools import wraps
import asyncio
import logging

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════
# STRING UTILITIES
# ═══════════════════════════════════════════════════════════════

def escape_markdown(text: str) -> str:
    """Escape markdown special characters"""
    escape_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '!', '.']
    for char in escape_chars:
        text = text.replace(char, f'\\{char}')
    return text


def escape_html(text: str) -> str:
    """Escape HTML special characters"""
    return html.escape(str(text))


def format_duration(seconds: int) -> str:
    """Format seconds to human readable duration"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes}m"
    elif seconds < 86400:
        hours = seconds // 3600
        return f"{hours}h"
    else:
        days = seconds // 86400
        return f"{days}d"


def parse_duration(duration_str: str) -> int:
    """Parse duration string to seconds"""
    match = re.match(r'(\d+)([smhd])?', duration_str.lower())
    if not match:
        return 0
    
    value, unit = match.groups()
    value = int(value)
    
    if unit == 's':
        return value
    elif unit == 'm':
        return value * 60
    elif unit == 'h':
        return value * 3600
    elif unit == 'd':
        return value * 86400
    else:
        return value


def get_mention(user: Any, name: Optional[str] = None) -> str:
    """Get user mention with HTML formatting"""
    name = name or (user.first_name or "User")
    user_id = getattr(user, 'id', None)
    if not user_id:
        return escape_html(name)
    return f"<a href='tg://user?id={user_id}'>{escape_html(name)}</a>"


def get_username(user: Any) -> str:
    """Get user display name"""
    if getattr(user, 'username', None):
        return f"@{user.username}"
    first_name = getattr(user, 'first_name', 'User')
    last_name = getattr(user, 'last_name', '')
    full_name = f"{first_name} {last_name}".strip()
    return get_mention(user, full_name or "User")


def truncate(text: str, length: int, suffix: str = "...") -> str:
    """Truncate text to length"""
    if len(text) <= length:
        return text
    return text[:length - len(suffix)] + suffix


# ═══════════════════════════════════════════════════════════════
# REGEX PATTERNS
# ═══════════════════════════════════════════════════════════════

# Spam patterns
SPAM_PATTERNS = [
    r'(?=.{1,50}?(?:[A-Za-z]{3,}).{1,50}?)(([A-Za-z]{3,})\2{5,})',
    r'(?i)\b(viagra|cialis|casino|lottery|winner|prize|free|money)\b',
    r'(?i)(?:https?://)?(?:[a-zA-Z0-9-]+\.)+(?:com|net|org|info|biz|ru|cn|pw|cc|top|site|online)\b',
    r'(?i)(?:https?://)?(?:bit\.ly|tinyurl|t\.co|goo\.gl|short\.to)\b',
]

# Scam patterns
SCAM_PATTERNS = [
    r'(?i)\b(giveaway|airdrop|crypto|btc|eth|wallet|private.?key)\b',
    r'(?i)\b(urgent|hack|exploit|security.?alert)\b',
    r'(?i)\b(free.?bitcoin|double.?your.?money)\b',
]

# Link patterns
URL_PATTERN = re.compile(
    r'(?:https?://)?'
    r'(?:(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}|'
    r'localhost|'
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    r'(?::\d+)?'
    r'(?:/[^\s]*)?',
    re.IGNORECASE
)

# Mention patterns
MENTION_PATTERN = re.compile(r'@[a-zA-Z0-9_]{5,32}')

# Hashtag pattern
HASHTAG_PATTERN = re.compile(r'#[a-zA-Z0-9_]+')

# Command pattern
COMMAND_PATTERN = re.compile(r'^/([a-zA-Z0-9_]+)(@[\w]+)?(\s.*)?$')


def extract_urls(text: str) -> List[str]:
    """Extract all URLs from text"""
    return URL_PATTERN.findall(text)


def extract_mentions(text: str) -> List[str]:
    """Extract all mentions from text"""
    return MENTION_PATTERN.findall(text)


def extract_hashtags(text: str) -> List[str]:
    """Extract all hashtags from text"""
    return HASHTAG_PATTERN.findall(text)


def is_spam(text: str) -> bool:
    """Check if text is spam"""
    for pattern in SPAM_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


def is_scam(text: str) -> bool:
    """Check if text is scam"""
    for pattern in SCAM_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


def contains_url(text: str) -> bool:
    """Check if text contains URL"""
    return bool(URL_PATTERN.search(text))


def extract_command(text: str) -> Optional[Dict[str, Any]]:
    """Extract command from message text"""
    match = COMMAND_PATTERN.match(text.strip())
    if match:
        command, bot_username, args = match.groups()
        return {
            'command': command.lower(),
            'bot_username': bot_username.lstrip('@') if bot_username else None,
            'args': args.strip() if args else None
        }
    return None


# ═══════════════════════════════════════════════════════════════
# DATA UTILITIES
# ═══════════════════════════════════════════════════════════════

def parse_user_id(text: str) -> Optional[int]:
    """Parse user ID from text (mentions, IDs, usernames)"""
    text = text.strip()
    
    # Direct numeric ID
    if text.isdigit():
        return int(text)
    
    # Mention
    mention_match = re.match(r'@([a-zA-Z0-9_]{5,32})', text)
    if mention_match:
        return mention_match.group(1)  # Return username for later resolution
    
    # User ID mention
    id_match = re.match(r'id(\d+)', text, re.IGNORECASE)
    if id_match:
        return int(id_match.group(1))
    
    # Forwarded user
    return None


def parse_chat_id(text: str) -> Optional[int]:
    """Parse chat ID from text"""
    text = text.strip()
    
    if text.startswith('-100') and text[1:].isdigit():
        return int(text)
    
    if text.startswith('@'):
        return text  # Return username for later resolution
    
    return None


def build_keyboard(buttons: List[List[Dict[str, str]]]) -> List[List[Dict]]:
    """Build inline keyboard from button data"""
    keyboard = []
    for row in buttons:
        keyboard_row = []
        for button in row:
            if button.get('callback_data'):
                keyboard_row.append({
                    'text': button['text'],
                    'callback_data': button['callback_data']
                })
            elif button.get('url'):
                keyboard_row.append({
                    'text': button['text'],
                    'url': button['url']
                })
        if keyboard_row:
            keyboard.append(keyboard_row)
    return keyboard


# ═══════════════════════════════════════════════════════════════
# TIME UTILITIES
# ═══════════════════════════════════════════════════════════════

def get_timestamp() -> int:
    """Get current Unix timestamp"""
    return int(time.time())


def format_timestamp(timestamp: int, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format Unix timestamp"""
    return datetime.fromtimestamp(timestamp).strftime(fmt)


def time_ago(timestamp: int) -> str:
    """Get human-readable time ago"""
    now = datetime.now()
    then = datetime.fromtimestamp(timestamp)
    diff = now - then
    
    if diff.days > 365:
        years = diff.days // 365
        return f"{years} year{'s' if years > 1 else ''} ago"
    elif diff.days > 30:
        months = diff.days // 30
        return f"{months} month{'s' if months > 1 else ''} ago"
    elif diff.days > 0:
        return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    else:
        return "just now"


# ═══════════════════════════════════════════════════════════════
# FILE UTILITIES
# ═══════════════════════════════════════════════════════════════

def format_size(size_bytes: int) -> str:
    """Format bytes to human readable size"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def safe_filename(text: str) -> str:
    """Convert text to safe filename"""
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-').lower()[:50]


# ═══════════════════════════════════════════════════════════════
# ERROR HANDLING
# ═══════════════════════════════════════════════════════════════

class GeoError(Exception):
    """Base exception for Geo bot"""
    pass


class PermissionError(GeoError):
    """Permission denied exception"""
    pass


class ValidationError(GeoError):
    """Validation error exception"""
    pass


class NotFoundError(GeoError):
    """Not found exception"""
    pass


async def retry_async(func, max_retries: int = 3, delay: float = 1.0, 
                     backoff: float = 2.0):
    """Retry async function with exponential backoff"""
    last_exception = None
    current_delay = delay
    
    for attempt in range(max_retries):
        try:
            return await func()
        except Exception as e:
            last_exception = e
            logger.warning(f"Attempt {attempt + 1}/{max_retries} failed: {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(current_delay)
                current_delay *= backoff
    
    raise last_exception


def log_execution(func):
    """Log function execution"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        func_name = func.__name__
        logger.debug(f"Executing {func_name}")
        try:
            result = await func(*args, **kwargs)
            logger.debug(f"{func_name} completed successfully")
            return result
        except Exception as e:
            logger.error(f"{func_name} failed: {e}")
            raise
    
    return wrapper


# ═══════════════════════════════════════════════════════════════
# PAGINATION UTILITIES
# ═══════════════════════════════════════════════════════════════

def paginate(items: List[Any], page: int, per_page: int = 10) -> Dict[str, Any]:
    """Paginate list of items"""
    total = len(items)
    total_pages = (total + per_page - 1) // per_page
    
    start = (page - 1) * per_page
    end = start + per_page
    
    return {
        'items': items[start:end],
        'page': page,
        'per_page': per_page,
        'total': total,
        'total_pages': total_pages,
        'has_next': page < total_pages,
        'has_prev': page > 1
    }


# ═══════════════════════════════════════════════════════════════
# FORMATTING UTILITIES
# ═══════════════════════════════════════════════════════════════

def format_list(items: List[str], separator: str = ", ", 
               last_separator: str = " and ") -> str:
    """Format list with proper grammar"""
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]}{last_separator}{items[1]}"
    return separator.join(items[:-1]) + f"{last_separator}{items[-1]}"


def format_number(num: int) -> str:
    """Format large numbers with K, M, B suffixes"""
    if num < 1000:
        return str(num)
    elif num < 1000000:
        return f"{num / 1000:.1f}K"
    elif num < 1000000000:
        return f"{num / 1000000:.1f}M"
    else:
        return f"{num / 1000000000:.1f}B"


def format_boolean(value: bool, true_text: str = "Yes", 
                  false_text: str = "No") -> str:
    """Format boolean as text"""
    return true_text if value else false_text