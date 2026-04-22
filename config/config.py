# ═══════════════════════════════════════════════════════════════
# Geo Protection Bot - Configuration Manager
# ═══════════════════════════════════════════════════════════════

import os
from pathlib import Path
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from dataclasses import dataclass, field

# Load environment variables
load_dotenv()


@dataclass
class BotConfig:
    """Bot configuration settings"""
    name: str = os.getenv("BOT_NAME", "Geo")
    username: str = os.getenv("BOT_USERNAME", "F_FFBot")
    token: Optional[str] = os.getenv("BOT_TOKEN")
    developer_id: int = int(os.getenv("DEVELOPER_ID", 0))
    god_mode: bool = os.getenv("GOD_MODE", "true").lower() == "true"
    god_status: str = os.getenv("GOD_STATUS", "Mythic")


@dataclass
class TelegramConfig:
    """Telegram API configuration"""
    api_id: int = int(os.getenv("API_ID", 0))
    api_hash: str = os.getenv("API_HASH", "")
    session_name: str = os.getenv("BOT_USERNAME", "Geo")
    device_model: str = "Geo Protection Bot"
    app_version: str = "1.0.0"
    lang_code: str = "en"


@dataclass
class DatabaseConfig:
    """Database configuration"""
    url: str = os.getenv("DATABASE_URL", "sqlite:///geo.db")
    auto_clean: bool = os.getenv("DB_AUTO_CLEAN", "true").lower() == "true"
    backup_interval: int = int(os.getenv("DB_BACKUP_INTERVAL", 3600))
    backup_dir: Path = field(default_factory=lambda: Path("backups"))
    
    def __post_init__(self):
        self.backup_dir.mkdir(exist_ok=True)


@dataclass
class RedisConfig:
    """Redis cache configuration"""
    url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    password: Optional[str] = os.getenv("REDIS_PASSWORD")
    ssl: bool = os.getenv("REDIS_SSL", "false").lower() == "true"
    decode_responses: bool = True
    max_connections: int = 50
    socket_timeout: int = 5
    socket_connect_timeout: int = 5


@dataclass
class PerformanceConfig:
    """Performance settings"""
    workers: int = int(os.getenv("WORKERS", 8))
    max_load: int = int(os.getenv("MAX_LOAD", 10000))
    connection_pool_size: int = int(os.getenv("CONNECTION_POOL_SIZE", 100))
    request_timeout: int = int(os.getenv("REQUEST_TIMEOUT", 30))
    max_retries: int = int(os.getenv("MAX_RETRIES", 3))
    use_uvloop: bool = True


@dataclass
class SecurityConfig:
    """Security settings"""
    secret_key: str = os.getenv("SECRET_KEY", "change-me-in-production")
    enable_antispam: bool = os.getenv("ENABLE_ANTISPAM", "true").lower() == "true"
    enable_flood_protection: bool = os.getenv("ENABLE_FLOOD_PROTECTION", "true").lower() == "true"
    max_message_length: int = int(os.getenv("MAX_MESSAGE_LENGTH", 4096))
    rate_limit: int = int(os.getenv("RATE_LIMIT", 30))


@dataclass
class FeatureConfig:
    """Feature flags"""
    enable_welcome: bool = os.getenv("ENABLE_WELCOME", "true").lower() == "true"
    enable_goodbye: bool = os.getenv("ENABLE_GOODBYE", "true").lower() == "true"
    enable_warnings: bool = os.getenv("ENABLE_WARNINGS", "true").lower() == "true"
    enable_locks: bool = os.getenv("ENABLE_LOCKS", "true").lower() == "true"
    enable_filters: bool = os.getenv("ENABLE_FILTERS", "true").lower() == "true"
    enable_reports: bool = os.getenv("ENABLE_REPORTS", "true").lower() == "true"
    enable_staff: bool = os.getenv("ENABLE_STAFF", "true").lower() == "true"
    enable_global_bans: bool = os.getenv("ENABLE_GLOBAL_BANS", "true").lower() == "true"
    enable_approvals: bool = os.getenv("ENABLE_APPROVALS", "true").lower() == "true"


@dataclass
class DefaultsConfig:
    """Default settings for groups"""
    default_warns: int = int(os.getenv("DEFAULT_WARNS", 3))
    default_antispam_time: int = int(os.getenv("DEFAULT_ANTISPAM_TIME", 100))
    default_flood_time: int = int(os.getenv("DEFAULT_FLOOD_TIME", 5))
    default_mute_time: int = int(os.getenv("DEFAULT_MUTE_TIME", 60))
    default_raid_protection_time: int = int(os.getenv("DEFAULT_RAID_PROTECTION_TIME", 300))


@dataclass
class LanguageConfig:
    """Language settings"""
    default_language: str = os.getenv("DEFAULT_LANGUAGE", "en")
    supported_languages: list = field(default_factory=lambda: os.getenv("SUPPORTED_LANGUAGES", "en,es,ar,ru,tr,de,pt,id,hi,zh").split(","))


@dataclass
class LoggingConfig:
    """Logging configuration"""
    level: str = os.getenv("LOG_LEVEL", "INFO")
    file: str = os.getenv("LOG_FILE", "geo.log")
    max_size: int = int(os.getenv("LOG_MAX_SIZE", 10485760))
    backup_count: int = int(os.getenv("LOG_BACKUP_COUNT", 5))
    enable_debug: bool = os.getenv("ENABLE_DEBUG", "false").lower() == "true"


@dataclass
class Config:
    """Main configuration container"""
    bot: BotConfig = field(default_factory=BotConfig)
    telegram: TelegramConfig = field(default_factory=TelegramConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    redis: RedisConfig = field(default_factory=RedisConfig)
    performance: PerformanceConfig = field(default_factory=PerformanceConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    features: FeatureConfig = field(default_factory=FeatureConfig)
    defaults: DefaultsConfig = field(default_factory=DefaultsConfig)
    language: LanguageConfig = field(default_factory=LanguageConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    
    def validate(self) -> bool:
        """Validate configuration"""
        errors = []
        
        if not self.telegram.api_id:
            errors.append("API_ID is required")
        if not self.telegram.api_hash:
            errors.append("API_HASH is required")
        if not self.bot.token:
            errors.append("BOT_TOKEN is required")
        if not self.bot.developer_id:
            errors.append("DEVELOPER_ID is required")
            
        if errors:
            raise ValueError("Configuration errors:\n" + "\n".join(errors))
            
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary"""
        return {
            "bot": self.bot.__dict__,
            "telegram": self.telegram.__dict__,
            "database": self.database.__dict__,
            "redis": self.redis.__dict__,
            "performance": self.performance.__dict__,
            "security": self.security.__dict__,
            "features": self.features.__dict__,
            "defaults": self.defaults.__dict__,
            "language": self.language.__dict__,
            "logging": self.logging.__dict__,
        }


# Global configuration instance
config = Config()


def reload_config():
    """Reload configuration from environment"""
    global config
    load_dotenv(override=True)
    config = Config()
    return config