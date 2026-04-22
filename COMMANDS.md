# ═══════════════════════════════════════════════════════════════
# Geo Protection Bot - Command Reference
# (Similar to MissRose.org/docs/)
# ═══════════════════════════════════════════════════════════════

## PRODUCTION COMMANDS
```
/antispam - Enable/disable anti-spam protection
/antiflood - Enable/disable anti-flood protection
/antibot - Enable/disable anti-bot protection
/antiraid - Enable/disable anti-raid protection
/antiscam - Enable/disable anti-scam protection
/antiporn - Enable/disable NSFW filter
/setantispamtime <seconds> - Set anti-spam time window
/setfloodtime <seconds> - Set flood check time
```

## ADMIN COMMANDS
```
/ban <user> [reason] - Ban user from chat
/unban <user> - Unban user from chat
/kick <user> - Kick user from chat
/mute <user> - Mute user
/unmute <user> - Unmute user
/tmute <user> <duration> - Temporarily mute user (e.g., 5m, 1h, 1d)
/warn <user> [reason] - Warn user
/dwarn <user> - Delete user's warning
/warns <user> - View user warnings
/resetwarns <user> - Reset all warnings for user
/pin - Pin replied message
/unpin - Unpin message or all messages
/purge - Purge messages from replied message
/setwarnlimit <number> - Set warning limit (1-10)
/setwelcome <message> - Set welcome message
/setgoodbye <message> - Set goodbye message
```

## LOCK COMMANDS
```
/lock <type> - Lock a feature
/unlock <type> - Unlock a feature
/locktypes - Show available lock types
```

### Lock Types:
- links - Lock all links
- spam - Lock spam content
- forward - Lock forwarded messages
- audio - Lock audio files
- video - Lock video files
- photo - Lock photos
- document - Lock documents
- sticker - Lock stickers
- location - Lock locations
- contact - Lock contacts
- game - Lock games
- inline - Lock inline queries

## FILTER COMMANDS
```
/addblk <word> - Add word to filters
/rmblk <word> - Remove word from filters
/cleanblk - Clear all filtered words
/blklist - View filtered words
```

## STAFF COMMANDS
```
/staff - View staff list
/addstaff <user> [rank] - Add staff member
/rmstaff <user> - Remove staff member
```

## GLOBAL BAN COMMANDS
```
/gban <user> [reason] - Globally ban user
/ungban <user> - Remove global ban
/gbanlist - View global ban list
```

## APPROVAL COMMANDS
```
/approve <user> - Approve user
/disapprove <user> - Remove user approval
/approved - View approved users
```

## REPORT COMMANDS
```
/report <reason> - Report to admins
/reports - Toggle reports feature
```

## SETTINGS
```
/settings - Open settings keyboard
```

## GENERAL COMMANDS
```
/start - Start the bot
/help - Show help message
/setlang <code> - Change language
/languages - Show available languages
/stats - Show bot statistics
/info [user] - Show user info
/id - Show IDs
/ping - Check bot latency
/about - Show bot info
/rules - Show chat rules
/version - Show bot version
```

## GOD MODE COMMANDS (Developer Only - Mythic Status)
```
/god - Open God Mode dashboard
/status - Show bot status
/stats - Show comprehensive statistics
/broadcast <message> - Broadcast to all chats
/groups - List all groups
/chatlist - Export chat list
/leave <chat_id> - Leave a chat
/restart - Restart bot
/shutdown - Shutdown bot
/backup - Backup database
/eval <code> - Execute Python code
/exec <command> - Execute shell command
/logs [lines] - View logs
/gc - Run garbage collection
/userinfo <user_id> - Get user info
/banall <user_id> [reason] - Global ban
/unbanall <user_id> - Remove global ban
/refresh - Refresh bot data
/clearcache - Clear Redis cache
/memory - Show memory usage
/sysinfo - Show system info
/update - Update bot from git
```