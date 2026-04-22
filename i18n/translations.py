# ═══════════════════════════════════════════════════════════════
# Geo Protection Bot - Translation Engine
# ═══════════════════════════════════════════════════════════════

from typing import Dict, Optional
from pathlib import Path
import json
import logging

logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════
# TRANSLATIONS DICTIONARY
# ═══════════════════════════════════════════════════════════════

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "en": {
        # General
        "bot_name": "Geo",
        "welcome": "Welcome {user}!",
        "goodbye": "{user} has left the chat",
        "success": "✅ Success",
        "error": "❌ Error",
        "warning": "⚠️ Warning",
        "info": "ℹ️ Info",
        
        # Protection
        "antispam_enabled": "Anti-Spam protection enabled",
        "antispam_disabled": "Anti-Spam protection disabled",
        "antibot_enabled": "Anti-Bot protection enabled",
        "antibot_disabled": "Anti-Bot protection disabled",
        "antiflood_enabled": "Anti-Flood protection enabled",
        "antiflood_disabled": "Anti-Flood protection disabled",
        "antiraid_enabled": "Anti-Raid protection enabled",
        "antiraid_disabled": "Anti-Raid protection disabled",
        "antiscam_enabled": "Anti-Scam protection enabled",
        "antiscam_disabled": "Anti-Scam protection disabled",
        "antiporn_enabled": "Anti-Porn filter enabled",
        "antiporn_disabled": "Anti-Porn filter disabled",
        
        # Actions
        "user_banned": "User {user} has been banned",
        "user_unbanned": "User {user} has been unbanned",
        "user_kicked": "User {user} has been kicked",
        "user_muted": "User {user} has been muted",
        "user_unmuted": "User {user} has been unmuted",
        "user_warned": "User {user} has been warned ({count}/{limit})",
        "user_unwarned": "Warning removed for {user}",
        "user_pinned": "Message pinned",
        "user_unpinned": "Message unpinned",
        
        # Settings
        "settings_saved": "Settings saved successfully",
        "settings_reset": "Settings reset to defaults",
        "warn_limit_set": "Warning limit set to {limit}",
        "welcome_set": "Welcome message set",
        "goodbye_set": "Goodbye message set",
        "language_set": "Language set to {lang}",
        
        # Locks
        "locked": "🔒 {item} locked",
        "unlocked": "🔓 {item} unlocked",
        "lock_links": "Links",
        "lock_spam": "Spam",
        "lock_forward": "Forwards",
        "lock_audio": "Audio",
        "lock_video": "Videos",
        "lock_photo": "Photos",
        "lock_document": "Documents",
        "lock_sticker": "Stickers",
        "lock_location": "Locations",
        "lock_contact": "Contacts",
        "lock_game": "Games",
        "lock_inline": "Inline queries",
        
        # Staff
        "staff_added": "User added to staff",
        "staff_removed": "User removed from staff",
        "not_staff": "User is not staff",
        
        # Global Bans
        "gban_added": "User globally banned",
        "gban_removed": "User globally unbanned",
        "gban_list": "Global Ban List",
        
        # Approvals
        "approved": "User approved",
        "disapproved": "User disapproval removed",
        
        # Errors
        "no_permission": "You don't have permission to use this command",
        "user_not_found": "User not found",
        "chat_only": "This command can only be used in groups",
        "admin_only": "This command can only be used by admins",
        "owner_only": "This command can only be used by the chat owner",
        
        # Filters
        "word_added": "Word added to filters",
        "word_removed": "Word removed from filters",
        "filter_list": "Filter List",
        
        # Reports
        "report_sent": "Report sent to admins",
        "reports_enabled": "Reports enabled",
        "reports_disabled": "Reports disabled",
        
        # Help
        "help_header": "Available Commands:",
        "help_admin": "Admin Commands",
        "help_protection": "Protection Commands",
        "help_user": "User Commands",
        
        # Stats
        "stats_header": "📊 Bot Statistics",
        "total_users": "Total Users",
        "total_chats": "Total Chats",
        "total_warnings": "Total Warnings",
        "total_gbans": "Global Bans",
        
        # God Mode
        "god_welcome": "👑 Welcome, {status} Developer! 👑",
        "god_status": "God Mode Status: {status}",
        "god_commands": "God Mode Commands",
        "broadcast_sent": "Broadcast sent to {count} chats",
        "restarting": "Bot is restarting...",
        "shutting_down": "Bot is shutting down...",
    },
    
    "es": {
        "bot_name": "Geo",
        "welcome": "¡Bienvenido {user}!",
        "goodbye": "{user} ha dejado el chat",
        "success": "✅ Éxito",
        "error": "❌ Error",
        "warning": "⚠️ Advertencia",
        "info": "ℹ️ Info",
        
        "antispam_enabled": "Protección anti-spam activada",
        "antispam_disabled": "Protección anti-spam desactivada",
        "antibot_enabled": "Protección anti-bot activada",
        "antibot_disabled": "Protección anti-bot desactivada",
        "antiflood_enabled": "Protección anti-inundación activada",
        "antiflood_disabled": "Protección anti-inundación desactivada",
        "antiraid_enabled": "Protección anti-raid activada",
        "antiraid_disabled": "Protección anti-raid desactivada",
        "antiscam_enabled": "Protección anti-estafa activada",
        "antiscam_disabled": "Protección anti-estafa desactivada",
        "antiporn_enabled": "Filtro anti-pornografía activado",
        "antiporn_disabled": "Filtro anti-pornografía desactivado",
        
        "user_banned": "Usuario {user} ha sido baneado",
        "user_unbanned": "Usuario {user} ha sido desbaneado",
        "user_kicked": "Usuario {user} ha sido expulsado",
        "user_muted": "Usuario {user} ha sido silenciado",
        "user_unmuted": "Usuario {user} ha sido désilenciado",
        "user_warned": "Usuario {user} ha sido advertida ({count}/{limit})",
        "user_unwarned": "Advertencia eliminada para {user}",
        "user_pinned": "Mensaje anclado",
        "user_unpinned": "Mensaje desanclado",
        
        "settings_saved": "Configuración guardada",
        "settings_reset": "Configuración restaurada",
        "warn_limit_set": "Límite de advertencias establecido en {limit}",
        "welcome_set": "Mensaje de bienvenida establecido",
        "goodbye_set": "Mensaje de despedida establecido",
        "language_set": "Idioma establecido en {lang}",
        
        "locked": "🔒 {item} bloqueado",
        "unlocked": "🔓 {item} desbloqueado",
        "lock_links": "Enlaces",
        "lock_spam": "Spam",
        "lock_forward": "Reenvíos",
        "lock_audio": "Audio",
        "lock_video": "Videos",
        "lock_photo": "Fotos",
        "lock_document": "Documentos",
        "lock_sticker": "Stickers",
        "lock_location": "Ubicaciones",
        "lock_contact": "Contactos",
        "lock_game": "Juegos",
        "lock_inline": "Consultas en línea",
        
        "staff_added": "Usuario añadido al staff",
        "staff_removed": "Usuario eliminado del staff",
        "not_staff": "El usuario no es staff",
        
        "gban_added": "Usuario baneado globalmente",
        "gban_removed": "Usuario desbaneado globalmente",
        "gban_list": "Lista de Bans Globales",
        
        "approved": "Usuario aprobado",
        "disapproved": "Desaprobación de usuario eliminada",
        
        "no_permission": "No tienes permiso para usar este comando",
        "user_not_found": "Usuario no encontrado",
        "chat_only": "Este comando solo puede usarse en grupos",
        "admin_only": "Este comando solo puede ser usado por administradores",
        "owner_only": "Este comando solo puede ser usado por el propietario del chat",
        
        "word_added": "Palabra añadida a filtros",
        "word_removed": "Palabra eliminada de filtros",
        "filter_list": "Lista de Filtros",
        
        "report_sent": "Reporte enviado a administradores",
        "reports_enabled": "Reportes habilitados",
        "reports_disabled": "Reportes deshabilitados",
        
        "help_header": "Comandos Disponibles:",
        "help_admin": "Comandos de Administrador",
        "help_protection": "Comandos de Protección",
        "help_user": "Comandos de Usuario",
        
        "stats_header": "📊 Estadísticas del Bot",
        "total_users": "Total de Usuarios",
        "total_chats": "Total de Chats",
        "total_warnings": "Total de Advertencias",
        "total_gbans": "Bans Globales",
        
        "god_welcome": "👑 ¡Bienvenido, Desarrollador {status}! 👑",
        "god_status": "Estado del Modo Dios: {status}",
        "god_commands": "Comandos del Modo Dios",
        "broadcast_sent": "Mensaje enviado a {count} chats",
        "restarting": "El bot se está reiniciando...",
        "shutting_down": "El bot se está apagando...",
    },
    
    "ar": {
        "bot_name": "Geo",
        "welcome": "مرحباً {user}!",
        "goodbye": "{user} غادر المحادثة",
        "success": "✅ نجاح",
        "error": "❌ خطأ",
        "warning": "⚠️ تحذير",
        "info": "ℹ️ معلومات",
        
        "antispam_enabled": "حماية مكافحة الرسائل المزعجة مفعلة",
        "antispam_disabled": "حماية مكافحة الرسائل المزعجة معطلة",
        "antibot_enabled": "حماية مكافحة البوتات مفعلة",
        "antibot_disabled": "حماية مكافحة البوتات معطلة",
        "antiflood_enabled": "حماية مكافحة الفيضان مفعلة",
        "antiflood_disabled": "حماية مكافحة الفيضان معطلة",
        "antiraid_enabled": "حماية مكافحة الهجمات مفعلة",
        "antiraid_disabled": "حماية مكافحة الهجمات معطلة",
        "antiscam_enabled": "حماية مكافحة الاحتيال مفعلة",
        "antiscam_disabled": "حماية مكافحة الاحتيال معطلة",
        "antiporn_enabled": "مرشح مكافحة المواد الإباحية مفعل",
        "antiporn_disabled": "مرشح مكافحة المواد الإباحية معطل",
        
        "user_banned": "تم حظر المستخدم {user}",
        "user_unbanned": "تم إلغاء حظر المستخدم {user}",
        "user_kicked": "تم طرد المستخدم {user}",
        "user_muted": "تم كتم المستخدم {user}",
        "user_unmuted": "تم إلغاء كتم المستخدم {user}",
        "user_warned": "تم تحذير المستخدم {user} ({count}/{limit})",
        "user_unwarned": "تم إزالة التحذير لـ {user}",
        "user_pinned": "تم تثبيت الرسالة",
        "user_unpinned": "تم إلغاء تثبيت الرسالة",
        
        "settings_saved": "تم حفظ الإعدادات",
        "settings_reset": "تم إعادة تعيين الإعدادات",
        "warn_limit_set": "تم تعيين حد التحذيرات إلى {limit}",
        "welcome_set": "تم تعيين رسالة الترحيب",
        "goodbye_set": "تم تعيين رسالة الوداع",
        "language_set": "تم تعيين اللغة إلى {lang}",
        
        "locked": "🔒 {item} مقفل",
        "unlocked": "🔓 {item} غير مقفل",
        "lock_links": "الروابط",
        "lock_spam": "الرسائل المزعجة",
        "lock_forward": "إعادة التوجيه",
        "lock_audio": "الصوت",
        "lock_video": "الفيديو",
        "lock_photo": "الصور",
        "lock_document": "المستندات",
        "lock_sticker": "الملصقات",
        "lock_location": "الموقع",
        "lock_contact": "جهات الاتصال",
        "lock_game": "الألعاب",
        "lock_inline": "الاستعلامات المضمنة",
        
        "staff_added": "تمت إضافة المستخدم إلى الموظفين",
        "staff_removed": "تمت إزالة المستخدم من الموظفين",
        "not_staff": "المستخدم ليس من الموظفين",
        
        "gban_added": "تم حظر المستخدم عالمياً",
        "gban_removed": "تم إلغاء حظر المستخدم عالمياً",
        "gban_list": "قائمة الحظر العالمي",
        
        "approved": "تمت الموافقة على المستخدم",
        "disapproved": "تمت إزالة عدم الموافقة على المستخدم",
        
        "no_permission": "ليس لديك إذن لاستخدام هذا الأمر",
        "user_not_found": "المستخدم غير موجود",
        "chat_only": "لا يمكن استخدام هذا الأمر إلا في المجموعات",
        "admin_only": "لا يمكن استخدام هذا الأمر إلا من قبل المشرفين",
        "owner_only": "لا يمكن استخدام هذا الأمر إلا من قبل مالك المحادثة",
        
        "word_added": "تمت إضافة الكلمة إلى الفلاتر",
        "word_removed": "تمت إزالة الكلمة من الفلاتر",
        "filter_list": "قائمة الفلاتر",
        
        "report_sent": "تم إرسال التقرير إلى المشرفين",
        "reports_enabled": "التقارير مفعلة",
        "reports_disabled": "التقارير معطلة",
        
        "help_header": "الأوامر المتاحة:",
        "help_admin": "أوامر المشرفين",
        "help_protection": "أوامر الحماية",
        "help_user": "أوامر المستخدمين",
        
        "stats_header": "📊 إحصائيات البوت",
        "total_users": "إجمالي المستخدمين",
        "total_chats": "إجمالي المحادثات",
        "total_warnings": "إجمالي التحذيرات",
        "total_gbans": "الحظر العالمي",
        
        "god_welcome": "👑 مرحباً، مطور {status}! 👑",
        "god_status": "حالة وضع الله: {status}",
        "god_commands": "أوامر وضع الله",
        "broadcast_sent": "تم إرسال الرسالة إلى {count} محادثة",
        "restarting": "البوت قيد إعادة التشغيل...",
        "shutting_down": "البوت قيد الإغلاق...",
    },
    
    "ru": {
        "bot_name": "Geo",
        "welcome": "Добро пожаловать {user}!",
        "goodbye": "{user} покинул(а) чат",
        "success": "✅ Успех",
        "error": "❌ Ошибка",
        "warning": "⚠️ Предупреждение",
        "info": "ℹ️ Информация",
        
        "antispam_enabled": "Защита от спама включена",
        "antispam_disabled": "Защита от спама отключена",
        "antibot_enabled": "Защита от ботов включена",
        "antibot_disabled": "Защита от ботов отключена",
        "antiflood_enabled": "Защита от флуда включена",
        "antiflood_disabled": "Защита от флуда отключена",
        "antiraid_enabled": "Защита от рейдов включена",
        "antiraid_disabled": "Защита от рейдов отключена",
        "antiscam_enabled": "Защита от мошенничества включена",
        "antiscam_disabled": "Защита от мошенничества отключена",
        "antiporn_enabled": "Фильтр NSFW включён",
        "antiporn_disabled": "Фильтр NSFW отключён",
        
        "user_banned": "Пользователь {user} заблокирован",
        "user_unbanned": "Пользователь {user} разблокирован",
        "user_kicked": "Пользователь {user} исключён",
        "user_muted": "Пользователь {user} заглушён",
        "user_unmuted": "Пользователь {user} разговорён",
        "user_warned": "Пользователь {user} предупреждён ({count}/{limit})",
        "user_unwarned": "Предупреждение снято для {user}",
        "user_pinned": "Сообщение закреплено",
        "user_unpinned": "Сообщение откреплено",
        
        "settings_saved": "Настройки сохранены",
        "settings_reset": "Настройки сброшены",
        "warn_limit_set": "Лимит предупреждений установлен на {limit}",
        "welcome_set": "Приветственное сообщение установлено",
        "goodbye_set": "Прощальное сообщение установлено",
        "language_set": "Язык установлен на {lang}",
        
        "locked": "🔒 {item} заблокировано",
        "unlocked": "🔓 {item} разблокировано",
        "lock_links": "Ссылки",
        "lock_spam": "Спам",
        "lock_forward": "Пересылка",
        "lock_audio": "Аудио",
        "lock_video": "Видео",
        "lock_photo": "Фото",
        "lock_document": "Документы",
        "lock_sticker": "Стикеры",
        "lock_location": "Местоположение",
        "lock_contact": "Контакты",
        "lock_game": "Игры",
        "lock_inline": "Inline запросы",
        
        "staff_added": "Пользователь добавлен в персонал",
        "staff_removed": "Пользователь удалён из персонала",
        "not_staff": "Пользователь не в персонале",
        
        "gban_added": "Пользователь глобально забанен",
        "gban_removed": "Пользователь глобально разбанен",
        "gban_list": "Список глобальных банов",
        
        "approved": "Пользователь одобрен",
        "disapproved": "Одобрение пользователя снято",
        
        "no_permission": "У вас нет прав использовать эту команду",
        "user_not_found": "Пользователь не найден",
        "chat_only": "Эта команда может использоваться только в группах",
        "admin_only": "Эта команда может использоваться только администраторами",
        "owner_only": "Эта команда может использоваться только владельцем чата",
        
        "word_added": "Слово добавлено в фильтры",
        "word_removed": "Слово удалено из фильтров",
        "filter_list": "Список фильтров",
        
        "report_sent": "Жалоба отправлена администраторам",
        "reports_enabled": "Жалобы включены",
        "reports_disabled": "Жалобы отключены",
        
        "help_header": "Доступные команды:",
        "help_admin": "Команды администратора",
        "help_protection": "Команды защиты",
        "help_user": "Команды пользователя",
        
        "stats_header": "📊 Статистика бота",
        "total_users": "Всего пользователей",
        "total_chats": "Всего чатов",
        "total_warnings": "Всего предупреждений",
        "total_gbans": "Глобальные баны",
        
        "god_welcome": "👑 Добро пожаловать, {status} Разработчик! 👑",
        "god_status": "Статус режима Бога: {status}",
        "god_commands": "Команды режима Бога",
        "broadcast_sent": "Сообщение отправлено в {count} чатов",
        "restarting": "Бот перезапускается...",
        "shutting_down": "Бот выключается...",
    },
    
    "tr": {
        "bot_name": "Geo",
        "welcome": "Hoş geldin {user}!",
        "goodbye": "{user} sohbeti terk etti",
        "success": "✅ Başarılı",
        "error": "❌ Hata",
        "warning": "⚠️ Uyarı",
        "info": "ℹ️ Bilgi",
        
        "antispam_enabled": "Anti-Spam koruması etkin",
        "antispam_disabled": "Anti-Spam koruması devre dışı",
        "antibot_enabled": "Anti-Bot koruması etkin",
        "antibot_disabled": "Anti-Bot koruması devre dışı",
        "antiflood_enabled": "Anti-Flood koruması etkin",
        "antiflood_disabled": "Anti-Flood koruması devre dışı",
        "antiraid_enabled": "Anti-Raid koruması etkin",
        "antiraid_disabled": "Anti-Raid koruması devre dışı",
        "antiscam_enabled": "Anti-Scam koruması etkin",
        "antiscam_disabled": "Anti-Scam koruması devre dışı",
        "antiporn_enabled": "Anti-Porn filtresi etkin",
        "antiporn_disabled": "Anti-Porn filtresi devre dışı",
        
        "user_banned": "Kullanıcı {user} yasaklandı",
        "user_unbanned": "Kullanıcı {user} yasağı kaldırıldı",
        "user_kicked": "Kullanıcı {user} atıldı",
        "user_muted": "Kullanıcı {user} susturuldu",
        "user_unmuted": "Kullanıcı {user} susturması kaldırıldı",
        "user_warned": "Kullanıcı {user} uyarıldı ({count}/{limit})",
        "user_unwarned": "{user} için uyarı kaldırıldı",
        "user_pinned": "Mesaj sabitlendi",
        "user_unpinned": "Mesaj sabitlenmesi kaldırıldı",
        
        "settings_saved": "Ayarlar kaydedildi",
        "settings_reset": "Ayarlar sıfırlandı",
        "warn_limit_set": "Uyarı limiti {limit} olarak ayarlandı",
        "welcome_set": "Hoşgeldin mesajı ayarlandı",
        "goodbye_set": "Hoşçakal mesajı ayarlandı",
        "language_set": "Dil {lang} olarak ayarlandı",
        
        "locked": "🔒 {item} kilitlendi",
        "unlocked": "🔓 {item} kilidi açıldı",
        "lock_links": "Bağlantılar",
        "lock_spam": "Spam",
        "lock_forward": "İletmeler",
        "lock_audio": "Ses",
        "lock_video": "Videolar",
        "lock_photo": "Fotoğraflar",
        "lock_document": "Belge",
        "lock_sticker": "Çıkartmalar",
        "lock_location": "Konumlar",
        "lock_contact": "Kişiler",
        "lock_game": "Oyunlar",
        "lock_inline": "Satır içi sorgular",
        
        "staff_added": "Kullanıcı personele eklendi",
        "staff_removed": "Kullanıcı personelden çıkarıldı",
        "not_staff": "Kullanıcı personel değil",
        
        "gban_added": "Kullanıcı global yasaklandı",
        "gban_removed": "Kullanıcı global yasağı kaldırıldı",
        "gban_list": "Global Yasak Listesi",
        
        "approved": "Kullanıcı onaylandı",
        "disapproved": "Kullanıcı onayı kaldırıldı",
        
        "no_permission": "Bu komutu kullanma yetkiniz yok",
        "user_not_found": "Kullanıcı bulunamadı",
        "chat_only": "Bu komut yalnızca gruplarda kullanılabilir",
        "admin_only": "Bu komut yalnızca yöneticiler tarafından kullanılabilir",
        "owner_only": "Bu komut yalnızca sohbet sahibi tarafından kullanılabilir",
        
        "word_added": "Kelime filtrelere eklendi",
        "word_removed": "Kelime filtrelerden kaldırıldı",
        "filter_list": "Filtre Listesi",
        
        "report_sent": "Rapor yöneticilere gönderildi",
        "reports_enabled": "Raporlar etkin",
        "reports_disabled": "Raporlar devre dışı",
        
        "help_header": "Mevcut Komutlar:",
        "help_admin": "Yönetici Komutları",
        "help_protection": "Koruma Komutları",
        "help_user": "Kullanıcı Komutları",
        
        "stats_header": "📊 Bot İstatistikleri",
        "total_users": "Toplam Kullanıcı",
        "total_chats": "Toplam Sohbet",
        "total_warnings": "Toplam Uyarı",
        "total_gbans": "Global Yasaklar",
        
        "god_welcome": "👑 Hoş geldin, {status} Geliştirici! 👑",
        "god_status": "God Modu Durumu: {status}",
        "god_commands": "God Modu Komutları",
        "broadcast_sent": "Mesaj {count} sohbete gönderildi",
        "restarting": "Bot yeniden başlatılıyor...",
        "shutting_down": "Bot kapatılıyor...",
    },
    
    "de": {
        "bot_name": "Geo",
        "welcome": "Willkommen {user}!",
        "goodbye": "{user} hat den Chat verlassen",
        "success": "✅ Erfolg",
        "error": "❌ Fehler",
        "warning": "⚠️ Warnung",
        "info": "ℹ️ Info",
        
        "antispam_enabled": "Anti-Spam Schutz aktiviert",
        "antispam_disabled": "Anti-Spam Schutz deaktiviert",
        "antibot_enabled": "Anti-Bot Schutz aktiviert",
        "antibot_disabled": "Anti-Bot Schutz deaktiviert",
        "antiflood_enabled": "Anti-Flood Schutz aktiviert",
        "antiflood_disabled": "Anti-Flood Schutz deaktiviert",
        "antiraid_enabled": "Anti-Raid Schutz aktiviert",
        "antiraid_disabled": "Anti-Raid Schutz deaktiviert",
        "antiscam_enabled": "Anti-Betrug Schutz aktiviert",
        "antiscam_disabled": "Anti-Betrug Schutz deaktiviert",
        "antiporn_enabled": "Anti-Porn Filter aktiviert",
        "antiporn_disabled": "Anti-Porn Filter deaktiviert",
        
        "user_banned": "Benutzer {user} wurde verbannt",
        "user_unbanned": "Benutzer {user} wurde entbannt",
        "user_kicked": "Benutzer {user} wurde gekickt",
        "user_muted": "Benutzer {user} wurde stummgeschaltet",
        "user_unmuted": "Benutzer {user} wurde entstummt",
        "user_warned": "Benutzer {user} wurde verwarnt ({count}/{limit})",
        "user_unwarned": "Verwarnung für {user} entfernt",
        "user_pinned": "Nachricht angepinnt",
        "user_unpinned": "Nachricht losgelöst",
        
        "settings_saved": "Einstellungen gespeichert",
        "settings_reset": "Einstellungen zurückgesetzt",
        "warn_limit_set": "Verwarnungslimit auf {limit} gesetzt",
        "welcome_set": "Willkommensnachricht gesetzt",
        "goodbye_set": "Abschiedsnachricht gesetzt",
        "language_set": "Sprache auf {lang} gesetzt",
        
        "locked": "🔒 {item} gesperrt",
        "unlocked": "🔓 {item} entsperrt",
        "lock_links": "Links",
        "lock_spam": "Spam",
        "lock_forward": "Weiterleitungen",
        "lock_audio": "Audio",
        "lock_video": "Videos",
        "lock_photo": "Fotos",
        "lock_document": "Dokumente",
        "lock_sticker": "Sticker",
        "lock_location": "Standorte",
        "lock_contact": "Kontakte",
        "lock_game": "Spiele",
        "lock_inline": "Inline-Abfragen",
        
        "staff_added": "Benutzer zum Personal hinzugefügt",
        "staff_removed": "Benutzer aus Personal entfernt",
        "not_staff": "Benutzer ist kein Personal",
        
        "gban_added": "Benutzer global verbannt",
        "gban_removed": "Benutzer global entbannt",
        "gban_list": "Globale Verbannungsliste",
        
        "approved": "Benutzer genehmigt",
        "disapproved": "Genehmigung für Benutzer entfernt",
        
        "no_permission": "Du hast keine Berechtigung für diesen Befehl",
        "user_not_found": "Benutzer nicht gefunden",
        "chat_only": "Dieser Befehl kann nur in Gruppen verwendet werden",
        "admin_only": "Dieser Befehl kann nur von Admins verwendet werden",
        "owner_only": "Dieser Befehl kann nur vom Chat-Eigentümer verwendet werden",
        
        "word_added": "Wort zu Filtern hinzugefügt",
        "word_removed": "Wort aus Filtern entfernt",
        "filter_list": "Filterliste",
        
        "report_sent": "Bericht an Admins gesendet",
        "reports_enabled": "Berichte aktiviert",
        "reports_disabled": "Berichte deaktiviert",
        
        "help_header": "Verfügbare Befehle:",
        "help_admin": "Admin-Befehle",
        "help_protection": "Schutz-Befehle",
        "help_user": "Benutzer-Befehle",
        
        "stats_header": "📊 Bot-Statistiken",
        "total_users": "Gesamte Benutzer",
        "total_chats": "Gesamte Chats",
        "total_warnings": "Gesamte Verwarnungen",
        "total_gbans": "Globale Verbannungen",
        
        "god_welcome": "👑 Willkommen, {status} Entwickler! 👑",
        "god_status": "God Modus Status: {status}",
        "god_commands": "God Modus Befehle",
        "broadcast_sent": "Nachricht an {count} Chats gesendet",
        "restarting": "Bot wird neu gestartet...",
        "shutting_down": "Bot wird heruntergefahren...",
    },
    
    "pt": {
        "bot_name": "Geo",
        "welcome": "Bem-vindo {user}!",
        "goodbye": "{user} saiu do chat",
        "success": "✅ Sucesso",
        "error": "❌ Erro",
        "warning": "⚠️ Aviso",
        "info": "ℹ️ Info",
        
        "antispam_enabled": "Proteção anti-spam ativada",
        "antispam_disabled": "Proteção anti-spam desativada",
        "antibot_enabled": "Proteção anti-bot ativada",
        "antibot_disabled": "Proteção anti-bot desativada",
        "antiflood_enabled": "Proteção anti-flood ativada",
        "antiflood_disabled": "Proteção anti-flood desativada",
        "antiraid_enabled": "Proteção anti-raid ativada",
        "antiraid_disabled": "Proteção anti-raid desativada",
        "antiscam_enabled": "Proteção anti-golpe ativada",
        "antiscam_disabled": "Proteção anti-golpe desativada",
        "antiporn_enabled": "Filtro anti-pornografia ativado",
        "antiporn_disabled": "Filtro anti-pornografia desativado",
        
        "user_banned": "Usuário {user} foi banido",
        "user_unbanned": "Usuário {user} foi desbanido",
        "user_kicked": "Usuário {user} foi expulso",
        "user_muted": "Usuário {user} foi mutado",
        "user_unmuted": "Usuário {user} foi desmutado",
        "user_warned": "Usuário {user} foi avisado ({count}/{limit})",
        "user_unwarned": "Aviso removido para {user}",
        "user_pinned": "Mensagem fixada",
        "user_unpinned": "Mensagem desafixada",
        
        "settings_saved": "Configurações salvas",
        "settings_reset": "Configurações restauradas",
        "warn_limit_set": "Limite de avisos definido para {limit}",
        "welcome_set": "Mensagem de boas-vindas definida",
        "goodbye_set": "Mensagem de despedida definida",
        "language_set": "Idioma definido para {lang}",
        
        "locked": "🔒 {item} bloqueado",
        "unlocked": "🔓 {item} desbloqueado",
        "lock_links": "Links",
        "lock_spam": "Spam",
        "lock_forward": "Encaminhamentos",
        "lock_audio": "Áudio",
        "lock_video": "Vídeos",
        "lock_photo": "Fotos",
        "lock_document": "Documentos",
        "lock_sticker": "Adesivos",
        "lock_location": "Localizações",
        "lock_contact": "Contatos",
        "lock_game": "Jogos",
        "lock_inline": "Consultas inline",
        
        "staff_added": "Usuário adicionado à equipe",
        "staff_removed": "Usuário removido da equipe",
        "not_staff": "Usuário não é da equipe",
        
        "gban_added": "Usuário globalmente banido",
        "gban_removed": "Usuário globalmente desbanido",
        "gban_list": "Lista de Banimentos Globais",
        
        "approved": "Usuário aprovado",
        "disapproved": "Aprovação de usuário removida",
        
        "no_permission": "Você não tem permissão para usar este comando",
        "user_not_found": "Usuário não encontrado",
        "chat_only": "Este comando só pode ser usado em grupos",
        "admin_only": "Este comando só pode ser usado por administradores",
        "owner_only": "Este comando só pode ser usado pelo dono do chat",
        
        "word_added": "Palavra adicionada aos filtros",
        "word_removed": "Palavra removida dos filtros",
        "filter_list": "Lista de Filtros",
        
        "report_sent": "Relatório enviado aos administradores",
        "reports_enabled": "Relatórios ativados",
        "reports_disabled": "Relatórios desativados",
        
        "help_header": "Comandos Disponíveis:",
        "help_admin": "Comandos de Administrador",
        "help_protection": "Comandos de Proteção",
        "help_user": "Comandos de Usuário",
        
        "stats_header": "📊 Estatísticas do Bot",
        "total_users": "Total de Usuários",
        "total_chats": "Total de Chats",
        "total_warnings": "Total de Avisos",
        "total_gbans": "Banimentos Globais",
        
        "god_welcome": "👑 Bem-vindo, Desenvolvedor {status}! 👑",
        "god_status": "Status do Modo Deus: {status}",
        "god_commands": "Comandos do Modo Deus",
        "broadcast_sent": "Mensagem enviada para {count} chats",
        "restarting": "Bot está reiniciando...",
        "shutting_down": "Bot está desligando...",
    },
    
    "id": {
        "bot_name": "Geo",
        "welcome": "Selamat datang {user}!",
        "goodbye": "{user} telah meninggalkan obrolan",
        "success": "✅ Berhasil",
        "error": "❌ Kesalahan",
        "warning": "⚠️ Peringatan",
        "info": "ℹ️ Info",
        
        "antispam_enabled": "Perlindungan anti-spam diaktifkan",
        "antispam_disabled": "Perlindungan anti-spam dinonaktifkan",
        "antibot_enabled": "Perlindungan anti-bot diaktifkan",
        "antibot_disabled": "Perlindungan anti-bot dinonaktifkan",
        "antiflood_enabled": "Perlindungan anti-flood diaktifkan",
        "antiflood_disabled": "Perlindungan anti-flood dinonaktifkan",
        "antiraid_enabled": "Perlindungan anti-raid diaktifkan",
        "antiraid_disabled": "Perlindungan anti-raid dinonaktifkan",
        "antiscam_enabled": "Perlindungan anti-penipuan diaktifkan",
        "antiscam_disabled": "Perlindungan anti-penipuan dinonaktifkan",
        "antiporn_enabled": "Filter anti-pornografi diaktifkan",
        "antiporn_disabled": "Filter anti-pornografi dinonaktifkan",
        
        "user_banned": "Pengguna {user} telah dibanned",
        "user_unbanned": "Pengguna {user} telah di-unban",
        "user_kicked": "Pengguna {user} telah dikick",
        "user_muted": "Pengguna {user} telah dimute",
        "user_unmuted": "Pengguna {user} telah di-unmute",
        "user_warned": "Pengguna {user} telah diperingatkan ({count}/{limit})",
        "user_unwarned": "Peringatan dihapus untuk {user}",
        "user_pinned": "Pesan disematkan",
        "user_unpinned": "Pesan tidak disematkan",
        
        "settings_saved": "Pengaturan disimpan",
        "settings_reset": "Pengaturan direset",
        "warn_limit_set": "Batas peringatan diatur ke {limit}",
        "welcome_set": "Pesan selamat datang diatur",
        "goodbye_set": "Pesan perpisahan diatur",
        "language_set": "Bahasa diatur ke {lang}",
        
        "locked": "🔒 {item} dikunci",
        "unlocked": "🔓 {item} dibuka",
        "lock_links": "Tautan",
        "lock_spam": "Spam",
        "lock_forward": "Maju",
        "lock_audio": "Audio",
        "lock_video": "Video",
        "lock_photo": "Foto",
        "lock_document": "Dokumen",
        "lock_sticker": "Stiker",
        "lock_location": "Lokasi",
        "lock_contact": "Kontak",
        "lock_game": "Game",
        "lock_inline": "Kueri inline",
        
        "staff_added": "Pengguna ditambahkan ke staff",
        "staff_removed": "Pengguna dihapus dari staff",
        "not_staff": "Pengguna bukan staff",
        
        "gban_added": "Pengguna dibanned secara global",
        "gban_removed": "Pengguna di-unban secara global",
        "gban_list": "Daftar Ban Global",
        
        "approved": "Pengguna disetujui",
        "disapproved": "Persetujuan pengguna dihapus",
        
        "no_permission": "Anda tidak memiliki izin untuk menggunakan perintah ini",
        "user_not_found": "Pengguna tidak ditemukan",
        "chat_only": "Perintah ini hanya dapat digunakan di grup",
        "admin_only": "Perintah ini hanya dapat digunakan oleh admin",
        "owner_only": "Perintah ini hanya dapat digunakan oleh pemilik obrolan",
        
        "word_added": "Kata ditambahkan ke filter",
        "word_removed": "Kata dihapus dari filter",
        "filter_list": "Daftar Filter",
        
        "report_sent": "Laporan dikirim ke admin",
        "reports_enabled": "Laporan diaktifkan",
        "reports_disabled": "Laporan dinonaktifkan",
        
        "help_header": "Perintah Tersedia:",
        "help_admin": "Perintah Admin",
        "help_protection": "Perintah Perlindungan",
        "help_user": "Perintah Pengguna",
        
        "stats_header": "📊 Statistik Bot",
        "total_users": "Total Pengguna",
        "total_chats": "Total Obrolan",
        "total_warnings": "Total Peringatan",
        "total_gbans": "Ban Global",
        
        "god_welcome": "👑 Selamat datang, {status} Pengembang! 👑",
        "god_status": "Status Mode Tuhan: {status}",
        "god_commands": "Perintah Mode Tuhan",
        "broadcast_sent": "Pesan dikirim ke {count} obrolan",
        "restarting": "Bot sedang memulai ulang...",
        "shutting_down": "Bot sedang mematikan...",
    },
    
    "hi": {
        "bot_name": "Geo",
        "welcome": "स्वागत है {user}!",
        "goodbye": "{user} ने चैट छोड़ दी",
        "success": "✅ सफल",
        "error": "❌ त्रुटि",
        "warning": "⚠️ चेतावनी",
        "info": "ℹ️ जानकारी",
        
        "antispam_enabled": "एंटी-स्पैम सुरक्षा सक्षम",
        "antispam_disabled": "एंटी-स्पैम सुरक्षा अक्षम",
        "antibot_enabled": "एंटी-बॉट सुरक्षा सक्षम",
        "antibot_disabled": "एंटी-बॉट सुरक्षा अक्षम",
        "antiflood_enabled": "एंटी-फ्लड सुरक्षा सक्षम",
        "antiflood_disabled": "एंटी-फ्लड सुरक्षा अक्षम",
        "antiraid_enabled": "एंटी-रेड सुरक्षा सक्षम",
        "antiraid_disabled": "एंटी-रेड सुरक्षा अक्षम",
        "antiscam_enabled": "एंटी-घोटाला सुरक्षा सक्षम",
        "antiscam_disabled": "एंटी-घोटाला सुरक्षा अक्षम",
        "antiporn_enabled": "एंटी-पोर्न फिल्टर सक्षम",
        "antiporn_disabled": "एंटी-पोर्न फिल्टर अक्षम",
        
        "user_banned": "उपयोगकर्ता {user} प्रतिबंधित",
        "user_unbanned": "उपयोगकर्ता {user} अनबैन",
        "user_kicked": "उपयोगकर्ता {user} निकाला गया",
        "user_muted": "उपयोगकर्ता {user} म्यूट",
        "user_unmuted": "उपयोगकर्ता {user} अनम्यूट",
        "user_warned": "उपयोगकर्ता {user} चेतावनी ({count}/{limit})",
        "user_unwarned": "{user} के लिए चेतावनी हटाई गई",
        "user_pinned": "संदेश पिन",
        "user_unpinned": "संदेश अनपिन",
        
        "settings_saved": "सेटिंग्स सहेजी गईं",
        "settings_reset": "सेटिंग्स रीसेट",
        "warn_limit_set": "चेतावनी सीमा {limit} पर सेट",
        "welcome_set": "स्वागत संदेश सेट",
        "goodbye_set": "विदाई संदेश सेट",
        "language_set": "भाषा {lang} पर सेट",
        
        "locked": "🔒 {item} लॉक",
        "unlocked": "🔓 {item} अनलॉक",
        "lock_links": "लिंक",
        "lock_spam": "स्पैम",
        "lock_forward": "फॉरवर्ड",
        "lock_audio": "ऑडियो",
        "lock_video": "वीडियो",
        "lock_photo": "फोटो",
        "lock_document": "दस्तावेज़",
        "lock_sticker": "स्टिकर",
        "lock_location": "स्थान",
        "lock_contact": "संपर्क",
        "lock_game": "गेम",
        "lock_inline": "इनलाइन क्वेरी",
        
        "staff_added": "उपयोगकर्ता स्टाफ में जोड़ा गया",
        "staff_removed": "उपयोगकर्ता स्टाफ से हटाया गया",
        "not_staff": "उपयोगकर्ता स्टाफ नहीं",
        
        "gban_added": "उपयोगकर्ता वैश्विक रूप से प्रतिबंधित",
        "gban_removed": "उपयोगकर्ता वैश्विक रूप से अनबैन",
        "gban_list": "वैश्विक बैन सूची",
        
        "approved": "उपयोगकर्ता स्वीकृत",
        "disapproved": "उपयोगकर्ता की स्वीकृति हटाई गई",
        
        "no_permission": "आपके पास इस कमांड का उपयोग करने की अनुमति नहीं है",
        "user_not_found": "उपयोगकर्ता नहीं मिला",
        "chat_only": "यह कमांड केवल समूहों में उपयोग किया जा सकता है",
        "admin_only": "यह कमांड केवल एडमिन द्वारा उपयोग किया जा सकता है",
        "owner_only": "यह कमांड केवल चैट स्वामी द्वारा उपयोग किया जा सकता है",
        
        "word_added": "शब्द फिल्टर में जोड़ा गया",
        "word_removed": "शब्द फिल्टर से हटाया गया",
        "filter_list": "फिल्टर सूची",
        
        "report_sent": "रिपोर्ट एडमिन को भेजी गई",
        "reports_enabled": "रिपोर्ट सक्षम",
        "reports_disabled": "रिपोर्ट अक्षम",
        
        "help_header": "उपलब्ध कमांड:",
        "help_admin": "एडमिन कमांड",
        "help_protection": "सुरक्षा कमांड",
        "help_user": "उपयोगकर्ता कमांड",
        
        "stats_header": "📊 बॉट सांख्यिकी",
        "total_users": "कुल उपयोगकर्ता",
        "total_chats": "कुल चैट",
        "total_warnings": "कुल चेतावनी",
        "total_gbans": "वैश्विक बैन",
        
        "god_welcome": "👑 स्वागत है, {status} डेवलपर! 👑",
        "god_status": "गॉड मोड स्थिति: {status}",
        "god_commands": "गॉड मोड कमांड",
        "broadcast_sent": "संदेश {count} चैट में भेजा गया",
        "restarting": "बॉट पुनः आरंभ हो रहा है...",
        "shutting_down": "बॉट बंद हो रहा है...",
    },
    
    "zh": {
        "bot_name": "Geo",
        "welcome": "欢迎 {user}!",
        "goodbye": "{user} 已离开聊天",
        "success": "✅ 成功",
        "error": "❌ 错误",
        "warning": "⚠️ 警告",
        "info": "ℹ️ 信息",
        
        "antispam_enabled": "反垃圾消息保护已启用",
        "antispam_disabled": "反垃圾消息保护已禁用",
        "antibot_enabled": "反机器人保护已启用",
        "antibot_disabled": "反机器人保护已禁用",
        "antiflood_enabled": "反洪水保护已启用",
        "antiflood_disabled": "反洪水保护已禁用",
        "antiraid_enabled": "反攻击保护已启用",
        "antiraid_disabled": "反攻击保护已禁用",
        "antiscam_enabled": "反诈骗保护已启用",
        "antiscam_disabled": "反诈骗保护已禁用",
        "antiporn_enabled": "反色情过滤器已启用",
        "antiporn_disabled": "反色情过滤器已禁用",
        
        "user_banned": "用户 {user} 已被封禁",
        "user_unbanned": "用户 {user} 已解封",
        "user_kicked": "用户 {user} 已被踢出",
        "user_muted": "用户 {user} 已被禁言",
        "user_unmuted": "用户 {user} 已解除禁言",
        "user_warned": "用户 {user} 已被警告 ({count}/{limit})",
        "user_unwarned": "{user} 的警告已移除",
        "user_pinned": "消息已置顶",
        "user_unpinned": "消息已取消置顶",
        
        "settings_saved": "设置已保存",
        "settings_reset": "设置已重置",
        "warn_limit_set": "警告限制已设置为 {limit}",
        "welcome_set": "欢迎消息已设置",
        "goodbye_set": "告别消息已设置",
        "language_set": "语言已设置为 {lang}",
        
        "locked": "🔒 {item} 已锁定",
        "unlocked": "🔓 {item} 已解锁",
        "lock_links": "链接",
        "lock_spam": "垃圾消息",
        "lock_forward": "转发",
        "lock_audio": "音频",
        "lock_video": "视频",
        "lock_photo": "照片",
        "lock_document": "文档",
        "lock_sticker": "贴纸",
        "lock_location": "位置",
        "lock_contact": "联系人",
        "lock_game": "游戏",
        "lock_inline": "内联查询",
        
        "staff_added": "用户已添加到员工",
        "staff_removed": "用户已从员工中移除",
        "not_staff": "用户不是员工",
        
        "gban_added": "用户已被全局封禁",
        "gban_removed": "用户已被全局解封",
        "gban_list": "全局封禁列表",
        
        "approved": "用户已批准",
        "disapproved": "用户的批准已移除",
        
        "no_permission": "你没有权限使用此命令",
        "user_not_found": "用户未找到",
        "chat_only": "此命令只能在群组中使用",
        "admin_only": "此命令只能由管理员使用",
        "owner_only": "此命令只能由群主使用",
        
        "word_added": "词语已添加到过滤器",
        "word_removed": "词语已从过滤器移除",
        "filter_list": "过滤器列表",
        
        "report_sent": "报告已发送给管理员",
        "reports_enabled": "报告已启用",
        "reports_disabled": "报告已禁用",
        
        "help_header": "可用命令：",
        "help_admin": "管理员命令",
        "help_protection": "保护命令",
        "help_user": "用户命令",
        
        "stats_header": "📊 机器人统计",
        "total_users": "用户总数",
        "total_chats": "聊天总数",
        "total_warnings": "警告总数",
        "total_gbans": "全局封禁",
        
        "god_welcome": "👑 欢迎，{status} 开发者！👑",
        "god_status": "上帝模式状态：{status}",
        "god_commands": "上帝模式命令",
        "broadcast_sent": "消息已发送到 {count} 个聊天",
        "restarting": "机器人正在重启...",
        "shutting_down": "机器人正在关闭...",
    },
}


class Translator:
    """Translation manager"""
    
    def __init__(self):
        self.translations = TRANSLATIONS
        self.default_lang = "en"
        self._cache = {}
    
    def get(self, text: str, lang: str = "en", **kwargs) -> str:
        """Get translated text"""
        if lang not in self.translations:
            lang = self.default_lang
        
        translation = self.translations.get(lang, {}).get(text)
        if not translation:
            translation = self.translations.get(self.default_lang, {}).get(text, text)
        
        if kwargs:
            translation = translation.format(**kwargs)
        
        return translation
    
    def get_all_languages(self) -> Dict[str, str]:
        """Get all available languages"""
        return {
            "en": "English",
            "es": "Español",
            "ar": "العربية",
            "ru": "Русский",
            "tr": "Türkçe",
            "de": "Deutsch",
            "pt": "Português",
            "id": "Bahasa Indonesia",
            "hi": "हिन्दी",
            "zh": "中文",
        }


# Global translator instance
translator = Translator()


def get_text(text: str, lang: str = "en", **kwargs) -> str:
    """Quick access to translations"""
    return translator.get(text, lang, **kwargs)