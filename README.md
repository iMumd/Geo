# Geo Protection Bot 🤖

```
╔══════════════════════════════════════════════════════════════╗
║   █████╗     ██████╗  ██████╗ ██████╗ ██╗   ██╗███████╗    ║
║  ██╔══██╗    ██╔══██╗██╔═══██╗██╔══██╗╚██╗ ██╔╝██╔════╝    ║
║  ███████║    ██████╔╝██║   ██║██████╔╝ ╚████╔╝ ███████╗    ║
║  ██╔══██║    ██╔══██╗██║   ██║██╔══██╗  ╚██╔╝  ╚════██║    ║
║  ██║  ██║    ██║  ██║╚██████╔╝██████╔╝   ██║   ███████║    ║
║  ╚═╝  ╚═╝    ╚═╝  ╚═╝ ╚═════╝ ╚═════╝    ╚═╝   ╚══════╝    ║
║                                                              ║
║    ████████╗ ██████╗ ███╗   ██╗ ██████╗                      ║
║    ╚══██╔══╝██╔═══██╗████╗  ██║██╔═══██╗                     ║
║       ██║   ██║   ██║██╔██╗ ██║██║   ██║                     ║
║       ██║   ██║   ██║██║╚██╗██║██║   ██║                     ║
║       ██║   ╚██████╔╝██║ ╚████║╚██████╔╝                     ║
║       ╚═╝    ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝                      ║
╚══════════════════════════════════════════════════════════════╝
```

## ⚡ Features

### 🛡️ Protection & Security
- **Anti-Spam System** - Automatic detection and removal of spam
- **Anti-Bot** - Prevents bots from joining
- **Anti-Flood** - Stops message flooding attacks
- **Anti-Scam** - Detects and blocks scams
- **Anti-Porn** - Filters inappropriate content
- **Anti-Raid** - Protects against raid attacks
- **Welcome & Farewell** - Customizable messages
- **Mute System** - Temporary and permanent muting
- **Ban/Kick System** - Full moderation tools
- **Warn System** - Progressive warning with auto-actions
- **Lock System** - Lock various chat features
- **Filter System** - Block specific words/patterns

### 👑 Admin Tools
- **Pin/Unpin Messages** - With notifications
- **Group Settings** - Full configuration control
- **User Management** - View user history and stats
- **Chat Reports** - Advanced reporting system
- **Clean Mode** - Auto-clean service messages
- **Approve/Report** - User verification system

### 🌐 Multi-Language Support
- English (en)
- Spanish (es)
- Arabic (ar)
- Russian (ru)
- Turkish (tr)
- German (de)
- Portuguese (pt)
- Indonesian (id)
- Hindi (hi)
- Chinese (zh)

### 💪 Technical Features
- **High Performance** - Multi-threaded architecture
- **SQLite Database** - Powerful persistent storage
- **Redis Cache** - Lightning-fast caching
- **Load Balancing** - Handles millions of users
- **Secure Code** - Protection against exploits
- **Hot Reload** - Update without restart
- **Backup System** - Automatic database backups
- **Logging** - Comprehensive activity logs

### 🎮 God Mode (Developer)
- **Mythic Status** - Special developer access
- **System Commands** - Bot management tools
- **Broadcast** - Send to all chats
- **Group Management** - Remote control
- **Stats Dashboard** - Real-time monitoring

## 🚀 Quick Start

### Prerequisites
```
Python 3.9+
Redis (optional but recommended)
SQLite3
```

### Installation

```bash
# Clone the repository
git clone https://github.com/iMumd/Geo.git
cd Geo

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env

# Run the bot
python main.py
```

## ⚙️ Configuration

Create your `.env` file with:

```env
# Bot Settings
BOT_NAME=Geo
BOT_USERNAME=F_FFBot
BOT_TOKEN=your_bot_token_here

# Developer Settings
DEVELOPER_ID=your_user_id
GOD_MODE=true

# Database
DATABASE_URL=sqlite:///geo.db
REDIS_URL=redis://localhost:6379

# Security
API_ID=your_api_id
API_HASH=your_api_hash

# Performance
WORKERS=8
MAX_LOAD=10000
```

## 📁 Project Structure

```
Geo/
├── 📄 main.py              # Entry point
├── 📄 bot.py               # Core bot logic
├── 📂 config/              # Configuration
│   └── 📄 config.py        # Settings manager
├── 📂 database/            # Database layer
│   ├── 📄 database.py      # SQLite operations
│   └── 📄 cache.py         # Redis cache
├── 📂 handlers/            # Command handlers
│   ├── 📄 admin.py         # Admin commands
│   ├── 📄 protection.py    # Protection tools
│   ├── 📄 moderation.py    # Moderation tools
│   └── 📄 user.py          # User commands
├── 📂 i18n/                # Translations
│   ├── 📄 translations.py  # Translation engine
│   └── 📂 locales/         # Language files
├── 📂 utils/               # Utilities
│   ├── 📄 helpers.py       # Helper functions
│   └── 📄 decorators.py    # Custom decorators
├── 📂 plugins/             # Plugin system
│   └── 📄 plugins.py       # Plugin loader
├── 📂 .env                 # Environment variables
└── 📄 README.md            # This file
```

## 📖 Command Reference

### 🔒 Protection Commands
| Command | Description |
|---------|-------------|
| `/antispam` | Toggle anti-spam protection |
| `/antibot` | Block bot joins |
| `/antiflood` | Anti-flood settings |
| `/antiraid` | Raid protection mode |
| `/setwarnlimit` | Set warning limit |
| `/setantispamtime` | Anti-spam time window |
| `/allowlinks` | Allow/deny links |
| `/allowbots` | Allow bot usage |
| `/antiscam` | Scam link protection |
| `/antiporn` | NSFW content filter |

### 👑 Admin Commands
| Command | Description |
|---------|-------------|
| `/pin` | Pin message |
| `/unpin` | Unpin message |
| `/purge` | Delete messages |
| `/ban` | Ban user |
| `/unban` | Unban user |
| `/kick` | Kick user |
| `/mute` | Mute user |
| `/unmute` | Unmute user |
| `/tmute` | Temporary mute |
| `/warn` | Warn user |
| `/dwarn` | Delete warning |
| `/warns` | View warnings |
| `/setwelcome` | Set welcome message |
| `/setgoodbye` | Set goodbye message |
| `/cleanblk` | Clean blocked words |
| `/addblk` | Add blocked word |
| `/rmblk` | Remove blocked word |
| `/lock` | Lock chat feature |
| `/unlock` | Unlock chat feature |
| `/locktypes` | View lock types |
| `/reports` | Toggle reports |
| `/settings` | Group settings |
| `/staff` | Staff management |
| `/addstaff` | Add staff member |
| `/rmstaff` | Remove staff member |
| `/setgban` | Global ban user |
| `/rmgban` | Remove global ban |
| `/gbanlist` | View global bans |
| `/approve` | Approve user |
| `/disapprove` | Remove approval |

### 🌐 Language Commands
| Command | Description |
|---------|-------------|
| `/setlang` | Change language |
| `/languages` | View available languages |

### 🎮 God Mode Commands (Mythic)
| Command | Description |
|---------|-------------|
| `/status` | Bot status |
| `/stats` | Statistics |
| `/broadcast` | Broadcast message |
| `/groups` | List all groups |
| `/leave` | Leave group |
| `/restart` | Restart bot |
| `/shutdown` | Shutdown bot |
| `/eval` | Execute code |
| `/exec` | Execute command |
| `/logs` | View logs |
| `/backup` | Backup database |
| `/update` | Update bot |

## 🔧 Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `BOT_NAME` | Yes | Geo | Bot display name |
| `BOT_USERNAME` | Yes | F_FFBot | Bot username |
| `BOT_TOKEN` | Yes | - | Telegram bot token |
| `DEVELOPER_ID` | Yes | - | Developer user ID |
| `GOD_MODE` | No | true | Enable god mode |
| `DATABASE_URL` | No | sqlite | Database connection |
| `REDIS_URL` | No | localhost | Redis connection |
| `API_ID` | Yes | - | Telegram API ID |
| `API_HASH` | Yes | - | Telegram API Hash |
| `WORKERS` | No | 8 | Worker threads |
| `MAX_LOAD` | No | 10000 | Max load per worker |
| `LOG_LEVEL` | No | INFO | Logging level |

## 🌐 Supported Languages

- 🇺🇸 English (en)
- 🇪🇸 Spanish (es)
- 🇸🇦 Arabic (ar)
- 🇷🇺 Russian (ru)
- 🇹🇷 Turkish (tr)
- 🇩🇪 German (de)
- 🇧🇷 Portuguese (pt)
- 🇮🇩 Indonesian (id)
- 🇮🇳 Hindi (hi)
- 🇨🇳 Chinese (zh)

## 📊 Permissions Required

The bot needs **Admin with Full Permissions** in groups to function properly:

```
✅ Delete messages
✅ Restrict members
✅ Manage chat
✅ Pin messages
✅ Change chat info
```

## 🐛 Troubleshooting

### Bot not responding?
1. Check bot token in `.env`
2. Verify API credentials
3. Check database connection
4. Review logs

### Commands not working?
1. Make bot admin with full permissions
2. Check group settings
3. Verify user permissions

### Database errors?
1. Check database file permissions
2. Ensure sufficient disk space
3. Verify database integrity

## 📧 Contact

**Developer**: @user9JKsuG
**Status**: Mythic (Developer)

---

**Version**: 1.0.0 Private Edition  
**License**: Private - Not for public distribution  
**Repository**: https://github.com/iMumd/Geo (Private)

---

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   💪 Geo Protection Bot - Built with ❤️ for safer groups 💪   ║
║                                                              ║
║   ⚡ Multi-threaded • Secure • Powerful • Fast ⚡             ║
║                                                              ║
║   🌟 Mythic Developer: @user9JKsuG 🌟                        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```