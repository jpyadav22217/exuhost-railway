"""
=============================================================
        TELEGRAM FIREBASE EXTRACTOR BOT (MINATO)
=============================================================
"""

# import requests
# TELEGRAM_SESSION = requests.Session()
# import re
# import urllib.parse
# import time
# import base64
# import os
# import tempfile
# import zipfile
# import json
# import html
# import threading
# import sqlite3
# from concurrent.futures import ThreadPoolExecutor, as_completed


import requests
TELEGRAM_SESSION = requests.Session()
import re
import urllib.parse
import time
import base64
import os
import tempfile
import zipfile
import json
import html
import threading
import sqlite3
from concurrent.futures import ThreadPoolExecutor, as_completed

# ── Directory setup ──────────────────────────────────────────
BASE_DIR = os.environ.get("DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
os.makedirs(BASE_DIR, exist_ok=True)

# ═══════════════════════════════════════════════════════════════
# TELEGRAM BOT CONFIGURATION
# ═══════════════════════════════════════════════════════════════
# 
DEFAULT_TG_TOKEN = os.environ.get("FB_BOT_TOKEN", "")
# TOKEN_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bot_token_friend.txt")
TOKEN_FILE = os.path.join(BASE_DIR, "bot_token_friend.txt")

def _load_bot_token():
    try:
        with open(TOKEN_FILE, "r", encoding="utf-8") as file:
            token = file.read().strip()
        if token:
            return token
    except Exception:
        pass
    try:
        with open(TOKEN_FILE, "w", encoding="utf-8") as file:
            file.write(DEFAULT_TG_TOKEN)
    except Exception:
        pass
    return DEFAULT_TG_TOKEN

TG_TOKEN = _load_bot_token()
print(f"[*] Using bot token from {TOKEN_FILE}: {TG_TOKEN[:12]}...{TG_TOKEN[-6:]}")
TG_GATEWAY = f"https://api.telegram.org/bot{TG_TOKEN}"
ADMIN_ID = 8960648271
BOT_BRAND = "FIREBASE EXTRACTOR"

FORCE_JOIN_CHANNELS = [
    {"chat_id": "@rewardradar0007", "join_url": "https://t.me/rewardradar0007", "label": "RADAR"},
    {"chat_id": "@TGautodidact",    "join_url": "https://t.me/TGautodidact",    "label": "TG AUDIT"},
]

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# USERS_FILE = os.path.join(BASE_DIR, "firebase_bot_users_friend.json")
# LINKS_FILE = os.path.join(BASE_DIR, "firebase_bot_links_friend.json")
# BATCH_DB_FILE = os.path.join(BASE_DIR, "firebase_bot_batches_friend.sqlite3")
# WEB_LINKS_FILE = os.path.join(BASE_DIR, "firebase_bot_web_links_friend.json")

# BASE_DIR = os.environ.get("DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
# os.makedirs(BASE_DIR, exist_ok=True)
USERS_FILE = os.path.join(BASE_DIR, "firebase_bot_users_friend.json")
LINKS_FILE = os.path.join(BASE_DIR, "firebase_bot_links_friend.json")
BATCH_DB_FILE = os.path.join(BASE_DIR, "firebase_bot_batches_friend.sqlite3")
WEB_LINKS_FILE = os.path.join(BASE_DIR, "firebase_bot_web_links_friend.json")
IST_OFFSET = 5.5 * 3600

BOT_USERNAME_CACHE = {'value': None}
BOT_USERNAME_LOCK = threading.Lock()

# ── Bulk Scan State ──────────────────────────────────────────
BULK_MODE_LOCK = threading.Lock()
BULK_MODE_USERS = {}

def set_bulk_mode(chat_id, on):
    with BULK_MODE_LOCK:
        if on: BULK_MODE_USERS.setdefault(int(chat_id), [])
        else: BULK_MODE_USERS.pop(int(chat_id), None)

def is_bulk_mode(chat_id):
    with BULK_MODE_LOCK:
        return int(chat_id) in BULK_MODE_USERS

def add_bulk_file(chat_id, file_id, file_name):
    with BULK_MODE_LOCK:
        bucket = BULK_MODE_USERS.setdefault(int(chat_id), [])
        bucket.append((file_id, file_name))
        return len(bucket)

def get_bulk_files(chat_id):
    with BULK_MODE_LOCK:
        return list(BULK_MODE_USERS.get(int(chat_id), []))

# ── FB Filter State (user-provided links only) ───────────────
FILTER_STATE_LOCK = threading.Lock()
FILTER_STATE = {}   # {chat_id: {"step": "links"|"min", "links": [...]}}

def start_filter(chat_id):
    with FILTER_STATE_LOCK:
        FILTER_STATE[int(chat_id)] = {"step": "links", "links": []}

def get_filter_state(chat_id):
    with FILTER_STATE_LOCK:
        st = FILTER_STATE.get(int(chat_id))
        return dict(st) if st else None

def set_filter_step(chat_id, step, links=None):
    with FILTER_STATE_LOCK:
        st = FILTER_STATE.get(int(chat_id))
        if st is None:
            st = {"step": step, "links": links or []}
            FILTER_STATE[int(chat_id)] = st
        else:
            st["step"] = step
            if links is not None:
                st["links"] = links

def clear_filter(chat_id):
    with FILTER_STATE_LOCK:
        FILTER_STATE.pop(int(chat_id), None)

def is_filter_mode(chat_id):
    with FILTER_STATE_LOCK:
        return int(chat_id) in FILTER_STATE


def get_bot_username():
    with BOT_USERNAME_LOCK:
        if BOT_USERNAME_CACHE['value']:
            return BOT_USERNAME_CACHE['value']
    try:
        response = TELEGRAM_SESSION.get(f"{TG_GATEWAY}/getMe", timeout=10)
        data = response.json()
        name = (data.get('result') or {}).get('username')
        if name:
            with BOT_USERNAME_LOCK: BOT_USERNAME_CACHE['value'] = name
            return name
    except Exception: pass
    return 'FirebaseExtractorBot'


UPDATE_EXECUTOR = ThreadPoolExecutor(max_workers=8)
FAST_EXECUTOR = ThreadPoolExecutor(max_workers=16)
HEAVY_EXECUTOR = ThreadPoolExecutor(max_workers=4)
ADMIN_EXECUTOR = ThreadPoolExecutor(max_workers=2)
BATCH_EXECUTOR = ThreadPoolExecutor(max_workers=8)
BATCH_TASKS = {}
BATCH_TASKS_LOCK = threading.Lock()
WEBSITE_BATCH_DELAY = 0.5
USERS_LOCK = threading.RLock()
LINKS_LOCK = threading.RLock()
USER_CACHE = None
LINK_CACHE = None
LINK_DUPLICATE_COUNT = 0
ADMIN_STATE_LOCK = threading.Lock()
ADMIN_BROADCAST_MODE = False
BROADCAST_CANCEL_EVENT = threading.Event()
CHAT_LOCKS_LOCK = threading.Lock()
CHAT_LOCKS = {}
WEBSITE_MODE_LOCK = threading.Lock()
WEBSITE_MODE_USERS = set()
MAX_DIRECT_WEBSITE_URLS = 5
MAX_FILE_WEBSITE_URLS = 600
MAX_FILTER_LINKS = 1000


def telegram_call(method, payload=None, timeout=15):
    try:
        response = TELEGRAM_SESSION.post(f"{TG_GATEWAY}/{method}", json=payload or {}, timeout=timeout)
        data = response.json()
        if response.status_code != 200 or not data.get("ok"): return None
        return data.get("result")
    except Exception:
        return None


def send_message(chat_id, text, reply_markup=None):
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML", "disable_web_page_preview": True}
    if reply_markup is not None: payload["reply_markup"] = reply_markup
    return telegram_call("sendMessage", payload, timeout=15)


def edit_message_text(chat_id, message_id, text, reply_markup=None):
    payload = {"chat_id": chat_id, "message_id": message_id, "text": text, "parse_mode": "HTML", "disable_web_page_preview": True}
    if reply_markup is not None: payload["reply_markup"] = reply_markup
    return telegram_call("editMessageText", payload, timeout=15)


def safe_remove_file(file_path):
    if not file_path: return
    try:
        if os.path.isfile(file_path): os.remove(file_path)
    except Exception as cleanup_error:
        print(f"[!] Temporary file cleanup error: {cleanup_error}")


def init_batch_database():
    with sqlite3.connect(BATCH_DB_FILE) as connection:
        connection.execute("PRAGMA journal_mode=WAL")
        connection.execute("""CREATE TABLE IF NOT EXISTS website_batches (
            job_id TEXT PRIMARY KEY, user_id INTEGER NOT NULL, file_name TEXT NOT NULL,
            total INTEGER NOT NULL, completed INTEGER NOT NULL DEFAULT 0,
            sent INTEGER NOT NULL DEFAULT 0, failed INTEGER NOT NULL DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'queued', user_message_id INTEGER,
            admin_message_id INTEGER, created_at REAL NOT NULL, updated_at REAL NOT NULL)""")
        connection.execute("""CREATE TABLE IF NOT EXISTS website_batch_items (
            job_id TEXT NOT NULL, item_index INTEGER NOT NULL, website_url TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending', result_text TEXT, error_text TEXT,
            PRIMARY KEY (job_id, item_index))""")
        connection.execute("""CREATE TABLE IF NOT EXISTS user_state (
            user_id INTEGER PRIMARY KEY, username TEXT, first_name TEXT,
            created_at REAL NOT NULL, updated_at REAL NOT NULL)""")
        connection.execute("""CREATE TABLE IF NOT EXISTS scan_stats (
            id INTEGER PRIMARY KEY CHECK (id=1), total_scans INTEGER NOT NULL DEFAULT 0,
            link_scans INTEGER NOT NULL DEFAULT 0, apk_scans INTEGER NOT NULL DEFAULT 0)""")
        connection.execute("INSERT OR IGNORE INTO scan_stats(id) VALUES (1)")
        connection.commit()


init_batch_database()


def create_batch_job(user_id, file_name, website_urls):
    job_id = f"web-{int(time.time())}-{threading.get_ident()}"
    now = time.time()
    with sqlite3.connect(BATCH_DB_FILE) as connection:
        connection.execute("INSERT INTO website_batches (job_id, user_id, file_name, total, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
            (job_id, int(user_id), file_name or "website_links.txt", len(website_urls), now, now))
        connection.executemany("INSERT INTO website_batch_items (job_id, item_index, website_url) VALUES (?, ?, ?)",
            [(job_id, index, url) for index, url in enumerate(website_urls)])
        connection.commit()
    return job_id


def get_batch(job_id):
    with sqlite3.connect(BATCH_DB_FILE) as connection:
        connection.row_factory = sqlite3.Row
        row = connection.execute("SELECT * FROM website_batches WHERE job_id=?", (job_id,)).fetchone()
        return dict(row) if row else None


def get_pending_batch_item(job_id):
    with sqlite3.connect(BATCH_DB_FILE) as connection:
        connection.row_factory = sqlite3.Row
        row = connection.execute("SELECT * FROM website_batch_items WHERE job_id=? AND status IN ('pending','processing') ORDER BY item_index LIMIT 1", (job_id,)).fetchone()
        return dict(row) if row else None


def mark_batch_item(job_id, item_index, status, result_text=None, error_text=None):
    with sqlite3.connect(BATCH_DB_FILE) as connection:
        connection.execute("UPDATE website_batch_items SET status=?, result_text=?, error_text=? WHERE job_id=? AND item_index=?",
            (status, result_text, error_text, job_id, item_index))
        connection.execute("""UPDATE website_batches SET
            completed=(SELECT COUNT(*) FROM website_batch_items WHERE job_id=? AND status IN ('sent','failed')),
            sent=(SELECT COUNT(*) FROM website_batch_items WHERE job_id=? AND status='sent'),
            failed=(SELECT COUNT(*) FROM website_batch_items WHERE job_id=? AND status='failed'),
            updated_at=? WHERE job_id=?""", (job_id, job_id, job_id, time.time(), job_id))
        connection.commit()


def mark_batch_status(job_id, status):
    with sqlite3.connect(BATCH_DB_FILE) as connection:
        connection.execute("UPDATE website_batches SET status=?, updated_at=? WHERE job_id=?", (status, time.time(), job_id))
        connection.commit()


def get_resumable_batch_ids():
    with sqlite3.connect(BATCH_DB_FILE) as connection:
        return [row[0] for row in connection.execute("SELECT job_id FROM website_batches WHERE status IN ('queued','running') AND completed < total").fetchall()]


def batch_progress_text(batch, status=None):
    processed = int(batch["completed"]); total = int(batch["total"])
    percent = (processed / total * 100) if total else 100
    return (f"📄 <b>Website link file:</b> {html.escape(batch['file_name'])}\n"
            f"📊 <b>Progress: {processed:02d}/{total}</b> — {percent:.2f}%\n"
            f"📤 <b>Sent:</b> {batch['sent']}\n❌ <b>Failed:</b> {batch['failed']}\n"
            f"⏳ <b>Remaining:</b> {max(0, total - processed)}\n"
            f"🔄 <b>Status:</b> {html.escape(status or batch['status'])}")


def update_batch_progress(job_id, status=None):
    batch = get_batch(job_id)
    if not batch: return
    text = batch_progress_text(batch, status=status)
    if batch.get("user_message_id"):
        edit_message_text(batch["user_id"], batch["user_message_id"], text, reply_markup=main_keyboard())
    if batch.get("admin_message_id"):
        edit_message_text(ADMIN_ID, batch["admin_message_id"], text, reply_markup=admin_keyboard())


def write_batch_result_file(job_id):
    batch = get_batch(job_id)
    if not batch: return None
    with sqlite3.connect(BATCH_DB_FILE) as connection:
        rows = connection.execute("SELECT item_index, website_url, result_text, error_text, status FROM website_batch_items WHERE job_id=? ORDER BY item_index", (job_id,)).fetchall()
    output = tempfile.NamedTemporaryFile(prefix=f"firebase_batch_{job_id}_", suffix=".txt", mode="w", encoding="utf-8", delete=False)
    output_path = output.name
    try:
        output.write(f"{BOT_BRAND} — Website Batch {job_id}\nFile: {batch['file_name']}\nTotal: {batch['total']}\nSent: {batch['sent']}\nFailed: {batch['failed']}\n\n")
        for item_index, website_url, result_text, error_text, status in rows:
            output.write(f"[{item_index + 1}/{batch['total']}] {status.upper()}\nWebsite: {website_url}\n")
            output.write((result_text or error_text or "No result") + "\n\n")
        output.close(); return output_path
    except Exception:
        output.close(); safe_remove_file(output_path); return None


def send_batch_result_file(job_id):
    output_path = write_batch_result_file(job_id)
    if not output_path: return
    try:
        batch = get_batch(job_id)
        caption = f"📦 <b>Website batch complete</b>\nTotal: {batch['total']} | Sent: {batch['sent']} | Failed: {batch['failed']}"
        send_document(batch["user_id"], output_path, caption=caption)
        send_document(ADMIN_ID, output_path, caption=f"Job {job_id} — {caption}")
    finally: safe_remove_file(output_path)


def delete_message(chat_id, message_id):
    telegram_call("deleteMessage", {"chat_id": chat_id, "message_id": message_id}, timeout=10)


def get_users():
    global USER_CACHE
    with USERS_LOCK:
        if USER_CACHE is not None: return set(USER_CACHE)
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
            USER_CACHE = {int(user_id) for user_id in data} if isinstance(data, list) else set()
        except Exception:
            USER_CACHE = set()
        return set(USER_CACHE)


def save_user(chat_id):
    global USER_CACHE
    try:
        with USERS_LOCK:
            if USER_CACHE is None: get_users()
            chat_id = int(chat_id)
            if chat_id in USER_CACHE: return
            USER_CACHE.add(chat_id)
            temp_users = USERS_FILE + ".tmp"
            with open(temp_users, "w", encoding="utf-8") as file:
                json.dump(sorted(USER_CACHE), file)
            os.replace(temp_users, USERS_FILE)
    except Exception: pass


def user_state_exists(user_id):
    with sqlite3.connect(BATCH_DB_FILE) as connection:
        return connection.execute("SELECT 1 FROM user_state WHERE user_id=?", (int(user_id),)).fetchone() is not None


def get_user_state(user_id, user=None):
    now = time.time()
    with sqlite3.connect(BATCH_DB_FILE) as connection:
        connection.row_factory = sqlite3.Row
        row = connection.execute("SELECT * FROM user_state WHERE user_id=?", (int(user_id),)).fetchone()
        if not row:
            user = user or {}
            connection.execute("INSERT INTO user_state(user_id,username,first_name,created_at,updated_at) VALUES(?,?,?,?,?)",
                (int(user_id), user.get("username", ""), user.get("first_name", "User"), now, now))
            connection.commit()
            row = connection.execute("SELECT * FROM user_state WHERE user_id=?", (int(user_id),)).fetchone()
        elif user:
            connection.execute("UPDATE user_state SET username=?, first_name=?, updated_at=? WHERE user_id=?",
                (user.get("username", ""), user.get("first_name", "User"), now, int(user_id)))
            connection.commit()
            row = connection.execute("SELECT * FROM user_state WHERE user_id=?", (int(user_id),)).fetchone()
        return dict(row)


def ist_datetime(timestamp):
    return time.strftime("%d %B %Y, %I:%M %p IST", time.localtime(timestamp + IST_OFFSET))


def update_scan_stat(kind):
    with sqlite3.connect(BATCH_DB_FILE) as connection:
        connection.execute("UPDATE scan_stats SET total_scans=total_scans+1, {}_scans={}_scans+1 WHERE id=1".format(kind, kind))
        connection.commit()


def get_admin_panel_text():
    with sqlite3.connect(BATCH_DB_FILE) as connection:
        total_users = connection.execute("SELECT COUNT(*) FROM user_state").fetchone()[0]
        stats = connection.execute("SELECT total_scans,link_scans,apk_scans FROM scan_stats WHERE id=1").fetchone()
    return ("🛠️ 𝘼𝘿𝙈𝙄𝙉 𝙋𝘼𝙉𝙀𝙇\n━━━━━━━━━━━━━━━━━━\n"
            f"📌 𝙏𝙊𝙏𝘼𝙇 𝙐𝙎𝙀𝙍𝙎: <code>{total_users:,}</code>\n"
            f"📦 𝙏𝙊𝙏𝘼𝙇 𝙎𝘾𝘼𝙉𝙎: <code>{stats[0] + LEGACY_TOTAL_SCANS:,}</code>\n"
            f"🔗 𝙇𝙄𝙉𝙆 𝙎𝘾𝘼𝙉𝙎: <code>{stats[1] + LEGACY_LINK_SCANS:,}</code>\n"
            f"📥 𝘼𝙋𝙆 𝙎𝘾𝘼𝙉𝙎: <code>{stats[2] + LEGACY_APK_SCANS:,}</code>\n"
            "━━━━━━━━━━━━━━━━━━\n\n𝘾𝙝𝙤𝙤𝙨𝙚 𝙖𝙣 𝙖𝙘𝙩𝙞𝙤𝙣 𝙗𝙚𝙡𝙤𝙬.")


def main_keyboard():
    return {"keyboard": [
        [{"text": "📤 𝙐𝙋𝙇𝙊𝘼𝘿 𝘼𝙋𝙆", "style": "success"}, {"text": "🌐 𝙎𝘾𝘼𝙉 𝙒𝙀𝘽𝙎𝙄𝙏𝙀", "style": "primary"}],
        [{"text": "📦 𝘽𝙐𝙇𝙆 𝙎𝘾𝘼𝙉", "style": "primary"}, {"text": "🎯 𝙁𝘽 𝙁𝙄𝙇𝙏𝙀𝙍", "style": "primary"}],
    ], "resize_keyboard": True, "is_persistent": True}


def bulk_scan_keyboard():
    return {"keyboard": [
        [{"text": "✅ 𝙎𝘾𝘼𝙉 𝘼𝙇𝙇", "style": "success"}],
        [{"text": "❌ 𝘾𝘼𝙉𝘾𝙀𝙇", "style": "danger"}],
    ], "resize_keyboard": True, "is_persistent": True}


def upgraded_admin_keyboard():
    return {"keyboard": [
        [{"text": "📢 𝘽𝙍𝙊𝘼𝘿𝘾𝘼𝙎𝙏", "style": "primary"}, {"text": "🔗 𝙈𝘼𝙉𝘼𝙂𝙀 𝙇𝙄𝙉𝙆𝙎", "style": "primary"}],
    ], "resize_keyboard": True, "is_persistent": True}


def admin_keyboard():
    return upgraded_admin_keyboard()


def manage_links_screen(chat_id):
    send_message(chat_id, "🔗 𝙈𝘼𝙉𝘼𝙂𝙀 𝙇𝙄𝙉𝙆𝙎\n━━━━━━━━━━━━━━━━━━━━\n\n𝘾𝙝𝙤𝙤𝙨𝙚 𝙖 𝙡𝙞𝙣𝙠 𝙘𝙤𝙡𝙡𝙚𝙘𝙩𝙞𝙤𝙣.", reply_markup=manage_links_keyboard())


def manage_links_keyboard():
    return {"keyboard": [[{"text": "🔥 𝙂𝙀𝙏 𝙁𝙄𝙍𝙀𝘽𝘼𝙎𝙀 𝙇𝙄𝙉𝙆𝙎", "style": "primary"}], [{"text": "🌐 𝙒𝙀𝘽 𝙇𝙄𝙉𝙆𝙎", "style": "primary"}]], "resize_keyboard": True, "is_persistent": True}


def send_web_links_collection(chat_id):
    count, duplicates = get_web_link_stats()
    path = write_web_links_file()
    if not path:
        send_message(chat_id, "❌ 𝙒𝙚𝙗 𝙡𝙞𝙣𝙠 𝙛𝙞𝙡𝙚 𝙜𝙚𝙣𝙚𝙧𝙖𝙩𝙞𝙤𝙣 𝙛𝙖𝙞𝙡𝙚𝙙.", reply_markup=admin_keyboard()); return
    try:
        send_document(chat_id, path, caption=f"🌐 <b>Web Links Collection</b>\n\n🔢 <b>Total Unique Web Links: <code>{count}</code></b>\n♻️ <b>Duplicate Detections: <code>{duplicates}</code></b>")
    finally: safe_remove_file(path)


# ═══════════════════════════════════════════════════════════════
# FIREBASE ONLINE-DEVICE ANALYZER (sharpened)
# ═══════════════════════════════════════════════════════════════
_BOOL_TRUE = {True, 1, "1", "true", "True", "TRUE", "yes", "Yes", "YES", "on", "On", "ON"}

_ONLINE_BOOL_MARKERS = (
    "online", "isOnline", "is_online", "is_Online", "isOnlineFlag",
    "user_online", "userOnline", "currentlyOnline", "is_active",
    "isActive", "active", "connected", "presence",
)
_STATUS_MARKERS = ("status", "state", "online_status", "onlineStatus", "userStatus")
_STATUS_ONLINE_VALUES = {"online", "active", "connected", "1", "true", "yes", "on"}

_TIMESTAMP_MARKERS = (
    "lastSeen", "last_seen", "lastseen", "last_Seen",
    "lastLogin", "last_login", "lastActive", "last_active",
    "lastUpdate", "last_update", "updatedAt", "updated_at",
    "timestamp", "time", "ts", "lastOnline", "last_online",
)
_TIMESTAMP_ONLINE_WINDOW = 300

_DIRECT_ONLINE_KEYS = (
    "online", "onlineUsers", "online_users", "onlineCount", "online_count",
    "onlineDevices", "devices_online", "activeUsers", "active_users",
    "activeCount", "live", "liveUsers", "live_users", "connected",
    "connectedUsers", "presence",
)

def _is_truthy_online(v):
    if isinstance(v, bool): return v
    if isinstance(v, (int, float)): return v == 1
    if isinstance(v, str): return v.strip().lower() in ("1", "true", "yes", "on", "online", "active", "connected")
    return False

def _timestamp_is_online(item, now):
    for marker in _TIMESTAMP_MARKERS:
        if marker not in item: continue
        v = item[marker]
        ts = None
        if isinstance(v, (int, float)): ts = float(v)
        elif isinstance(v, str):
            try: ts = float(v)
            except Exception: continue
        if not ts or ts <= 0: continue
        if ts > 1e12: ts = ts / 1000.0
        if ts < 946684800 or ts > now + 86400: continue
        if 0 < (now - ts) <= _TIMESTAMP_ONLINE_WINDOW: return True
    return False

def _item_is_online(item, now):
    if not isinstance(item, dict): return False
    for m in _ONLINE_BOOL_MARKERS:
        if m in item and _is_truthy_online(item[m]): return True
    for m in _STATUS_MARKERS:
        if m in item:
            v = item[m]
            if isinstance(v, str) and v.strip().lower() in _STATUS_ONLINE_VALUES: return True
            if isinstance(v, bool) and v: return True
    if _timestamp_is_online(item, now): return True
    return False


def analyze_firebase_database(db_url, timeout=6):
    now = time.time()
    try:
        base = db_url.rstrip("/")
        if base.startswith("http://"): base = "https://" + base[len("http://"):]
        url = base + "/.json"
        resp = TELEGRAM_SESSION.get(url, timeout=timeout)
        if resp.status_code != 200: return None
        try: data = resp.json()
        except Exception: return None
        if data is None:
            return {"readable": True, "empty": True, "online": 0, "total": 0, "keys": []}
        online = 0; total = 0; keys = []
        if isinstance(data, dict):
            keys = list(data.keys())
            direct_online = 0
            for dk in _DIRECT_ONLINE_KEYS:
                if dk in data:
                    v = data[dk]
                    if isinstance(v, bool): direct_online = max(direct_online, 1 if v else 0)
                    elif isinstance(v, int): direct_online = max(direct_online, v)
                    elif isinstance(v, str):
                        try: direct_online = max(direct_online, int(v))
                        except Exception: pass
                    elif isinstance(v, (dict, list)): direct_online = max(direct_online, len(v))
            for k, v in data.items():
                if k in _DIRECT_ONLINE_KEYS:
                    if isinstance(v, dict): total += len(v)
                    continue
                if isinstance(v, dict):
                    total += len(v)
                    for item in v.values():
                        if isinstance(item, dict):
                            if _item_is_online(item, now): online += 1
                        elif _is_truthy_online(item): online += 1
                elif isinstance(v, list):
                    total += len(v)
                    for item in v:
                        if isinstance(item, dict):
                            if _item_is_online(item, now): online += 1
                        elif _is_truthy_online(item): online += 1
                elif isinstance(v, bool) and k.lower() in ("online", "active", "connected"):
                    online += 1
            online = max(online, direct_online)
        elif isinstance(data, list):
            total = len(data)
            for item in data:
                if isinstance(item, dict):
                    if _item_is_online(item, now): online += 1
                elif _is_truthy_online(item): online += 1
        return {"readable": True, "empty": False, "online": online, "total": total, "keys": keys[:15]}
    except Exception:
        return None


def analyze_databases_parallel(databases):
    databases = list(databases)
    if not databases: return {}
    results = {}
    workers = min(20, max(1, len(databases)))
    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_map = {executor.submit(analyze_firebase_database, db): db for db in databases}
        for future in as_completed(future_map):
            db = future_map[future]
            try: results[db] = future.result(timeout=15)
            except Exception: results[db] = None
    return results


def format_firebase_list_with_analysis(databases, analyses=None):
    databases = sorted(databases)
    if analyses is None: analyses = analyze_databases_parallel(databases)
    lines = []
    for index, db in enumerate(databases, 1):
        info = analyses.get(db); safe_url = html.escape(db)
        if info is None:
            lines.append(f"{index}. 🔒 <code>{safe_url}</code>\n   └ 𝙎𝙩𝙖𝙩𝙪𝙨: Private / Unreachable")
        elif info.get("empty"):
            lines.append(f"{index}. ✅ <code>{safe_url}</code>\n   └ 𝙎𝙩𝙖𝙩𝙪𝙨: Public (empty DB)")
        else:
            keys = info.get("keys", [])
            keys_str = ", ".join(f"<code>{html.escape(k)}</code>" for k in keys[:8]) if keys else "—"
            lines.append(
                f"{index}. ✅ <code>{safe_url}</code>\n"
                f"   └ 🟢 𝙊𝙣𝙡𝙞𝙣𝙚 𝘿𝙚𝙫𝙞𝙘𝙚𝙨: <b>{info['online']}</b>\n"
                f"   └ 👥 𝙏𝙤𝙩𝙖𝙡 𝙍𝙚𝙘𝙤𝙧𝙙𝙨: <b>{info['total']}</b>\n"
                f"   └ 🔑 𝙆𝙚𝙮𝙨: {keys_str}"
            )
    return "\n\n".join(lines)


def extract_urls_from_binary(data_bytes: bytes) -> set:
    found = set()
    strings = re.findall(b'[\x20-\x7E]{4,}', data_bytes)
    for s in strings:
        try:
            text = s.decode("utf-8", errors="ignore")
            for match in re.findall(r'https?://[a-zA-Z0-9_.-]+(?:firebaseio\.com|firebasedatabase\.app)', text):
                if "your-project" not in match: found.add(match)
            for domain in re.findall(r'[a-zA-Z0-9_-]+-default-rtdb\.(?:firebaseio\.com|firebasedatabase\.app)', text):
                if not domain.startswith("http"): domain = "https://" + domain
                if "your-project" not in domain: found.add(domain)
        except Exception: pass
    return found


def format_database_list(found_databases):
    return "\n".join(f"{index}. <code>{html.escape(db_url)}</code>" for index, db_url in enumerate(sorted(found_databases), 1))


def extract_firebase_links_from_text(text: str) -> set:
    found = set()
    found.update(re.findall(r'https?://[a-zA-Z0-9_.-]+(?:firebaseio\.com|firebasedatabase\.app)', text))
    for domain in re.findall(r'[a-zA-Z0-9_-]+-default-rtdb\.(?:firebaseio\.com|firebasedatabase\.app)', text):
        found.add(domain if domain.startswith("http") else "https://" + domain)
    return {link for link in found if "your-project" not in link}


def normalize_firebase_urls(raw_text):
    """Extract & normalize Firebase DB URLs from arbitrary text. Returns sorted unique list."""
    links = extract_firebase_links_from_text(raw_text or "")
    normalized = set()
    for url in links:
        u = url.strip().rstrip("/").rstrip(".,;:!?)]}>")
        if not u.startswith("http"): u = "https://" + u
        normalized.add(u)
    return sorted(normalized)


LEGACY_SEED_LINKS = [
    'https://aaaa-b3749-default-rtdb.firebaseio.com',
    'https://adsf-8b4e8-default-rtdb.asia-southeast1.firebasedatabase.app',
    'https://afroar-66af-default-rtdb.firebaseio.com',
]
LEGACY_DUPLICATE_COUNT = 3226
LEGACY_WEBSITE_COUNT = 464
LEGACY_APK_COUNT = 108
LEGACY_LINK_SCANS = 464
LEGACY_APK_SCANS = 108
LEGACY_TOTAL_SCANS = LEGACY_LINK_SCANS + LEGACY_APK_SCANS


def _load_link_store():
    try:
        with open(LINKS_FILE, "r", encoding="utf-8") as file: data = json.load(file)
    except Exception:
        records = []; seen = set()
        for url in LEGACY_SEED_LINKS:
            if url and url not in seen:
                records.append({"url": url, "sources": ["legacy"]}); seen.add(url)
        try:
            with open(LINKS_FILE, "w", encoding="utf-8") as file:
                json.dump({"links": records, "duplicate_count": LEGACY_DUPLICATE_COUNT}, file, ensure_ascii=False)
        except Exception: pass
        return records, LEGACY_DUPLICATE_COUNT
    if isinstance(data, list):
        records = []; seen = set()
        for item in data:
            if isinstance(item, dict):
                url = str(item.get("url", "")); sources = [str(s) for s in item.get("sources", [])]
            else: url = str(item); sources = ["legacy"]
            if url and url not in seen:
                records.append({"url": url, "sources": sources or ["legacy"]}); seen.add(url)
        return records, 0
    if isinstance(data, dict):
        raw_records = data.get("links", [])
        records = []; seen = set()
        for item in raw_records:
            if isinstance(item, dict):
                url = str(item.get("url", "")); sources = [str(s) for s in item.get("sources", [])]
            else: url = str(item); sources = ["legacy"]
            if url and url not in seen:
                records.append({"url": url, "sources": sources or ["legacy"]}); seen.add(url)
        return records, int(data.get("duplicate_count", 0) or 0)
    return [], 0


def _ensure_link_store_locked():
    global LINK_CACHE, LINK_DUPLICATE_COUNT
    if LINK_CACHE is None:
        LINK_CACHE, LINK_DUPLICATE_COUNT = _load_link_store()


def get_saved_links():
    global LINK_CACHE, LINK_DUPLICATE_COUNT
    with LINKS_LOCK:
        _ensure_link_store_locked()
        return [record["url"] for record in LINK_CACHE]


def save_firebase_links(links, source="unknown"):
    global LINK_CACHE, LINK_DUPLICATE_COUNT
    links = [str(link) for link in links if link]
    if not links: return {"new": 0, "duplicates": 0, "total": len(get_saved_links())}
    try:
        with LINKS_LOCK:
            _ensure_link_store_locked()
            by_url = {record["url"]: record for record in LINK_CACHE}
            new_count = 0; duplicate_count = 0
            for link in links:
                if link in by_url:
                    duplicate_count += 1
                    record = by_url[link]
                    if source and source not in record["sources"]: record["sources"].append(source)
                else:
                    record = {"url": link, "sources": [source] if source else ["unknown"]}
                    LINK_CACHE.append(record); by_url[link] = record; new_count += 1
            LINK_DUPLICATE_COUNT += duplicate_count
            temp_links = LINKS_FILE + ".tmp"
            with open(temp_links, "w", encoding="utf-8") as file:
                json.dump({"links": LINK_CACHE, "duplicate_count": LINK_DUPLICATE_COUNT}, file, ensure_ascii=False)
            os.replace(temp_links, LINKS_FILE)
            return {"new": new_count, "duplicates": duplicate_count, "total": len(LINK_CACHE)}
    except Exception:
        return {"new": 0, "duplicates": 0, "total": len(get_saved_links())}


def get_link_collection_stats():
    global LINK_CACHE, LINK_DUPLICATE_COUNT
    with LINKS_LOCK:
        _ensure_link_store_locked()
        website_count = LEGACY_WEBSITE_COUNT + sum("website" in record["sources"] for record in LINK_CACHE)
        apk_count = LEGACY_APK_COUNT + sum("apk" in record["sources"] for record in LINK_CACHE)
        return {"total": len(LINK_CACHE), "duplicates": LINK_DUPLICATE_COUNT, "website": website_count, "apk": apk_count}


def ensure_web_link_store():
    try:
        with open(WEB_LINKS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
        if isinstance(data, list): return data
    except Exception: pass
    return []


def save_web_link(target_url, database_count):
    if not target_url or int(database_count) <= 2: return
    try:
        links = ensure_web_link_store()
        existing = {str(item.get("url")): item for item in links if isinstance(item, dict)}
        if target_url in existing:
            existing[target_url]["database_count"] = max(int(existing[target_url].get("database_count", 0)), int(database_count))
        else: links.append({"url": target_url, "database_count": int(database_count)})
        temp = WEB_LINKS_FILE + ".tmp"
        with open(temp, "w", encoding="utf-8") as file:
            json.dump(links, file, ensure_ascii=False, indent=2)
        os.replace(temp, WEB_LINKS_FILE)
    except Exception: pass


def get_web_link_stats():
    links = ensure_web_link_store()
    return len(links), 0


def write_web_links_file():
    links = ensure_web_link_store()
    output = tempfile.NamedTemporaryFile(prefix="web_links_", suffix=".txt", mode="w", encoding="utf-8", delete=False)
    output_path = output.name
    try:
        output.write("Web Links Collection\n\n")
        for index, item in enumerate(links, 1):
            count = int(item.get("database_count", 0))
            label = "database" if count == 1 else "databases"
            output.write(f"{index}. {item.get('url', '')} ({count} {label})\n")
        output.close(); return output_path
    except Exception:
        output.close(); safe_remove_file(output_path); return None


def extract_firebase_from_apk(file_path: str) -> str:
    found_databases = set()
    try:
        with zipfile.ZipFile(file_path, "r") as apk_zip:
            for filename in apk_zip.namelist():
                try: found_databases.update(extract_urls_from_binary(apk_zip.read(filename)))
                except Exception: pass
        if found_databases:
            body = format_firebase_list_with_analysis(found_databases)
            return (f"📦 <b>APK Scanned Successfully!</b>\n\n"
                    f"<b>Found Firebase Databases ({len(found_databases)}):</b>\n\n{body}")
        return "⚠️ <b>No Firebase database URL could be resolved from this APK.</b>"
    except Exception as error:
        return f"❌ <b>Error processing APK:</b> <code>{html.escape(str(error))}</code>"


def extract_firebase_from_url(target_url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 14; Mobile) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36"}
    try:
        if not target_url.startswith("http"): target_url = "https://" + target_url
        found_databases = set()
        parsed_url = urllib.parse.urlparse(target_url)
        for values in urllib.parse.parse_qs(parsed_url.query).values():
            for value in values:
                try:
                    padding = "=" * (-len(value) % 4)
                    decoded = base64.b64decode(value + padding).decode("utf-8", errors="ignore")
                    found_databases.update(extract_urls_from_binary(decoded.encode()))
                except Exception: pass
                found_databases.update(extract_urls_from_binary(value.encode()))
        response = requests.get(target_url, headers=headers, timeout=15, allow_redirects=True)
        found_databases.update(extract_urls_from_binary(response.content))
        for js in re.findall(r'src=["\']([^"\']+\.js[^"\']*)["\']', response.text):
            try:
                js_response = requests.get(urllib.parse.urljoin(target_url, js), headers=headers, timeout=10)
                found_databases.update(extract_urls_from_binary(js_response.content))
            except Exception: pass
        if found_databases:
            body = format_firebase_list_with_analysis(found_databases)
            return (f"🌐 <b>Website Scan Successfully!</b>\n"
                    f"🌐 Target: <code>{html.escape(target_url)}</code>\n\n"
                    f"<b>Found Databases ({len(found_databases)}):</b>\n\n{body}")
        return f"⚠️ <b>Scan Result:</b> No Firebase database URL found for <code>{html.escape(target_url)}</code>"
    except Exception as error:
        return f"❌ <b>Error:</b> <code>{html.escape(str(error))}</code>"


def download_telegram_file(file_id: str, suffix=".apk", prefix="firebase_apk_"):
    try:
        file_info = telegram_call("getFile", {"file_id": file_id}, timeout=10)
        file_path_info = (file_info or {}).get("file_path")
        if not file_path_info: return None
        download_url = f"https://api.telegram.org/file/bot{TG_TOKEN}/{file_path_info}"
        temp_file = tempfile.NamedTemporaryFile(prefix=prefix, suffix=suffix, delete=False)
        temp_apk = temp_file.name
        try:
            with TELEGRAM_SESSION.get(download_url, stream=True, timeout=40) as file_response:
                file_response.raise_for_status()
                for chunk in file_response.iter_content(chunk_size=1024 * 64):
                    if chunk: temp_file.write(chunk)
            temp_file.close(); return temp_apk
        except Exception:
            temp_file.close()
            try: os.remove(temp_apk)
            except Exception: pass
            return None
    except Exception: return None


def send_document(chat_id, file_path, caption=""):
    try:
        with open(file_path, "rb") as file:
            response = TELEGRAM_SESSION.post(f"{TG_GATEWAY}/sendDocument",
                data={"chat_id": str(chat_id), "caption": caption, "parse_mode": "HTML"},
                files={"document": file}, timeout=30)
        data = response.json()
        return data.get("result") if response.status_code == 200 and data.get("ok") else None
    except Exception: return None


def send_firebase_links_collection(chat_id):
    links = get_saved_links()
    stats = get_link_collection_stats()
    heading = ("📦 <b>Firebase Links Collection</b>\n\n"
               f"🔢 <b>Total Unique Links: {stats['total']}</b>\n"
               f"♻️ <b>Duplicate Links: {stats['duplicates']}</b>\n"
               f"🌐 <b>Website Links: {stats['website']}</b>\n"
               f"📱 <b>APK Links: {stats['apk']}</b>")
    if not links: return send_message(chat_id, heading + "\n\nNo Firebase links have been collected yet.")
    direct_body = heading + "\n\n" + format_database_list(links)
    if len(direct_body) <= 3800: return send_message(chat_id, direct_body)
    temp_txt = tempfile.NamedTemporaryFile(prefix="firebase_links_", suffix=".txt", mode="w", encoding="utf-8", delete=False)
    txt_path = temp_txt.name
    try:
        temp_txt.write(f"Firebase Links Collection\n\nTotal: {stats['total']}\nDuplicates: {stats['duplicates']}\nWebsite: {stats['website']}\nAPK: {stats['apk']}\n\n")
        for index, link in enumerate(links, 1): temp_txt.write(f"{index}. {link}\n")
        temp_txt.close()
        return send_document(chat_id, txt_path, caption=heading)
    finally:
        try: os.remove(txt_path)
        except Exception: pass


def channel_is_joined(user_id, channel_id):
    member = telegram_call("getChatMember", {"chat_id": channel_id, "user_id": user_id}, timeout=12)
    if not member: return False
    status = member.get("status")
    return status in {"creator", "administrator", "member"} or (status == "restricted" and bool(member.get("is_member")))


def get_missing_channels(user_id):
    return [ch for ch in FORCE_JOIN_CHANNELS if not channel_is_joined(user_id, ch["chat_id"])]


def join_keyboard(missing_channels):
    return {"inline_keyboard": [[{"text": f"📢 {ch['label']}", "url": ch["join_url"], "style": "primary"} for ch in missing_channels]]}


def reply_keyboard(button_text, style="success"):
    return {"keyboard": [[{"text": button_text, "style": style}]], "resize_keyboard": True, "is_persistent": True}


def force_join_message(user_id):
    missing_channels = get_missing_channels(user_id)
    if not missing_channels: return False
    send_message(user_id, "⚠️ ᴘʟᴇᴀꜱᴇ ᴊᴏɪɴ ᴛʜᴇ ꜰᴏʟʟᴏᴡɪɴɢ ᴛᴏ ᴜꜱᴇ ᴛʜɪꜱ ʙᴏᴛ\n\nᴀꜰᴛᴇʀ ᴊᴏɪɴɪɴɢ, ᴘʀᴇꜱꜱ ✅ ᴠᴇʀɪꜰʏ", reply_markup=join_keyboard(missing_channels))
    send_message(user_id, "✅ Verify", reply_markup=reply_keyboard("✅ Verify", "success"))
    return True


def welcome_message(user):
    state = get_user_state(user["id"], user)
    joined = ist_datetime(state["created_at"])
    send_message(user["id"],
        f"╔═══════════════════════╗\n"
        f"🔥 <b>{BOT_BRAND}</b> 🔥\n"
        f"╚═══════════════════════╝\n\n"
        f"👋 𝙒𝙀𝙇𝘾𝙊𝙈𝙀, <code>{html.escape((user.get('first_name') or 'User').strip())}</code> 💫\n\n"
        f"👤 𝙐𝙎𝙀𝙍 𝙉𝘼𝙈𝙀: <code>@{html.escape(user.get('username') or 'user')}</code>\n"
        f"🆔 𝙐𝙎𝙀𝙍 𝙄𝘿: <code>{user['id']}</code>\n"
        f"📅 𝙅𝙊𝙄𝙉𝙀𝘿: <code>{joined}</code>\n"
        f"🎁 𝘼𝘾𝘾𝙀𝙎𝙎: <b>FREE UNLIMITED</b>\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "👇 𝘾𝙃𝙊𝙊𝙎𝙀 𝘼𝙉 𝙊𝙋𝙏𝙄𝙊𝙉 𝘽𝙀𝙇𝙊𝙒\n"
        "━━━━━━━━━━━━━━━━━━━━",
        reply_markup=main_keyboard())


def set_website_mode(chat_id):
    with WEBSITE_MODE_LOCK: WEBSITE_MODE_USERS.add(int(chat_id))

def clear_website_mode(chat_id):
    with WEBSITE_MODE_LOCK: WEBSITE_MODE_USERS.discard(int(chat_id))

def is_website_mode(chat_id):
    with WEBSITE_MODE_LOCK: return int(chat_id) in WEBSITE_MODE_USERS


def extract_website_urls_from_text(text, limit=None):
    url_pattern = re.compile(r"https?://[^\s<>\"']+", re.IGNORECASE)
    urls = []; seen = set()
    for raw_url in url_pattern.findall(text or ""):
        url = raw_url.rstrip(".,;:!?)]}>")
        if not url or url in seen: continue
        seen.add(url); urls.append(url)
        if limit is not None and len(urls) >= limit: break
    return urls


def user_display_name(user):
    return html.escape(" ".join(part for part in [user.get("first_name", ""), user.get("last_name", "")] if part) or "Unknown User")


def admin_scan_message(user, file_name, scan_result):
    return (f"📥 <b>New APK Scan Result</b>\n\n"
            f"👤 User: {user_display_name(user)}\n"
            f"🆔 User ID: <code>{user.get('id')}</code>\n"
            f"📄 File: <code>{html.escape(file_name or 'unknown.apk')}</code>\n\n{scan_result}")


def admin_website_message(user, scan_result):
    return (f"🌐 <b>New Website Scan Result</b>\n\n"
            f"👤 User: {user_display_name(user)}\n"
            f"🆔 User ID: <code>{user.get('id')}</code>\n\n{scan_result}")


def send_message_reliably(chat_id, text, reply_markup=None, attempts=3):
    for attempt in range(attempts):
        result = send_message(chat_id, text, reply_markup=reply_markup)
        if result: return result
        if attempt + 1 < attempts: time.sleep(0.5 * (attempt + 1))
    return None


def combine_website_results(results):
    cleaned_results = []
    success_heading = "🌐 <b>Website Scan Successfully!</b>\n"
    for index, result in enumerate(results, 1):
        if result.startswith(success_heading): result = result[len(success_heading):]
        cleaned_results.append(f"🌐 <b>Website {index}</b>\n{result}")
    return success_heading + "\n" + "\n\n".join(cleaned_results)


def process_website_urls(user, chat_id, website_urls, separate_messages=False):
    results = []
    for website_url in website_urls:
        result_text = extract_firebase_from_url(website_url)
        count_match = re.search(r"Found Databases \((\d+)\)", result_text)
        save_web_link(website_url, int(count_match.group(1)) if count_match else 0)
        save_firebase_links(extract_firebase_links_from_text(result_text), source="website")
        results.append(result_text)
    if separate_messages:
        for result_text in results:
            send_message_reliably(chat_id, result_text, reply_markup=main_keyboard())
            send_message_reliably(ADMIN_ID, admin_website_message(user, result_text))
            time.sleep(0.05)
        return
    combined_result = combine_website_results(results)
    send_message_reliably(chat_id, combined_result, reply_markup=main_keyboard())
    send_message_reliably(ADMIN_ID, admin_website_message(user, combined_result))


# ═══════════════════════════════════════════════════════════════
# BULK APK SCAN
# ═══════════════════════════════════════════════════════════════
def process_bulk_apks(user, chat_id, files):
    total = len(files); scanned_ok = 0
    send_message(chat_id, f"🚀 <b>Bulk scan started for {total} APK(s)...</b>", reply_markup=main_keyboard())
    for index, (file_id, file_name) in enumerate(files, 1):
        try:
            send_message(chat_id, f"📦 <b>[{index}/{total}]</b> Scanning <code>{html.escape(file_name)}</code>...")
            local_apk = download_telegram_file(file_id)
            if not local_apk:
                send_message(chat_id, f"❌ Failed to download <code>{html.escape(file_name)}</code>"); continue
            try:
                update_scan_stat("apk")
                scan_result = extract_firebase_from_apk(local_apk)
                save_firebase_links(extract_firebase_links_from_text(scan_result), source="apk")
                send_message(chat_id, f"📄 <b>{html.escape(file_name)}</b>\n\n{scan_result}", reply_markup=main_keyboard())
                send_message(ADMIN_ID, admin_scan_message(user, file_name, scan_result))
                scanned_ok += 1
            finally: safe_remove_file(local_apk)
        except Exception as e:
            send_message(chat_id, f"❌ Error scanning <code>{html.escape(file_name)}</code>: <code>{html.escape(str(e))}</code>")
    send_message(chat_id, f"✅ <b>Bulk scan complete!</b>\nScanned: <b>{scanned_ok}/{total}</b>", reply_markup=main_keyboard())


# ═══════════════════════════════════════════════════════════════
# FB FILTER (user-provided links only)
# ═══════════════════════════════════════════════════════════════
def _filter_report_lines(matches, min_online, links_count):
    header = (f"🎯 <b>FB FILTER RESULT</b>\n\n"
              f"📥 𝙎𝙘𝙖𝙣𝙣𝙚𝙙: <b>{links_count}</b>\n"
              f"🎚️ 𝙈𝙞𝙣 𝙊𝙣𝙡𝙞𝙣𝙚: <b>{min_online}</b>\n"
              f"✅ 𝙈𝙖𝙩𝙘𝙝𝙚𝙨: <b>{len(matches)}</b>\n"
              "━━━━━━━━━━━━━━━━━━\n\n")
    body = "\n".join(
        f"{i}. <code>{html.escape(db)}</code>  ({online} online devices)"
        for i, (db, online) in enumerate(matches, 1)
    )
    return header, body


def _send_filter_report(chat_id, matches, min_online, links_count, reply_markup):
    header, body = _filter_report_lines(matches, min_online, links_count)
    full = header + body
    if len(full) <= 4000:
        send_message(chat_id, full, reply_markup=reply_markup); return
    try:
        tmp = tempfile.NamedTemporaryFile(prefix="fb_filter_", suffix=".txt", mode="w", encoding="utf-8", delete=False)
        tmp.write("FB FILTER RESULT\n")
        tmp.write(f"Scanned: {links_count}\nMin Online: {min_online}\nMatches: {len(matches)}\n\n")
        for i, (db, online) in enumerate(matches, 1):
            tmp.write(f"{i}. {db}  ({online} online devices)\n")
        tmp.close()
        try:
            send_document(chat_id, tmp.name, caption=f"🎯 <b>FB Filter Result</b>\nScanned: {links_count} | Min: {min_online} | Matches: {len(matches)}")
        finally: safe_remove_file(tmp.name)
    except Exception: pass
    send_message(chat_id, "📄 Full result sent as file above.", reply_markup=reply_markup)


def run_fb_filter(user, chat_id, links, min_online):
    links = list(dict.fromkeys(links))[:MAX_FILTER_LINKS]
    if not links:
        msg = "⚠️ 𝙉𝙤 𝙁𝙞𝙧𝙚𝙗𝙖𝙨𝙚 𝙡𝙞𝙣𝙠𝙨 𝙥𝙧𝙤𝙫𝙞𝙙𝙚𝙙."
        send_message(chat_id, msg, reply_markup=main_keyboard())
        send_message(ADMIN_ID, f"🎯 <b>FB Filter Result</b>\n👤 {user_display_name(user)} | <code>{chat_id}</code>\n\n{msg}", reply_markup=admin_keyboard())
        return

    send_message(chat_id, f"🎯 𝘼𝙣𝙖𝙡𝙮𝙯𝙞𝙣𝙜 <b>{len(links)}</b> 𝘿𝘽𝙨...\n⏱️ 𝙏𝙝𝙞𝙨 𝙢𝙖𝙮 𝙩𝙖𝙠𝙚 𝙖 𝙬𝙝𝙞𝙡𝙚.", reply_markup=main_keyboard())

    results = analyze_databases_parallel(links)

    matches = []
    for db, info in results.items():
        if not info or info.get("empty"): continue
        online = int(info.get("online", 0))
        if online >= min_online:
            matches.append((db, online))
    matches.sort(key=lambda x: x[1], reverse=True)

    if not matches:
        header = (f"🎯 <b>FB FILTER RESULT</b>\n\n"
                  f"📥 𝙎𝙘𝙖𝙣𝙣𝙚𝙙: <b>{len(links)}</b>\n"
                  f"🎚️ 𝙈𝙞𝙣 𝙊𝙣𝙡𝙞𝙣𝙚: <b>{min_online}</b>\n"
                  f"✅ 𝙈𝙖𝙩𝙘𝙝𝙚𝙨: <b>0</b>\n\n"
                  f"❌ No database matched with <b>{min_online}+</b> online devices.")
        send_message(chat_id, header, reply_markup=main_keyboard())
        send_message(ADMIN_ID,
            f"🎯 <b>FB Filter Result</b>\n👤 {user_display_name(user)} | <code>{chat_id}</code>\n\n{header}",
            reply_markup=admin_keyboard())
        return

    _send_filter_report(chat_id, matches, min_online, len(links), main_keyboard())

    admin_header, admin_body = _filter_report_lines(matches, min_online, len(links))
    admin_prefix = (f"🎯 <b>FB Filter Result</b>\n"
                    f"👤 {user_display_name(user)} | <code>{chat_id}</code>\n\n")
    admin_full = admin_prefix + admin_header + admin_body
    if len(admin_full) <= 4000:
        send_message(ADMIN_ID, admin_full, reply_markup=admin_keyboard())
    else:
        try:
            tmp = tempfile.NamedTemporaryFile(prefix="fb_filter_admin_", suffix=".txt", mode="w", encoding="utf-8", delete=False)
            tmp.write(f"FB FILTER RESULT\nUser: {user_display_name(user)} ({chat_id})\nScanned: {len(links)}\nMin Online: {min_online}\nMatches: {len(matches)}\n\n")
            for i, (db, online) in enumerate(matches, 1):
                tmp.write(f"{i}. {db}  ({online} online devices)\n")
            tmp.close()
            try:
                send_document(ADMIN_ID, tmp.name, caption=f"🎯 <b>FB Filter Result</b>\n👤 <code>{chat_id}</code> | Scanned: {len(links)} | Min: {min_online} | Matches: {len(matches)}")
            finally: safe_remove_file(tmp.name)
        except Exception: pass


# ═══════════════════════════════════════════════════════════════
# WEBSITE BATCH
# ═══════════════════════════════════════════════════════════════
def launch_website_batch(job_id, user, chat_id):
    with BATCH_TASKS_LOCK:
        existing_task = BATCH_TASKS.get(job_id)
        if existing_task and not existing_task.done(): return
        BATCH_TASKS[job_id] = BATCH_EXECUTOR.submit(run_website_batch, job_id, user, chat_id)


def run_website_batch(job_id, user, chat_id):
    try:
        while True:
            batch = get_batch(job_id); item = get_pending_batch_item(job_id)
            if not batch or not item: break
            if batch.get("status") == "cancelled": break
            item_index = int(item["item_index"]); website_url = item["website_url"]
            with sqlite3.connect(BATCH_DB_FILE) as connection:
                connection.execute("UPDATE website_batch_items SET status='processing', error_text=NULL WHERE job_id=? AND item_index=?", (job_id, item_index))
                connection.execute("UPDATE website_batches SET status='running', updated_at=? WHERE job_id=?", (time.time(), job_id))
                connection.commit()
            try:
                result_text = extract_firebase_from_url(website_url)
                count_match = re.search(r"Found Databases \((\d+)\)", result_text)
                save_web_link(website_url, int(count_match.group(1)) if count_match else 0)
                save_firebase_links(extract_firebase_links_from_text(result_text), source="website")
                user_result = send_message_reliably(chat_id, result_text, reply_markup=main_keyboard())
                admin_result = send_message_reliably(ADMIN_ID, admin_website_message(user, result_text))
                if user_result and admin_result:
                    mark_batch_item(job_id, item_index, "sent", result_text=result_text)
                else:
                    mark_batch_item(job_id, item_index, "failed", result_text=result_text, error_text="Telegram delivery failed")
            except Exception as error:
                error_text = f"❌ <b>Error:</b> <code>{html.escape(str(error))}</code>"
                send_message_reliably(chat_id, error_text, reply_markup=main_keyboard())
                send_message_reliably(ADMIN_ID, admin_website_message(user, error_text))
                mark_batch_item(job_id, item_index, "failed", result_text=error_text, error_text=str(error))
            update_batch_progress(job_id, status="running")
            time.sleep(WEBSITE_BATCH_DELAY)
        batch = get_batch(job_id)
        if batch and batch.get("status") != "cancelled":
            mark_batch_status(job_id, "completed"); update_batch_progress(job_id, status="completed"); send_batch_result_file(job_id)
        elif batch: update_batch_progress(job_id, status="cancelled")
    finally:
        with BATCH_TASKS_LOCK: BATCH_TASKS.pop(job_id, None)


def resume_website_batches():
    for job_id in get_resumable_batch_ids():
        batch = get_batch(job_id)
        if batch:
            user = {"id": batch["user_id"], "first_name": "User", "last_name": ""}
            launch_website_batch(job_id, user, batch["user_id"])


def broadcast_to_users(text, cancel_event=None):
    users = get_users(); sent = 0; failed = 0
    for chat_id in users:
        if cancel_event is not None and cancel_event.is_set(): break
        if send_message(chat_id, text): sent += 1
        else: failed += 1
    return sent, failed


def run_broadcast(text, admin_chat_id):
    sent, failed = broadcast_to_users(text, BROADCAST_CANCEL_EVENT)
    if not BROADCAST_CANCEL_EVENT.is_set():
        send_message(admin_chat_id, f"✅ <b>Broadcast sent to {sent} users.</b>\n❌ <b>Failed: {failed} users.</b>", reply_markup=admin_keyboard())


def get_chat_lock(chat_id):
    with CHAT_LOCKS_LOCK:
        if chat_id not in CHAT_LOCKS: CHAT_LOCKS[chat_id] = threading.Lock()
        return CHAT_LOCKS[chat_id]


def get_admin_broadcast_mode():
    with ADMIN_STATE_LOCK: return ADMIN_BROADCAST_MODE


def set_admin_broadcast_mode(value):
    global ADMIN_BROADCAST_MODE
    with ADMIN_STATE_LOCK: ADMIN_BROADCAST_MODE = value


# ═══════════════════════════════════════════════════════════════
# UPDATE HANDLER
# ═══════════════════════════════════════════════════════════════
def process_update(update):
    if "callback_query" in update:
        callback = update["callback_query"]
        msg = callback.get("message") or {}; chat = msg.get("chat") or {}
        chat_id = chat.get("id")
        if chat_id is None: return
        user = msg.get("from") or {}; user["id"] = chat_id
        save_user(chat_id); get_user_state(chat_id, user)
        data = callback.get("data", "")
        telegram_call("answerCallbackQuery", {"callback_query_id": callback.get("id")}, timeout=10)
        with get_chat_lock(chat_id):
            if data == "user_back": welcome_message(user)
            elif data == "admin_back": send_message(chat_id, get_admin_panel_text(), reply_markup=admin_keyboard())
            elif data == "manage_firebase": send_firebase_links_collection(chat_id)
            elif data == "manage_web": send_web_links_collection(chat_id)
        return

    if "message" not in update: return
    message = update["message"]
    chat_id = message["chat"]["id"]
    with get_chat_lock(chat_id):
        user = message.get("from", {}); user["id"] = chat_id
        save_user(chat_id); get_user_state(chat_id, user)

        if "text" in message:
            text = message["text"].strip()

            if text in ("🔙 𝘽𝘼𝘾𝙆", "🔙 BACK"):
                clear_website_mode(chat_id); set_bulk_mode(chat_id, False); clear_filter(chat_id)
                if chat_id == ADMIN_ID: send_message(chat_id, get_admin_panel_text(), reply_markup=admin_keyboard())
                else: welcome_message(user)
                return

            if text in ("❌ 𝘾𝘼𝙉𝘾𝙀𝙇", "❌ CANCEL", "❌ Cancel", "❌ Cancel Broadcast"):
                clear_website_mode(chat_id); set_bulk_mode(chat_id, False); clear_filter(chat_id)
                was_broadcasting = get_admin_broadcast_mode()
                set_admin_broadcast_mode(False); BROADCAST_CANCEL_EVENT.set()
                if chat_id == ADMIN_ID and was_broadcasting:
                    send_message(chat_id, "↩️ 𝘾𝙖𝙣𝙘𝙚𝙡𝙡𝙚𝙙.", reply_markup=admin_keyboard())
                else:
                    send_message(chat_id, "↩️ 𝘾𝙖𝙣𝙘𝙚𝙡𝙡𝙚𝙙.", reply_markup=main_keyboard())
                return

            if chat_id == ADMIN_ID and text in ("🔥 𝙂𝙀𝙏 𝙁𝙄𝙍𝙀𝘽𝘼𝙎𝙀 𝙇𝙄𝙉𝙆𝙎", "🔥 GET FIREBASE LINKS", "🔗 Get Firebase Links"):
                send_firebase_links_collection(chat_id); return
            if chat_id == ADMIN_ID and text in ("🌐 𝙒𝙀𝘽 𝙇𝙄𝙉𝙆𝙎", "🌐 WEB LINKS"):
                send_web_links_collection(chat_id); return

            if text.startswith("/start"):
                if force_join_message(chat_id): return
                welcome_message(user); return

            if chat_id == ADMIN_ID and text == "/admin":
                set_admin_broadcast_mode(False)
                send_message(chat_id, get_admin_panel_text(), reply_markup=admin_keyboard()); return
            if chat_id == ADMIN_ID and text in ("📢 Broadcast", "📢 𝘽𝙍𝙊𝘼𝘿𝘾𝘼𝙎𝙏"):
                set_admin_broadcast_mode(True); BROADCAST_CANCEL_EVENT.clear()
                send_message(chat_id, "📢 𝘽𝙍𝙊𝘼𝘿𝘾𝘼𝙎𝙏 𝙈𝙊𝘿𝙀\n\n𝙎𝙚𝙣𝙙 𝙩𝙝𝙚 𝙢𝙚𝙨𝙨𝙖𝙜𝙚 𝙩𝙤 𝙗𝙧𝙤𝙖𝙙𝙘𝙖𝙨𝙩.", reply_markup=reply_keyboard("❌ 𝘾𝘼𝙉𝘾𝙀𝙇", "danger")); return
            if chat_id == ADMIN_ID and text in ("❌ Cancel Broadcast", "❌ 𝘾𝘼𝙉𝘾𝙀𝙇"):
                set_admin_broadcast_mode(False); BROADCAST_CANCEL_EVENT.set()
                send_message(chat_id, "❌ 𝘽𝙧𝙤𝙖𝙙𝙘𝙖𝙨𝙩 𝙘𝙖𝙣𝙘𝙚𝙡𝙡𝙚𝙙.", reply_markup=admin_keyboard()); return
            if chat_id == ADMIN_ID and text in ("🔗 𝙈𝘼𝙉𝘼𝙂𝙀 𝙇𝙄𝙉𝙆𝙎", "🔗 Manage Links"):
                manage_links_screen(chat_id); return
            if chat_id == ADMIN_ID and get_admin_broadcast_mode():
                set_admin_broadcast_mode(False)
                UPDATE_EXECUTOR.submit(run_broadcast, text, chat_id)
                send_message(chat_id, "📤 𝘽𝙧𝙤𝙖𝙙𝙘𝙖𝙨𝙩 𝙨𝙩𝙖𝙧𝙩𝙚𝙙 𝙞𝙣 𝙗𝙖𝙘𝙠𝙜𝙧𝙤𝙪𝙣𝙙.", reply_markup=admin_keyboard()); return

            if text in ("✅ Verify", "✅ 𝙑𝙀𝙍𝙄𝙁𝙔"):
                clear_website_mode(chat_id); set_bulk_mode(chat_id, False); clear_filter(chat_id)
                if force_join_message(chat_id): return
                send_message(chat_id, "✅ <b>Verification successful!</b>", reply_markup=main_keyboard()); return

            # ═══════ FB FILTER — handle typed input first ═══════
            if is_filter_mode(chat_id):
                st = get_filter_state(chat_id) or {}
                step = st.get("step")
                if step == "links":
                    urls = normalize_firebase_urls(text)
                    if not urls:
                        send_message(chat_id,
                            "❌ 𝙉𝙤 𝙫𝙖𝙡𝙞𝙙 𝙁𝙞𝙧𝙚𝙗𝙖𝙨𝙚 𝙐𝙍𝙇 𝙛𝙤𝙪𝙣𝙙 𝙞𝙣 𝙮𝙤𝙪𝙧 𝙢𝙚𝙨𝙨𝙖𝙜𝙚.\n\n"
                            "𝙋𝙡𝙚𝙖𝙨𝙚 𝙥𝙖𝙨𝙩𝙚 𝙁𝙞𝙧𝙚𝙗𝙖𝙨𝙚 𝘿𝘽 𝙡𝙞𝙣𝙠𝙨 (𝙤𝙣𝙚 𝙥𝙚𝙧 𝙡𝙞𝙣𝙚) 𝙤𝙧 𝙪𝙥𝙡𝙤𝙖𝙙 𝙖 .𝙩𝙭𝙩 𝙛𝙞𝙡𝙚.",
                            reply_markup=reply_keyboard("❌ 𝘾𝘼𝙉𝘾𝙀𝙇", "danger"))
                        return
                    set_filter_step(chat_id, "min", links=urls)
                    send_message(chat_id,
                        f"✅ 𝙍𝙚𝙘𝙚𝙞𝙫𝙚𝙙 <b>{len(urls)}</b> 𝙁𝙞𝙧𝙚𝙗𝙖𝙨𝙚 𝙡𝙞𝙣𝙠(s).\n\n"
                        f"🎚️ 𝙉𝙤𝙬 𝙚𝙣𝙩𝙚𝙧 𝙩𝙝𝙚 <b>𝙢𝙞𝙣𝙞𝙢𝙪𝙢 𝙤𝙣𝙡𝙞𝙣𝙚 𝙙𝙚𝙫𝙞𝙘𝙚𝙨</b> 𝙘𝙤𝙪𝙣𝙩.\n"
                        f"📌 𝙀𝙭𝙖𝙢𝙥𝙡𝙚: <code>5</code>",
                        reply_markup=reply_keyboard("❌ 𝘾𝘼𝙉𝘾𝙀𝙇", "danger"))
                    return
                if step == "min":
                    try:
                        min_online = int(text.strip())
                        if min_online < 0: raise ValueError
                    except ValueError:
                        send_message(chat_id, "❌ 𝙄𝙣𝙫𝙖𝙡𝙞𝙙 𝙣𝙪𝙢𝙗𝙚𝙧. 𝙎𝙚𝙣𝙙 𝙖 𝙥𝙤𝙨𝙞𝙩𝙞𝙫𝙚 𝙞𝙣𝙩𝙚𝙜𝙚𝙧.", reply_markup=reply_keyboard("❌ 𝘾𝘼𝙉𝘾𝙀𝙇", "danger"))
                        return
                    links = st.get("links", [])
                    clear_filter(chat_id)
                    HEAVY_EXECUTOR.submit(run_fb_filter, user, chat_id, links, min_online)
                    return

            # ── MAIN MENU ──────────────────────────────────
            if text in ("📤 𝙐𝙋𝙇𝙊𝘼𝘿 𝘼𝙋𝙆", "📤 Upload APK"):
                clear_website_mode(chat_id); set_bulk_mode(chat_id, False)
                send_message(chat_id, "📤 <b>Please send the APK file.</b>", reply_markup=reply_keyboard("❌ 𝘾𝘼𝙉𝘾𝙀𝙇", "danger")); return

            if text in ("🌐 𝙎𝘾𝘼𝙉 𝙒𝙀𝘽𝙎𝙄𝙏𝙀", "🌐 Scan Website"):
                set_bulk_mode(chat_id, False)
                set_website_mode(chat_id)
                send_message(chat_id, "🌐 <b>Please send up to 5 website links, one per line.</b>", reply_markup=reply_keyboard("❌ 𝘾𝘼𝙉𝘾𝙀𝙇", "danger")); return

            if text in ("📦 𝘽𝙐𝙇𝙆 𝙎𝘾𝘼𝙉", "📦 BULK SCAN"):
                clear_website_mode(chat_id)
                set_bulk_mode(chat_id, True)
                send_message(chat_id,
                    "📦 𝘽𝙐𝙇𝙆 𝙎𝘾𝘼𝙉 𝙈𝙊𝘿𝙀\n\n"
                    "𝙎𝙚𝙣𝙙 𝙢𝙪𝙡𝙩𝙞𝙥𝙡𝙚 <b>.apk</b> 𝙛𝙞𝙡𝙚𝙨 𝙤𝙣𝙚 𝙗𝙮 𝙤𝙣𝙚.\n"
                    "𝙒𝙝𝙚𝙣 𝙙𝙤𝙣𝙚, 𝙥𝙧𝙚𝙨𝙨 ✅ 𝙎𝘾𝘼𝙉 𝘼𝙇𝙇.",
                    reply_markup=bulk_scan_keyboard()); return

            if text in ("✅ 𝙎𝘾𝘼𝙉 𝘼𝙇𝙇", "✅ SCAN ALL"):
                files = get_bulk_files(chat_id)
                set_bulk_mode(chat_id, False)
                if not files:
                    send_message(chat_id, "⚠️ 𝙉𝙤 𝘼𝙋𝙆 𝙛𝙞𝙡𝙚𝙨 𝙦𝙪𝙚𝙪𝙚𝙙.", reply_markup=main_keyboard()); return
                HEAVY_EXECUTOR.submit(process_bulk_apks, user, chat_id, files); return

            if text in ("🎯 𝙁𝘽 𝙁𝙄𝙇𝙏𝙀𝙍", "🎯 FB FILTER"):
                set_bulk_mode(chat_id, False); clear_website_mode(chat_id)
                start_filter(chat_id)
                send_message(chat_id,
                    "🎯 𝙁𝘽 𝙁𝙄𝙇𝙏𝙀𝙍\n"
                    "━━━━━━━━━━━━━━━━━━━━\n\n"
                    "📥 𝙎𝙚𝙣𝙙 𝙮𝙤𝙪𝙧 <b>𝙁𝙞𝙧𝙚𝙗𝙖𝙨𝙚 𝘿𝘽 𝙡𝙞𝙣𝙠𝙨</b>:\n"
                    "• 𝙋𝙖𝙨𝙩𝙚 𝙡𝙞𝙣𝙠𝙨 (𝙤𝙣𝙚 𝙥𝙚𝙧 𝙡𝙞𝙣𝙚) 𝙞𝙣 𝙖 𝙢𝙚𝙨𝙨𝙖𝙜𝙚, 𝙤𝙧\n"
                    "• 𝙐𝙥𝙡𝙤𝙖𝙙 𝙖 <b>.𝙩𝙭𝙩</b> 𝙛𝙞𝙡𝙚 𝙘𝙤𝙣𝙩𝙖𝙞𝙣𝙞𝙣𝙜 𝙩𝙝𝙚 𝙡𝙞𝙣𝙠𝙨.",
                    reply_markup=reply_keyboard("❌ 𝘾𝘼𝙉𝘾𝙀𝙇", "danger"))
                return

            if is_website_mode(chat_id):
                clear_website_mode(chat_id)
                website_urls = [line.strip() for line in text.splitlines() if line.strip()][:5]
                if website_urls:
                    update_scan_stat("link")
                    process_website_urls(user, chat_id, website_urls, separate_messages=False)
                return

            if force_join_message(chat_id): return

            website_urls = extract_website_urls_from_text(text, MAX_DIRECT_WEBSITE_URLS)
            if website_urls:
                send_message(chat_id, "⏳ Mining target data...")
                update_scan_stat("link")
                process_website_urls(user, chat_id, website_urls, separate_messages=False); return
            send_message(chat_id, "⏳ Mining target data...")
            result_text = extract_firebase_from_url(text)
            count_match = re.search(r"Found Databases \((\d+)\)", result_text)
            save_web_link(text, int(count_match.group(1)) if count_match else 0)
            save_firebase_links(extract_firebase_links_from_text(result_text), source="website")
            send_message(chat_id, result_text, reply_markup=main_keyboard()); return

        if "document" in message or "audio" in message:
            if force_join_message(chat_id): return
            document = message.get("document") or message.get("audio")
            file_name = document.get("file_name", "")
            mime_type = document.get("mime_type", "")
            is_txt = file_name.lower().endswith(".txt") or mime_type.startswith("text/")
            is_apk = file_name.lower().endswith(".apk") or mime_type == "application/vnd.android.package-archive"

            # ── FB FILTER: .txt of links ─────────────
            if is_filter_mode(chat_id):
                st = get_filter_state(chat_id) or {}
                if st.get("step") == "links" and is_txt:
                    send_message(chat_id, "📄 <b>Reading your .txt file...</b>")
                    local_txt = download_telegram_file(document["file_id"], suffix=".txt", prefix="fb_filter_")
                    if not local_txt:
                        send_message(chat_id, "❌ Failed to download file.", reply_markup=reply_keyboard("❌ 𝘾𝘼𝙉𝘾𝙀𝙇", "danger")); return
                    try:
                        with open(local_txt, "r", encoding="utf-8", errors="ignore") as file:
                            file_text = file.read(5 * 1024 * 1024)
                    finally:
                        safe_remove_file(local_txt)
                    urls = normalize_firebase_urls(file_text)
                    if not urls:
                        send_message(chat_id,
                            "❌ 𝙉𝙤 𝙁𝙞𝙧𝙚𝙗𝙖𝙨𝙚 𝙪𝙧𝙡𝙨 𝙛𝙤𝙪𝙣𝙙 𝙞𝙣 𝙛𝙞𝙡𝙚. 𝙏𝙧𝙮 𝙖𝙜𝙖𝙞𝙣 𝙤𝙧 𝙥𝙖𝙨𝙩𝙚 𝙡𝙞𝙣𝙠𝙨 𝙞𝙣 𝙩𝙚𝙭𝙩.",
                            reply_markup=reply_keyboard("❌ 𝘾𝘼𝙉𝘾𝙀𝙇", "danger"))
                        return
                    set_filter_step(chat_id, "min", links=urls)
                    send_message(chat_id,
                        f"✅ 𝙍𝙚𝙘𝙚𝙞𝙫𝙚𝙙 <b>{len(urls)}</b> 𝙁𝙞𝙧𝙚𝙗𝙖𝙨𝙚 𝙡𝙞𝙣𝙠(s) 𝙛𝙧𝙤𝙢 𝙛𝙞𝙡𝙚.\n\n"
                        f"🎚️ 𝙉𝙤𝙬 𝙚𝙣𝙩𝙚𝙧 𝙩𝙝𝙚 <b>𝙢𝙞𝙣𝙞𝙢𝙪𝙢 𝙤𝙣𝙡𝙞𝙣𝙚 𝙙𝙚𝙫𝙞𝙘𝙚𝙨</b> 𝙘𝙤𝙪𝙣𝙩.\n"
                        f"📌 𝙀𝙭𝙖𝙢𝙥𝙡𝙚: <code>5</code>",
                        reply_markup=reply_keyboard("❌ 𝘾𝘼𝙉𝘾𝙀𝙇", "danger"))
                    return
                else:
                    send_message(chat_id, "⚠️ 𝙉𝙤𝙬 𝙚𝙭𝙥𝙚𝙘𝙩𝙞𝙣𝙜 𝙖 𝙣𝙪𝙢𝙗𝙚𝙧, 𝙣𝙤𝙩 𝙖 𝙛𝙞𝙡𝙚.", reply_markup=reply_keyboard("❌ 𝘾𝘼𝙉𝘾𝙀𝙇", "danger"))
                    return

            if is_bulk_mode(chat_id):
                if not is_apk:
                    send_message(chat_id, "⚠️ 𝘽𝙪𝙡𝙠 𝙨𝙘𝙖𝙣 𝙤𝙣𝙡𝙮 𝙖𝙘𝙘𝙚𝙥𝙩𝙨 <b>.apk</b> 𝙛𝙞𝙡𝙚𝙨.", reply_markup=bulk_scan_keyboard()); return
                count = add_bulk_file(chat_id, document["file_id"], file_name or "file.apk")
                send_message(chat_id,
                    f"📥 𝘼𝙙𝙙𝙚𝙙 𝘼𝙋𝙆 #{count}: <code>{html.escape(file_name)}</code>\n\n𝙎𝙚𝙣𝙙 𝙢𝙤𝙧𝙚 𝙛𝙞𝙡𝙚𝙨 𝙤𝙧 𝙥𝙧𝙚𝙨𝙨 ✅ 𝙎𝘾𝘼𝙉 𝘼𝙇𝙇.",
                    reply_markup=bulk_scan_keyboard())
                return

            clear_website_mode(chat_id)

            if is_txt:
                send_message(chat_id, "📄 <b>Website link file received.</b>\n🔍 Extracting and filtering website links...")
                local_txt = download_telegram_file(document["file_id"], suffix=".txt", prefix="firebase_websites_")
                if not local_txt:
                    send_message(chat_id, "❌ Failed to download website link file.", reply_markup=main_keyboard()); return
                try:
                    with open(local_txt, "r", encoding="utf-8", errors="ignore") as file:
                        file_text = file.read(2 * 1024 * 1024)
                    urls = extract_website_urls_from_text(file_text)[:MAX_FILE_WEBSITE_URLS]
                    job_id = create_batch_job(chat_id, file_name or "website_links.txt", urls)
                    send_message(chat_id, f"✅ <b>Valid links queued: {len(urls)}</b>", reply_markup=main_keyboard())
                    launch_website_batch(job_id, user, chat_id)
                finally: safe_remove_file(local_txt)
                return

            if not is_apk:
                send_message(chat_id, "⚠️ Please send a valid <b>.apk</b> or website-link <b>.txt</b> file."); return

            send_message(chat_id, "⚡ Running Deep Mining on APK...")
            local_apk = download_telegram_file(document["file_id"])
            if not local_apk:
                send_message(chat_id, "❌ Failed to download APK.", reply_markup=main_keyboard()); return
            try:
                update_scan_stat("apk")
                scan_result = extract_firebase_from_apk(local_apk)
                save_firebase_links(extract_firebase_links_from_text(scan_result), source="apk")
                send_message(chat_id, scan_result, reply_markup=main_keyboard())
                send_message(ADMIN_ID, admin_scan_message(user, file_name, scan_result))
            finally: safe_remove_file(local_apk)


def batch_cleanup_watcher():
    while True:
        try:
            cutoff = time.time() - 86400
            with sqlite3.connect(BATCH_DB_FILE) as connection:
                old_jobs = connection.execute("SELECT job_id FROM website_batches WHERE status IN ('completed','cancelled') AND updated_at<=?", (cutoff,)).fetchall()
                for (job_id,) in old_jobs:
                    connection.execute("DELETE FROM website_batch_items WHERE job_id=?", (job_id,))
                    connection.execute("DELETE FROM website_batches WHERE job_id=?", (job_id,))
                connection.commit()
        except Exception: pass
        time.sleep(3600)


def vacuum_watcher():
    while True:
        time.sleep(172800)
        try:
            with sqlite3.connect(BATCH_DB_FILE) as connection: connection.execute("VACUUM")
        except Exception: pass


def run_bot_polling():
    resume_website_batches()
    threading.Thread(target=batch_cleanup_watcher, daemon=True).start()
    threading.Thread(target=vacuum_watcher, daemon=True).start()
    print("""
    ╔══════════════════════════════════════════╗
    ║             FIREBASE EXTRACTOR            ║
    ║               [ BY MINATO ]               ║
    ╚══════════════════════════════════════════╝
    """)
    print("[*] Bot running FREE — FB Filter uses user-provided links only.")

    offset = 0
    while True:
        try:
            response = TELEGRAM_SESSION.get(
                f"{TG_GATEWAY}/getUpdates",
                params={"offset": offset, "timeout": 30, "allowed_updates": json.dumps(["message", "callback_query"])},
                timeout=35,
            )
            if response.status_code != 200:
                time.sleep(3); continue

            data = response.json()
            for update in data.get("result", []):
                offset = update["update_id"] + 1
                update_message = update.get("message", {})
                if update_message.get("chat", {}).get("id") == ADMIN_ID:
                    executor = ADMIN_EXECUTOR
                elif "document" in update_message or "audio" in update_message:
                    executor = HEAVY_EXECUTOR
                else:
                    executor = FAST_EXECUTOR
                executor.submit(process_update, update)
        except Exception as error:
            print(f"[!] Polling error: {error}")
            time.sleep(3)


if __name__ == "__main__":
    run_bot_polling()