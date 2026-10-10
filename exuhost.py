"""
𝐈𝐍𝐒𝐀𝐍𝐄 𝐁𝐎𝐓 𝐇𝐎𝐒𝐓𝐈𝐍𝐆 𝐕𝐄𝐑𝐒𝐈𝐎𝐍 𝟑.𝟐
𝐂𝐋𝐄𝐀𝐍𝐄𝐃 & 𝐏𝐑𝐎𝐃𝐔𝐂𝐓𝐈𝐎𝐍-𝐑𝐄𝐀𝐃𝐘
𝐅𝐎𝐍𝐓 𝐒𝐓𝐘𝐋𝐄: 𝐌𝐀𝐓𝐇𝐄𝐌𝐀𝐓𝐈𝐂𝐀𝐋 𝐁𝐎𝐋𝐃 𝐒𝐀𝐍𝐒-𝐒𝐄𝐑𝐈𝐅
"""

import subprocess
import sys
import os

# ✅ 𝐀𝐮𝐭𝐨-𝐢𝐧𝐬𝐭𝐚𝐥𝐥 𝐦𝐢𝐬𝐬𝐢𝐧𝐠 𝐦𝐨𝐝𝐮𝐥𝐞𝐬
def auto_install(package):
    try:
        __import__(package)
    except ModuleNotFoundError:
        print(f"📦 𝐈𝐧𝐬𝐭𝐚𝐥𝐥𝐢𝐧𝐠 𝐦𝐢𝐬𝐬𝐢𝐧𝐠 𝐩𝐚𝐜𝐤𝐚𝐠𝐞: {package} ...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ 𝐈𝐧𝐬𝐭𝐚𝐥𝐥𝐞𝐝: {package}")

for mod in ["telebot", "psutil", "requests", "flask", "Pillow"]:
    auto_install(mod)

import telebot
import zipfile
import tempfile
import shutil
from telebot import types
import time
from datetime import datetime
import psutil
import logging
import threading
import re
import atexit
import requests
from flask import Flask
from threading import Thread


# ================================
# 𝐅𝐋𝐀𝐒𝐊 𝐊𝐄𝐄𝐏-𝐀𝐋𝐈𝐕𝐄
# ================================
app = Flask('')

@app.route('/')
def home():
    return "𝐈'𝐦 𝐈𝐍𝐒𝐀𝐍𝐄 𝐁𝐎𝐓 𝐇𝐎𝐒𝐓𝐈𝐍𝐆"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()
    print("✅ 𝐅𝐥𝐚𝐬𝐤 𝐊𝐞𝐞𝐩-𝐀𝐥𝐢𝐯𝐞 𝐬𝐞𝐫𝐯𝐞𝐫 𝐬𝐭𝐚𝐫𝐭𝐞𝐝.")

# ================================
# 𝐂𝐎𝐍𝐅𝐈𝐆𝐔𝐑𝐀𝐓𝐈𝐎𝐍
# ================================
TOKEN = '8901297950:AAEZKcAqeW_pDhn2SxdQgwIK_ZpujninTpM'
OWNER_ID = 8960648271
ADMIN_ID = 8960648271








# 𝐅𝐨𝐥𝐝𝐞𝐫 𝐬𝐞𝐭𝐮𝐩
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_BOTS_DIR = os.path.join(BASE_DIR, 'exu_uploads')
EXU_DATA_DIR = os.path.join(BASE_DIR, 'exu_data')

# 𝐓𝐈𝐄𝐑 𝐒𝐘𝐒𝐓𝐄𝐌
TIER_SYSTEM = {
    "free": {
        "name": "𝐅𝐑𝐄𝐄",
        "upload_limit": 3,
        "max_file_size": 50 * 1024 * 1024,
        "icon": "🎫",
        "color": "#2ecc71",
    },
    "premium": {
        "name": "𝐏𝐑𝐄𝐌𝐈𝐔𝐌",
        "upload_limit": 10,
        "max_file_size": 200 * 1024 * 1024,
        "icon": "⭐",
        "color": "#f39c12",
    },
    "owner": {
        "name": "𝐎𝐖𝐍𝐄𝐑",
        "upload_limit": float('inf'),
        "max_file_size": float('inf'),
        "icon": "👑",
        "color": "#e74c3c",
    }
}

# 𝐂𝐫𝐞𝐚𝐭𝐞 𝐧𝐞𝐜𝐞𝐬𝐬𝐚𝐫𝐲 𝐝𝐢𝐫𝐞𝐜𝐭𝐨𝐫𝐢𝐞𝐬
os.makedirs(UPLOAD_BOTS_DIR, exist_ok=True)
os.makedirs(EXU_DATA_DIR, exist_ok=True)

# 𝐈𝐧𝐢𝐭𝐢𝐚𝐥𝐢𝐳𝐞 𝐛𝐨𝐭
bot = telebot.TeleBot(TOKEN)

# 𝐆𝐥𝐨𝐛𝐚𝐥 𝐬𝐭𝐚𝐭𝐞
bot_scripts = {}
user_subscriptions = {}
user_files = {}
active_users = set()
admin_ids = {ADMIN_ID, OWNER_ID}
bot_locked = False

# 𝐋𝐨𝐠𝐠𝐢𝐧𝐠
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ================================
# 𝐅𝐎𝐍𝐓 𝐂𝐎𝐍𝐕𝐄𝐑𝐒𝐈𝐎𝐍
# ================================
def convert_to_bold_uppercase(text: str) -> str:
    bold_mapping = {
        'A': '𝐀', 'B': '𝐁', 'C': '𝐂', 'D': '𝐃', 'E': '𝐄', 'F': '𝐅', 'G': '𝐆',
        'H': '𝐇', 'I': '𝐈', 'J': '𝐉', 'K': '𝐊', 'L': '𝐋', 'M': '𝐌', 'N': '𝐍',
        'O': '𝐎', 'P': '𝐏', 'Q': '𝐐', 'R': '𝐑', 'S': '𝐒', 'T': '𝐓', 'U': '𝐔',
        'V': '𝐕', 'W': '𝐖', 'X': '𝐗', 'Y': '𝐘', 'Z': '𝐙',
        'a': '𝐚', 'b': '𝐛', 'c': '𝐜', 'd': '𝐝', 'e': '𝐞', 'f': '𝐟', 'g': '𝐠',
        'h': '𝐡', 'i': '𝐢', 'j': '𝐣', 'k': '𝐤', 'l': '𝐥', 'm': '𝐦', 'n': '𝐧',
        'o': '𝐨', 'p': '𝐩', 'q': '𝐪', 'r': '𝐫', 's': '𝐬', 't': '𝐭', 'u': '𝐮',
        'v': '𝐯', 'w': '𝐰', 'x': '𝐱', 'y': '𝐲', 'z': '𝐳',
        '0': '𝟎', '1': '𝟏', '2': '𝟐', '3': '𝟑', '4': '𝟒', '5': '𝟓', '6': '𝟔',
        '7': '𝟕', '8': '𝟖', '9': '𝟗',
        ' ': ' ', '!': '!', '@': '@', '#': '#', '$': '$', '%': '%', '^': '^',
        '&': '&', '*': '*', '(': '(', ')': ')', '-': '-', '_': '_', '=': '=',
        '+': '+', '[': '[', ']': ']', '{': '{', '}': '}', '\\': '\\', '|': '|',
        ';': ';', ':': ':', "'": "'", '"': '"', ',': ',', '.': '.', '<': '<',
        '>': '>', '/': '/', '?': '?', '`': '`', '~': '~'
    }
    result = []
    for char in str(text):
        result.append(bold_mapping.get(char, char))
    return ''.join(result)

B = convert_to_bold_uppercase

# ================================
# 𝐀𝐍𝐈𝐌𝐀𝐓𝐈𝐎𝐍
# ================================
class ProgressAnimation:
    @staticmethod
    def execute_animation():
        return [
            B("𝐄𝐱𝐞𝐜𝐮𝐭𝐢𝐧𝐠: [▱▱▱▱▱▱▱▱▱▱] 0%"),
            B("⚡ 𝐄𝐱𝐞𝐜𝐮𝐭𝐢𝐧𝐠: [▰▱▱▱▱▱▱▱▱▱] 10%"),
            B("⚡ 𝐄𝐱𝐞𝐜𝐮𝐭𝐢𝐧𝐠: [▰▰▱▱▱▱▱▱▱▱] 20%"),
            B("⚡ 𝐄𝐱𝐞𝐜𝐮𝐭𝐢𝐧𝐠: [▰▰▰▱▱▱▱▱▱▱] 30%"),
            B("⚡ 𝐄𝐱𝐞𝐜𝐮𝐭𝐢𝐧𝐠: [▰▰▰▰▱▱▱▱▱▱] 40%"),
            B("⚡ 𝐄𝐱𝐞𝐜𝐮𝐭𝐢𝐧𝐠: [▰▰▰▰▰▱▱▱▱▱] 50%"),
            B("⚡ 𝐄𝐱𝐞𝐜𝐮𝐭𝐢𝐧𝐠: [▰▰▰▰▰▰▱▱▱▱] 60%"),
            B("⚡ 𝐄𝐱𝐞𝐜𝐮𝐭𝐢𝐧𝐠: [▰▰▰▰▰▰▰▱▱▱] 70%"),
            B("⚡ 𝐄𝐱𝐞𝐜𝐮𝐭𝐢𝐧𝐠: [▰▰▰▰▰▰▰▰▱▱] 80%"),
            B("⚡ 𝐄𝐱𝐞𝐜𝐮𝐭𝐢𝐧𝐠: [▰▰▰▰▰▰▰▰▰▱] 90%"),
            B("✅ 𝐂𝐨𝐦𝐩𝐥𝐞𝐭𝐞: [▰▰▰▰▰▰▰▰▰▰] 100%")
        ]

    @staticmethod
    def upload_animation():
        return [
            B("📤 𝐔𝐩𝐥𝐨𝐚𝐝𝐢𝐧𝐠: [▱▱▱▱▱▱▱▱▱▱] 0%"),
            B("📤 𝐔𝐩𝐥𝐨𝐚𝐝𝐢𝐧𝐠: [▰▱▱▱▱▱▱▱▱▱] 25%"),
            B("📤 𝐔𝐩𝐥𝐨𝐚𝐝𝐢𝐧𝐠: [▰▰▰▱▱▱▱▱▱▱] 50%"),
            B("📤 𝐔𝐩𝐥𝐨𝐚𝐝𝐢𝐧𝐠: [▰▰▰▰▰▰▱▱▱▱] 75%"),
            B("✅ 𝐔𝐩𝐥𝐨𝐚𝐝 𝐂𝐨𝐦𝐩𝐥𝐞𝐭𝐞: [▰▰▰▰▰▰▰▰▰▰] 100%")
        ]

# ================================
# 𝐃𝐀𝐓𝐀𝐁𝐀𝐒𝐄 - 𝐑𝐀𝐌 𝐎𝐍𝐋𝐘 (𝐅𝐀𝐒𝐓)
# ================================
DB_LOCK = threading.Lock()

def init_db():
    """Initialize RAM data with owner/admin."""
    admin_ids.add(OWNER_ID)
    admin_ids.add(ADMIN_ID)
    logger.info("✅ RAM DB initialized.")

def load_data():
    """Data is in RAM - nothing to load."""
    logger.info("✅ 𝐑𝐀𝐌 𝐦𝐨𝐝𝐞: 𝐧𝐨 𝐥𝐨𝐚𝐝 𝐧𝐞𝐞𝐝𝐞𝐝.")

def save_user_file(user_id, file_name, file_type='py'):
    """Save user file metadata to RAM."""
    with DB_LOCK:
        if user_id not in user_files:
            user_files[user_id] = []
        user_files[user_id] = [(fn, ft) for fn, ft in user_files[user_id] if fn != file_name]
        user_files[user_id].append((file_name, file_type))
        logger.info(f"💾 𝐅𝐢𝐥𝐞 𝐬𝐚𝐯𝐞𝐝: {file_name} for {user_id}")

def remove_user_file_db(user_id, file_name):
    """Remove user file from RAM."""
    with DB_LOCK:
        if user_id in user_files:
            user_files[user_id] = [f for f in user_files[user_id] if f[0] != file_name]
            if not user_files[user_id]:
                del user_files[user_id]
        logger.info(f"🗑️ 𝐅𝐢𝐥𝐞 𝐫𝐞𝐦𝐨𝐯𝐞𝐝: {file_name} for {user_id}")

def add_active_user(user_id, username=None):
    """Add active user to RAM instantly."""
    active_users.add(user_id)

def save_subscription(user_id, expiry, tier='premium'):
    """Save subscription to RAM."""
    user_subscriptions[user_id] = {'expiry': expiry, 'tier': tier}

def add_admin_to_db(admin_id, added_by):
    """Add admin to RAM."""
    admin_ids.add(admin_id)

def remove_admin_from_db(admin_id):
    """Remove admin from RAM."""
    admin_ids.discard(admin_id)

# Init
init_db()
load_data()

# ================================
# 𝐇𝐄𝐋𝐏𝐄𝐑 𝐅𝐔𝐍𝐂𝐓𝐈𝐎𝐍𝐒
# ================================
def get_user_folder(user_id):
    user_folder = os.path.join(UPLOAD_BOTS_DIR, str(user_id))
    os.makedirs(user_folder, exist_ok=True)
    return user_folder

def get_user_tier(user_id):
    if user_id == OWNER_ID or user_id in admin_ids:
        return "owner"
    if user_id in user_subscriptions:
        sub = user_subscriptions[user_id]
        if sub.get('expiry') and sub['expiry'] > datetime.now():
            return sub.get('tier', 'premium')
    return "free"

def get_user_file_limit(user_id):
    return TIER_SYSTEM[get_user_tier(user_id)]["upload_limit"]

def get_user_file_count(user_id):
    return len(user_files.get(user_id, []))

def is_bot_running(user_id, file_name):
    script_key = f"{user_id}_{file_name}"
    script_info = bot_scripts.get(script_key)
    if script_info and script_info.get('process'):
        try:
            proc = psutil.Process(script_info['process'].pid)
            return proc.is_running() and proc.status() != psutil.STATUS_ZOMBIE
        except psutil.NoSuchProcess:
            if script_key in bot_scripts:
                del bot_scripts[script_key]
            return False
    return False

def kill_process_tree(process_info):
    try:
        process = process_info.get('process')
        if process and hasattr(process, 'pid'):
            pid = process.pid
            try:
                parent = psutil.Process(pid)
                children = parent.children(recursive=True)
                for child in children:
                    try:
                        child.terminate()
                    except:
                        pass
                try:
                    parent.terminate()
                    parent.wait(timeout=3)
                except:
                    try:
                        parent.kill()
                    except:
                        pass
            except psutil.NoSuchProcess:
                pass
    except Exception as e:
        logger.error(f"❌ 𝐄𝐫𝐫𝐨𝐫 𝐤𝐢𝐥𝐥𝐢𝐧𝐠 𝐩𝐫𝐨𝐜𝐞𝐬𝐬: {e}")

# ================================
# 𝐌𝐎𝐃𝐔𝐋𝐄𝐒
# ================================
TELEGRAM_MODULES = {
    'telebot': 'pyTelegramBotAPI',
    'telegram': 'python-telegram-bot',
    'aiogram': 'aiogram',
    'pyrogram': 'pyrogram',
    'telethon': 'telethon',
    'requests': 'requests',
    'flask': 'Flask',
    'psutil': 'psutil',
    'bs4': 'beautifulsoup4',
    'pandas': 'pandas',
    'numpy': 'numpy'
}

def attempt_install_pip(module_name, message):
    package_name = TELEGRAM_MODULES.get(module_name.lower(), module_name)
    if package_name is None:
        return False
    try:
        bot.reply_to(message, B(f"🐍 𝐈𝐧𝐬𝐭𝐚𝐥𝐥𝐢𝐧𝐠 `{module_name}`..."))
        command = [sys.executable, '-m', 'pip', 'install', package_name]
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        if result.returncode == 0:
            bot.reply_to(message, B(f"✅ 𝐏𝐚𝐜𝐤𝐚𝐠𝐞 `{package_name}` 𝐢𝐧𝐬𝐭𝐚𝐥𝐥𝐞𝐝."))
            return True
        else:
            bot.reply_to(message, B(f"❌ 𝐅𝐚𝐢𝐥𝐞𝐝 𝐭𝐨 𝐢𝐧𝐬𝐭𝐚𝐥𝐥 `{package_name}`."))
            return False
    except Exception as e:
        bot.reply_to(message, B(f"❌ 𝐄𝐫𝐫𝐨𝐫: {str(e)}"))
        return False

# ================================
# 𝐒𝐂𝐑𝐈𝐏𝐓 𝐑𝐔𝐍𝐍𝐈𝐍𝐆
# ================================
def run_script(script_path, user_id, user_folder, file_name, message):
    """Run Python script."""
    try:
        msg = bot.reply_to(message, ProgressAnimation.execute_animation()[0])

        for frame in ProgressAnimation.execute_animation():
            try:
                bot.edit_message_text(frame, message.chat.id, msg.message_id)
                time.sleep(0.3)
            except:
                pass

        if not os.path.exists(script_path):
            bot.edit_message_text(B(f"❌ 𝐅𝐢𝐥𝐞 𝐧𝐨𝐭 𝐟𝐨𝐮𝐧𝐝: `{file_name}`"),
                                   message.chat.id, msg.message_id)
            return

        # Pre-check for missing modules
        check_proc = None
        try:
            check_proc = subprocess.Popen(
                [sys.executable, script_path],
                cwd=user_folder,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True, encoding='utf-8', errors='ignore'
            )
            stdout, stderr = check_proc.communicate(timeout=5)
            if stderr:
                match = re.search(r"ModuleNotFoundError: No module named '(.+?)'", stderr)
                if match:
                    module_name = match.group(1)
                    if attempt_install_pip(module_name, message):
                        time.sleep(2)
        except subprocess.TimeoutExpired:
            if check_proc:
                check_proc.kill()
                check_proc.communicate()
        except Exception:
            pass

        log_file_path = os.path.join(user_folder, f"{os.path.splitext(file_name)[0]}.log")
        log_file = open(log_file_path, 'w', encoding='utf-8', errors='ignore')

        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE

        process = subprocess.Popen(
            [sys.executable, script_path],
            cwd=user_folder,
            stdout=log_file, stderr=log_file,
            stdin=subprocess.PIPE,
            startupinfo=startupinfo,
            encoding='utf-8', errors='ignore'
        )

        script_key = f"{user_id}_{file_name}"
        bot_scripts[script_key] = {
            'process': process,
            'log_file': log_file,
            'file_name': file_name,
            'user_id': user_id,
            'start_time': datetime.now(),
            'type': 'py',
            'script_key': script_key,
            'script_path': script_path
        }

        bot.edit_message_text(
            B(f"✅ 𝐏𝐲𝐭𝐡𝐨𝐧 𝐬𝐜𝐫𝐢𝐩𝐭 `{file_name}` 𝐬𝐭𝐚𝐫𝐭𝐞𝐝!\n📊 𝐏𝐈𝐃: `{process.pid}`"),
            message.chat.id, msg.message_id
        )

        # Auto show My Files list after script starts
        try:
            # Files already in RAM
            files = user_files.get(user_id, [])
            if files:
                markup = types.InlineKeyboardMarkup(row_width=1)
                for fn, ft in files:
                    running = is_bot_running(user_id, fn)
                    status = "🟢" if running else "🔴"
                    markup.add(types.InlineKeyboardButton(
                        B(f"{status} {fn} ({ft})"), callback_data=f'file_{user_id}_{fn}'))
                markup.add(types.InlineKeyboardButton(B("🔙 𝐁𝐚𝐜𝐤"), callback_data='back_to_main'))
                bot.send_message(message.chat.id, B("📂 𝐘𝐨𝐮𝐫 𝐅𝐢𝐥𝐞𝐬:"), reply_markup=markup)
        except Exception as ae:
            logger.error(f"Auto-show files error: {ae}")

    except Exception as e:
        logger.error(f"❌ run_script error: {e}")
        try:
            bot.reply_to(message, B(f"❌ 𝐄𝐫𝐫𝐨𝐫 𝐬𝐭𝐚𝐫𝐭𝐢𝐧𝐠 𝐬𝐜𝐫𝐢𝐩𝐭: {str(e)}"))
        except:
            pass

def run_js_script(script_path, user_id, user_folder, file_name, message):
    """Run JavaScript script."""
    try:
        msg = bot.reply_to(message, ProgressAnimation.execute_animation()[0])

        for frame in ProgressAnimation.execute_animation():
            try:
                bot.edit_message_text(frame, message.chat.id, msg.message_id)
                time.sleep(0.3)
            except:
                pass

        if not os.path.exists(script_path):
            bot.edit_message_text(B(f"❌ 𝐅𝐢𝐥𝐞 𝐧𝐨𝐭 𝐟𝐨𝐮𝐧𝐝: `{file_name}`"),
                                   message.chat.id, msg.message_id)
            return

        # Check for missing NPM modules
        check_proc = None
        try:
            check_proc = subprocess.Popen(
                ['node', script_path],
                cwd=user_folder,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True, encoding='utf-8', errors='ignore'
            )
            stdout, stderr = check_proc.communicate(timeout=5)
            if stderr and 'Cannot find module' in stderr:
                match = re.search(r"Cannot find module '(.+?)'", stderr)
                if match:
                    module_name = match.group(1)
                    bot.reply_to(message, B(f"📦 𝐈𝐧𝐬𝐭𝐚𝐥𝐥𝐢𝐧𝐠 `{module_name}`..."))
                    try:
                        subprocess.run(['npm', 'install', module_name], cwd=user_folder,
                                       capture_output=True, text=True, check=True)
                        bot.reply_to(message, B(f"✅ 𝐍𝐏𝐌 𝐩𝐚𝐜𝐤𝐚𝐠𝐞 `{module_name}` 𝐢𝐧𝐬𝐭𝐚𝐥𝐥𝐞𝐝."))
                        time.sleep(2)
                    except:
                        bot.reply_to(message, B(f"❌ 𝐅𝐚𝐢𝐥𝐞𝐝 𝐭𝐨 𝐢𝐧𝐬𝐭𝐚𝐥𝐥 `{module_name}`."))
        except subprocess.TimeoutExpired:
            if check_proc:
                check_proc.kill()
                check_proc.communicate()
        except Exception:
            pass

        log_file_path = os.path.join(user_folder, f"{os.path.splitext(file_name)[0]}.log")
        log_file = open(log_file_path, 'w', encoding='utf-8', errors='ignore')

        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE

        process = subprocess.Popen(
            ['node', script_path],
            cwd=user_folder,
            stdout=log_file, stderr=log_file,
            stdin=subprocess.PIPE,
            startupinfo=startupinfo,
            encoding='utf-8', errors='ignore'
        )

        script_key = f"{user_id}_{file_name}"
        bot_scripts[script_key] = {
            'process': process,
            'log_file': log_file,
            'file_name': file_name,
            'user_id': user_id,
            'start_time': datetime.now(),
            'type': 'js',
            'script_key': script_key
        }

        bot.edit_message_text(
            B(f"✅ 𝐉𝐒 𝐬𝐜𝐫𝐢𝐩𝐭 `{file_name}` 𝐬𝐭𝐚𝐫𝐭𝐞𝐝!\n📊 𝐏𝐈𝐃: `{process.pid}`"),
            message.chat.id, msg.message_id
        )

        # Auto show My Files list
        try:
            # Files already in RAM
            files = user_files.get(user_id, [])
            if files:
                markup = types.InlineKeyboardMarkup(row_width=1)
                for fn, ft in files:
                    running = is_bot_running(user_id, fn)
                    status = "🟢" if running else "🔴"
                    markup.add(types.InlineKeyboardButton(
                        B(f"{status} {fn} ({ft})"), callback_data=f'file_{user_id}_{fn}'))
                markup.add(types.InlineKeyboardButton(B("🔙 𝐁𝐚𝐜𝐤"), callback_data='back_to_main'))
                bot.send_message(message.chat.id, B("📂 𝐘𝐨𝐮𝐫 𝐅𝐢𝐥𝐞𝐬:"), reply_markup=markup)
        except Exception as ae:
            logger.error(f"Auto-show files error: {ae}")

    except Exception as e:
        logger.error(f"❌ run_js_script error: {e}")
        try:
            bot.reply_to(message, B(f"❌ 𝐄𝐫𝐫𝐨𝐫 𝐬𝐭𝐚𝐫𝐭𝐢𝐧𝐠 𝐉𝐒 𝐬𝐜𝐫𝐢𝐩𝐭: {str(e)}"))
        except:
            pass

# ================================
# 𝐌𝐄𝐍𝐔 𝐁𝐔𝐈𝐋𝐃𝐄𝐑𝐒
# ================================
def create_main_menu_inline(user_id):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_upload  = types.InlineKeyboardButton(B('📤 𝐔𝐩𝐥𝐨𝐚𝐝'), callback_data='upload')
    btn_files   = types.InlineKeyboardButton(B('📂 𝐌𝐲 𝐅𝐢𝐥𝐞𝐬'), callback_data='check_files')
    btn_stats   = types.InlineKeyboardButton(B('📊 𝐒𝐭𝐚𝐭𝐬'), callback_data='stats')
    btn_profile = types.InlineKeyboardButton(B('👤 𝐏𝐫𝐨𝐟𝐢𝐥𝐞'), callback_data='profile')
    btn_modules = types.InlineKeyboardButton(B('🐍 𝐌𝐨𝐝𝐮𝐥𝐞𝐬'), callback_data='modules')
    markup.add(btn_upload, btn_files)
    markup.add(btn_stats, btn_profile)
    markup.add(btn_modules)
    if user_id in admin_ids:
        btn_admin     = types.InlineKeyboardButton(B('👑 𝐀𝐝𝐦𝐢𝐧'), callback_data='admin_panel')
        btn_broadcast = types.InlineKeyboardButton(B('📢 𝐁𝐫𝐨𝐚𝐝𝐜𝐚𝐬𝐭'), callback_data='broadcast')
        btn_lock = types.InlineKeyboardButton(
            B('🔒 𝐋𝐨𝐜𝐤') if not bot_locked else B('🔓 𝐔𝐧𝐥𝐨𝐜𝐤'),
            callback_data='lock_bot' if not bot_locked else 'unlock_bot'
        )
        btn_analytics = types.InlineKeyboardButton(B('📈 𝐀𝐧𝐚𝐥𝐲𝐭𝐢𝐜𝐬'), callback_data='analytics')
        btn_managedb = types.InlineKeyboardButton(B('🗄️ 𝐌𝐚𝐧𝐚𝐠𝐞 𝐃𝐁'), callback_data='manage_db')
        markup.add(btn_admin, btn_broadcast)
        markup.add(btn_lock, btn_analytics)
        markup.add(btn_managedb)
    return markup

def create_reply_keyboard_main_menu(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    if user_id in admin_ids:
        buttons = [
            B("📤 𝐔𝐩𝐥𝐨𝐚𝐝"), B("📂 𝐌𝐲 𝐅𝐢𝐥𝐞𝐬"),
            B("📊 𝐒𝐭𝐚𝐭𝐬"), B("👤 𝐏𝐫𝐨𝐟𝐢𝐥𝐞"),
            B("🐍 𝐌𝐨𝐝𝐮𝐥𝐞𝐬"), B("👑 𝐀𝐝𝐦𝐢𝐧"),
            B("📢 𝐁𝐫𝐨𝐚𝐝𝐜𝐚𝐬𝐭"), B("🗄️ 𝐌𝐚𝐧𝐚𝐠𝐞 𝐃𝐁"),
        ]
    else:
        buttons = [
            B("📤 𝐔𝐩𝐥𝐨𝐚𝐝"), B("📂 𝐌𝐲 𝐅𝐢𝐥𝐞𝐬"),
            B("📊 𝐒𝐭𝐚𝐭𝐬"), B("👤 𝐏𝐫𝐨𝐟𝐢𝐥𝐞"),
            B("🐍 𝐌𝐨𝐝𝐮𝐥𝐞𝐬"),
        ]
    for i in range(0, len(buttons), 2):
        row = buttons[i:i+2]
        markup.add(*[types.KeyboardButton(text) for text in row])
    return markup

def create_control_buttons(user_id, file_name, is_running=True):
    markup = types.InlineKeyboardMarkup(row_width=2)
    if is_running:
        markup.row(
            types.InlineKeyboardButton(B("🔴 𝐒𝐭𝐨𝐩"), callback_data=f'stop_{user_id}_{file_name}'),
            types.InlineKeyboardButton(B("🔄 𝐑𝐞𝐬𝐭𝐚𝐫𝐭"), callback_data=f'restart_{user_id}_{file_name}')
        )
        markup.row(
            types.InlineKeyboardButton(B("🗑️ 𝐃𝐞𝐥𝐞𝐭𝐞"), callback_data=f'delete_{user_id}_{file_name}'),
            types.InlineKeyboardButton(B("📜 𝐋𝐨𝐠𝐬"), callback_data=f'logs_{user_id}_{file_name}')
        )
    else:
        markup.row(
            types.InlineKeyboardButton(B("🟢 𝐒𝐭𝐚𝐫𝐭"), callback_data=f'start_{user_id}_{file_name}'),
            types.InlineKeyboardButton(B("🗑️ 𝐃𝐞𝐥𝐞𝐭𝐞"), callback_data=f'delete_{user_id}_{file_name}')
        )
        markup.row(
            types.InlineKeyboardButton(B("📜 𝐕𝐢𝐞𝐰 𝐋𝐨𝐠𝐬"), callback_data=f'logs_{user_id}_{file_name}')
        )
    markup.add(types.InlineKeyboardButton(B("🔙 𝐁𝐚𝐜𝐤"), callback_data='check_files'))
    return markup

def create_admin_panel():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.row(
        types.InlineKeyboardButton(B('➕ 𝐀𝐝𝐝 𝐀𝐝𝐦𝐢𝐧'), callback_data='add_admin'),
        types.InlineKeyboardButton(B('➖ 𝐑𝐞𝐦𝐨𝐯𝐞 𝐀𝐝𝐦𝐢𝐧'), callback_data='remove_admin')
    )
    markup.row(
        types.InlineKeyboardButton(B('📋 𝐋𝐢𝐬𝐭 𝐀𝐝𝐦𝐢𝐧𝐬'), callback_data='list_admins'),
        types.InlineKeyboardButton(B('📊 𝐒𝐲𝐬𝐭𝐞𝐦 𝐒𝐭𝐚𝐭𝐬'), callback_data='system_stats')
    )
    markup.row(types.InlineKeyboardButton(B('🔙 𝐁𝐚𝐜𝐤'), callback_data='back_to_main'))
    return markup

# ================================
# 𝐂𝐎𝐌𝐌𝐀𝐍𝐃 𝐇𝐀𝐍𝐃𝐋𝐄𝐑𝐒
# ================================
@bot.message_handler(commands=['start'])
def command_send_welcome(message):
    user_id = message.from_user.id
    username = message.from_user.username
    add_active_user(user_id, username)

    if user_id not in admin_ids:
        # Non-admin users get a basic reply
        bot.send_message(
            message.chat.id,
            B("⚠️ 𝐀𝐜𝐜𝐞𝐬𝐬 𝐃𝐞𝐧𝐢𝐞𝐝. 𝐂𝐨𝐧𝐭𝐚𝐜𝐭 𝐚𝐝𝐦𝐢𝐧.")
        )
        return

    tier = get_user_tier(user_id)
    tier_info = TIER_SYSTEM[tier]

    welcome_text = B(f"""
┏━━━━━━━━━━━━━━━━━━━━━━┓
┃   🚀 𝐈𝐍𝐒𝐀𝐍𝐄 𝐁𝐎𝐓 𝐇𝐎𝐒𝐓𝐈𝐍𝐆   ┃
┃      𝐕𝐄𝐑𝐒𝐈𝐎𝐍 𝟑.𝟐     ┃
┗━━━━━━━━━━━━━━━━━━━━━━┛

⚡ 𝐀𝐚 𝐠𝐚𝐲𝐚 𝐛𝐡𝐚𝐢, {message.from_user.first_name}! 🔥
🆔 𝐈𝐃: `{user_id}`
🎫 𝐓𝐢𝐞𝐫: {tier_info['icon']} {tier_info['name']}
📁 𝐅𝐢𝐥𝐞𝐬: {get_user_file_count(user_id)}/{get_user_file_limit(user_id)}

🛡️ 𝐓𝐞𝐫𝐚 𝐛𝐨𝐭 𝐡𝐚𝐦𝐚𝐫𝐞 𝐬𝐚𝐭𝐡 𝐬𝐚𝐟𝐞 𝐡𝐚𝐢!
📤 𝐅𝐢𝐥𝐞 𝐛𝐡𝐞𝐣, 𝐛𝐨𝐭 𝐜𝐡𝐚𝐥𝐚𝐨 — 𝐛𝐚𝐬 𝐢𝐭𝐧𝐚 𝐤𝐚𝐚𝐦.
""")

    try:
        user_profile_photos = bot.get_user_profile_photos(user_id, limit=1)
        if user_profile_photos.total_count > 0:
            file_id = user_profile_photos.photos[0][-1].file_id
            bot.send_photo(message.chat.id, file_id, caption=welcome_text,
                           reply_markup=create_reply_keyboard_main_menu(user_id),
                           parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, welcome_text,
                             reply_markup=create_reply_keyboard_main_menu(user_id),
                             parse_mode='Markdown')
    except Exception:
        bot.send_message(message.chat.id, welcome_text,
                         reply_markup=create_reply_keyboard_main_menu(user_id),
                         parse_mode='Markdown')

@bot.message_handler(commands=['help'])
def command_help(message):
    if message.from_user.id not in admin_ids:
        return
    help_text = B("""
🤖 𝐈𝐍𝐒𝐀𝐍𝐄 𝐁𝐎𝐓 𝐇𝐎𝐒𝐓𝐈𝐍𝐆 𝐇𝐄𝐋𝐏

𝐁𝐚𝐬𝐢𝐜 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬:
/start - 𝐒𝐭𝐚𝐫𝐭 𝐭𝐡𝐞 𝐛𝐨𝐭
/files - 𝐀𝐩𝐧𝐢 𝐟𝐢𝐥𝐞𝐬 𝐝𝐞𝐤𝐡𝐨
/admin - 𝐀𝐝𝐦𝐢𝐧 𝐩𝐚𝐧𝐞𝐥
/stats - 𝐒𝐭𝐚𝐭𝐢𝐬𝐭𝐢𝐜𝐬
/profile - 𝐀𝐩𝐧𝐚 𝐩𝐫𝐨𝐟𝐢𝐥𝐞
/modules - 𝐌𝐨𝐝𝐮𝐥𝐞𝐬 𝐦𝐚𝐧𝐚𝐠𝐞𝐫
/broadcast - 𝐒𝐚𝐛 𝐤𝐨 𝐦𝐞𝐬𝐬𝐚𝐠𝐞 𝐛𝐡𝐞𝐣𝐨

𝐔𝐩𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝐅𝐢𝐥𝐞𝐬:
- 𝐒𝐞𝐧𝐝 𝐚 .𝐩𝐲, .𝐣𝐬, 𝐨𝐫 .𝐳𝐢𝐩 𝐟𝐢𝐥𝐞
- 𝐁𝐨𝐭 𝐰𝐢𝐥𝐥 𝐚𝐮𝐭𝐨-𝐢𝐧𝐬𝐭𝐚𝐥𝐥 𝐝𝐞𝐩𝐞𝐧𝐝𝐞𝐧𝐜𝐢𝐞𝐬
- 𝐘𝐨𝐮𝐫 𝐬𝐜𝐫𝐢𝐩𝐭 𝐰𝐢𝐥𝐥 𝐬𝐭𝐚𝐫𝐭 𝐚𝐮𝐭𝐨𝐦𝐚𝐭𝐢𝐜𝐚𝐥𝐥𝐲
""")
    bot.reply_to(message, help_text, parse_mode='Markdown')

@bot.message_handler(commands=['files'])
def command_files(message):
    if message.from_user.id not in admin_ids:
        return
    show_user_files(message)

@bot.message_handler(commands=['admin'])
def command_admin(message):
    if message.from_user.id not in admin_ids:
        return
    show_admin_panel(message)

@bot.message_handler(commands=['stats'])
def command_stats_cmd(message):
    if message.from_user.id not in admin_ids:
        return
    show_stats(message)

@bot.message_handler(commands=['profile'])
def command_profile(message):
    if message.from_user.id not in admin_ids:
        return
    show_profile(message)

@bot.message_handler(commands=['modules'])
def command_modules(message):
    if message.from_user.id not in admin_ids:
        return
    show_modules_panel(message)

@bot.message_handler(commands=['broadcast'])
def command_broadcast(message):
    if message.from_user.id not in admin_ids:
        return
    start_broadcast(message)

# ================================
# 𝐅𝐈𝐋𝐄 𝐔𝐏𝐋𝐎𝐀𝐃 𝐇𝐀𝐍𝐃𝐋𝐄𝐑
# ================================
@bot.message_handler(content_types=['document'])
def handle_file_upload(message):
    user_id = message.from_user.id
    if user_id not in admin_ids:
        return

    if bot_locked:
        bot.reply_to(message, B("⚠️ 𝐁𝐨𝐭 𝐢𝐬 𝐥𝐨𝐜𝐤𝐞𝐝."))
        return

    file_limit = get_user_file_limit(user_id)
    current_files = get_user_file_count(user_id)

    if current_files >= file_limit:
        bot.reply_to(message, B(f"⚠️ 𝐅𝐢𝐥𝐞 𝐥𝐢𝐦𝐢𝐭 𝐫𝐞𝐚𝐜𝐡𝐞𝐝 ({current_files}/{file_limit})."))
        return

    doc = message.document
    if not doc.file_name:
        bot.reply_to(message, B("⚠️ 𝐍𝐨 𝐟𝐢𝐥𝐞 𝐧𝐚𝐦𝐞 𝐩𝐫𝐨𝐯𝐢𝐝𝐞𝐝."))
        return

    file_ext = os.path.splitext(doc.file_name)[1].lower()
    if file_ext not in ['.py', '.js', '.zip']:
        bot.reply_to(message, B("⚠️ 𝐔𝐧𝐬𝐮𝐩𝐩𝐨𝐫𝐭𝐞𝐝 𝐟𝐢𝐥𝐞 𝐭𝐲𝐩𝐞. 𝐔𝐬𝐞 .𝐩𝐲, .𝐣𝐬, 𝐨𝐫 .𝐳𝐢𝐩"))
        return

    msg = bot.reply_to(message, ProgressAnimation.upload_animation()[0])

    try:
        for frame in ProgressAnimation.upload_animation():
            try:
                bot.edit_message_text(frame, message.chat.id, msg.message_id)
                time.sleep(0.3)
            except:
                pass

        file_info = bot.get_file(doc.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        user_folder = get_user_folder(user_id)
        file_path = os.path.join(user_folder, doc.file_name)

        with open(file_path, 'wb') as f:
            f.write(downloaded_file)

        if file_ext == '.zip':
            handle_zip_file(downloaded_file, doc.file_name, user_id, user_folder, message)
        elif file_ext == '.py':
            save_user_file(user_id, doc.file_name, 'py')
            threading.Thread(target=run_script,
                             args=(file_path, user_id, user_folder, doc.file_name, message)).start()
        elif file_ext == '.js':
            save_user_file(user_id, doc.file_name, 'js')
            threading.Thread(target=run_js_script,
                             args=(file_path, user_id, user_folder, doc.file_name, message)).start()

    except Exception as e:
        try:
            bot.edit_message_text(
                B(f"❌ 𝐄𝐫𝐫𝐨𝐫 𝐮𝐩𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝐟𝐢𝐥𝐞: {str(e)}"),
                message.chat.id, msg.message_id
            )
        except:
            bot.reply_to(message, B(f"❌ 𝐄𝐫𝐫𝐨𝐫: {str(e)}"))

def handle_zip_file(file_content, file_name, user_id, user_folder, message):
    temp_dir = None
    try:
        temp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(temp_dir, file_name)

        with open(zip_path, 'wb') as f:
            f.write(file_content)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        extracted_files = os.listdir(temp_dir)
        py_files = [f for f in extracted_files if f.endswith('.py')]
        js_files = [f for f in extracted_files if f.endswith('.js')]

        main_script = None
        file_type = None

        for name in ['main.py', 'bot.py', 'app.py']:
            if name in py_files:
                main_script = name
                file_type = 'py'
                break

        if not main_script and py_files:
            main_script = py_files[0]
            file_type = 'py'
        elif not main_script and js_files:
            for name in ['index.js', 'main.js', 'bot.js']:
                if name in js_files:
                    main_script = name
                    file_type = 'js'
                    break
            if not main_script and js_files:
                main_script = js_files[0]
                file_type = 'js'

        if not main_script:
            bot.reply_to(message, B("❌ 𝐍𝐨 .𝐩𝐲 𝐨𝐫 .𝐣𝐬 𝐟𝐢𝐥𝐞 𝐟𝐨𝐮𝐧𝐝 𝐢𝐧 𝐙𝐈𝐏."))
            return

        for item in os.listdir(temp_dir):
            src = os.path.join(temp_dir, item)
            dst = os.path.join(user_folder, item)
            if os.path.isdir(src):
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)

        save_user_file(user_id, main_script, file_type)
        main_script_path = os.path.join(user_folder, main_script)

        if file_type == 'py':
            threading.Thread(target=run_script,
                             args=(main_script_path, user_id, user_folder, main_script, message)).start()
        else:
            threading.Thread(target=run_js_script,
                             args=(main_script_path, user_id, user_folder, main_script, message)).start()

    except Exception as e:
        bot.reply_to(message, B(f"❌ 𝐄𝐫𝐫𝐨𝐫 𝐩𝐫𝐨𝐜𝐞𝐬𝐬𝐢𝐧𝐠 𝐙𝐈𝐏: {str(e)}"))
    finally:
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

# ================================
# 𝐁𝐔𝐒𝐈𝐍𝐄𝐒𝐒 𝐋𝐎𝐆𝐈𝐂 𝐅𝐔𝐍𝐂𝐓𝐈𝐎𝐍𝐒
# ================================
def show_user_files(message):
    user_id = message.from_user.id
    # Use RAM directly

    files = user_files.get(user_id, [])
    if not files:
        bot.reply_to(message, B("📭 𝐍𝐨 𝐟𝐢𝐥𝐞𝐬 𝐮𝐩𝐥𝐨𝐚𝐝𝐞𝐝 𝐲𝐞𝐭."))
        return

    markup = types.InlineKeyboardMarkup(row_width=1)
    for file_name, file_type in files:
        running = is_bot_running(user_id, file_name)
        status = "🟢" if running else "🔴"
        markup.add(types.InlineKeyboardButton(
            B(f"{status} {file_name} ({file_type})"),
            callback_data=f'file_{user_id}_{file_name}'
        ))
    bot.reply_to(message, B("📂 𝐘𝐨𝐮𝐫 𝐅𝐢𝐥𝐞𝐬:"), reply_markup=markup)

def show_stats(message):
    user_id = message.from_user.id
    total_users = len(active_users)
    total_files = sum(len(files) for files in user_files.values())
    running_scripts = len([k for k, v in bot_scripts.items() if is_bot_running(v['user_id'], v['file_name'])])

    stats_text = B(f"""
📊 𝐒𝐘𝐒𝐓𝐄𝐌 𝐒𝐓𝐀𝐓𝐈𝐒𝐓𝐈𝐂𝐒

👥 𝐓𝐨𝐭𝐚𝐥 𝐔𝐬𝐞𝐫𝐬: {total_users}
📁 𝐓𝐨𝐭𝐚𝐥 𝐅𝐢𝐥𝐞𝐬: {total_files}
🟢 𝐑𝐮𝐧𝐧𝐢𝐧𝐠 𝐒𝐜𝐫𝐢𝐩𝐭𝐬: {running_scripts}
🔒 𝐁𝐨𝐭 𝐒𝐭𝐚𝐭𝐮𝐬: {'🔴 𝐋𝐨𝐜𝐤𝐞𝐝' if bot_locked else '🟢 𝐔𝐧𝐥𝐨𝐜𝐤𝐞𝐝'}

🎫 𝐓𝐢𝐞𝐫 𝐃𝐢𝐬𝐭𝐫𝐢𝐛𝐮𝐭𝐢𝐨𝐧:
• 𝐅𝐑𝐄𝐄: {len([uid for uid in active_users if get_user_tier(uid) == 'free'])}
• 𝐏𝐑𝐄𝐌𝐈𝐔𝐌: {len([uid for uid in active_users if get_user_tier(uid) == 'premium'])}
• 𝐎𝐖𝐍𝐄𝐑/𝐀𝐃𝐌𝐈𝐍: {len([uid for uid in active_users if get_user_tier(uid) == 'owner'])}
""")
    bot.reply_to(message, stats_text, parse_mode='Markdown')

def show_profile(message):
    user_id = message.from_user.id
    tier = get_user_tier(user_id)
    tier_info = TIER_SYSTEM[tier]

    profile_text = B(f"""
👤 𝐏𝐑𝐎𝐅𝐈𝐋𝐄

🆔 𝐔𝐬𝐞𝐫 𝐈𝐃: `{user_id}`
👤 𝐍𝐚𝐦𝐞: {message.from_user.first_name}
🎫 𝐓𝐢𝐞𝐫: {tier_info['icon']} {tier_info['name']}
📁 𝐅𝐢𝐥𝐞𝐬: {get_user_file_count(user_id)}/{get_user_file_limit(user_id)}
🟢 𝐑𝐮𝐧𝐧𝐢𝐧𝐠: {len([1 for f in user_files.get(user_id, []) if is_bot_running(user_id, f[0])])}
""")
    bot.reply_to(message, profile_text, parse_mode='Markdown')

def show_modules_panel(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton(B("🔙 𝐁𝐚𝐜𝐤"), callback_data="back_to_main"))
    bot.reply_to(message, B("""🐍 𝐌𝐎𝐃𝐔𝐋𝐄𝐒 𝐌𝐀𝐍𝐀𝐆𝐄𝐑

📦 𝐀𝐩𝐧𝐚 module name bhejo install karne ke liye
𝐄𝐱𝐚𝐦𝐩𝐥𝐞: requests, flask, numpy

𝐁𝐨𝐭 automatically install karega!"""), reply_markup=markup)

def show_admin_panel(message):
    if message.from_user.id not in admin_ids:
        bot.reply_to(message, B("⚠️ 𝐀𝐝𝐦𝐢𝐧 𝐩𝐞𝐫𝐦𝐢𝐬𝐬𝐢𝐨𝐧𝐬 𝐫𝐞𝐪𝐮𝐢𝐫𝐞𝐝."))
        return
    bot.reply_to(message, B("👑 𝐀𝐃𝐌𝐈𝐍 𝐏𝐀𝐍𝐄𝐋"), reply_markup=create_admin_panel())

def start_broadcast(message):
    if message.from_user.id not in admin_ids:
        bot.reply_to(message, B("⚠️ 𝐀𝐝𝐦𝐢𝐧 𝐩𝐞𝐫𝐦𝐢𝐬𝐬𝐢𝐨𝐧𝐬 𝐫𝐞𝐪𝐮𝐢𝐫𝐞𝐝."))
        return
    bot.reply_to(message, B("📢 𝐒𝐞𝐧𝐝 𝐭𝐡𝐞 𝐦𝐞𝐬𝐬𝐚𝐠𝐞 𝐲𝐨𝐮 𝐰𝐚𝐧𝐭 𝐭𝐨 𝐛𝐫𝐨𝐚𝐝𝐜𝐚𝐬𝐭."))
    bot.register_next_step_handler(message, process_broadcast_message)

def process_broadcast_message(message):
    if message.from_user.id not in admin_ids:
        return
    broadcast_text = message.text or message.caption
    if not broadcast_text:
        bot.reply_to(message, B("⚠️ 𝐍𝐨 𝐦𝐞𝐬𝐬𝐚𝐠𝐞 𝐟𝐨𝐮𝐧𝐝."))
        return
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(B('✅ 𝐂𝐨𝐧𝐟𝐢𝐫𝐦'), callback_data=f'broadcast_confirm_{message.message_id}'),
        types.InlineKeyboardButton(B('❌ 𝐂𝐚𝐧𝐜𝐞𝐥'), callback_data='broadcast_cancel')
    )
    preview_text = broadcast_text[:1000].strip()
    bot.reply_to(message,
                 B(f"📢 𝐁𝐫𝐨𝐚𝐝𝐜𝐚𝐬𝐭 𝐭𝐨 {len(active_users)} 𝐮𝐬𝐞𝐫𝐬?\n\n{preview_text}"),
                 reply_markup=markup)

# ================================
# 𝐓𝐄𝐗𝐓 𝐁𝐔𝐓𝐓𝐎𝐍 𝐇𝐀𝐍𝐃𝐋𝐄𝐑𝐒
# ================================
BUTTON_HANDLERS = {
    B("📤 𝐔𝐩𝐥𝐨𝐚𝐝"): lambda m: bot.reply_to(m, B("📤 𝐒𝐞𝐧𝐝 𝐲𝐨𝐮𝐫 .𝐩𝐲, .𝐣𝐬, 𝐨𝐫 .𝐳𝐢𝐩 𝐟𝐢𝐥𝐞.")),
    B("📂 𝐌𝐲 𝐅𝐢𝐥𝐞𝐬"): lambda m: show_user_files(m),
    B("📊 𝐒𝐭𝐚𝐭𝐬"): lambda m: show_stats(m),
    B("👤 𝐏𝐫𝐨𝐟𝐢𝐥𝐞"): lambda m: show_profile(m),
    B("🐍 𝐌𝐨𝐝𝐮𝐥𝐞𝐬"): lambda m: show_modules_panel(m),
    B("👑 𝐀𝐝𝐦𝐢𝐧"): lambda m: show_admin_panel(m),
    B("📢 𝐁𝐫𝐨𝐚𝐝𝐜𝐚𝐬𝐭"): lambda m: start_broadcast(m),
    B("🗄️ 𝐌𝐚𝐧𝐚𝐠𝐞 𝐃𝐁"): lambda m: show_manage_db(m),
}

@bot.message_handler(func=lambda message: message.text in BUTTON_HANDLERS)
def handle_button_click(message):
    if message.from_user.id not in admin_ids:
        return
    handler = BUTTON_HANDLERS.get(message.text)
    if handler:
        handler(message)

@bot.message_handler(func=lambda message: message.text and len(message.text.split()) == 1
                     and message.text not in BUTTON_HANDLERS
                     and not message.text.startswith('/'))
def handle_module_install(message):
    """Handle plain text module install requests."""
    if message.from_user.id not in admin_ids:
        return
    module_name = message.text.strip()
    if re.match(r'^[a-zA-Z0-9_\-\.]+$', module_name):
        attempt_install_pip(module_name, message)

# ================================
# 𝐂𝐀𝐋𝐋𝐁𝐀𝐂𝐊 𝐇𝐀𝐍𝐃𝐋𝐄𝐑𝐒
# ================================
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    user_id = call.from_user.id
    if user_id not in admin_ids:
        bot.answer_callback_query(call.id)
        return
    data = call.data

    try:
        if data == 'upload':
            upload_callback(call)
        elif data == 'check_files':
            check_files_callback(call)
        elif data.startswith('file_'):
            file_control_callback(call)
        elif data.startswith('start_'):
            start_bot_callback(call)
        elif data.startswith('stop_'):
            stop_bot_callback(call)
        elif data.startswith('restart_'):
            restart_bot_callback(call)
        elif data.startswith('delete_'):
            delete_bot_callback(call)
        elif data.startswith('logs_'):
            logs_bot_callback(call)
        elif data == 'stats':
            stats_callback(call)
        elif data == 'profile':
            profile_callback(call)
        elif data == 'admin_panel':
            admin_panel_callback(call)
        elif data == 'broadcast':
            broadcast_callback(call)
        elif data == 'lock_bot':
            lock_bot_callback(call)
        elif data == 'unlock_bot':
            unlock_bot_callback(call)
        elif data == 'analytics':
            analytics_callback(call)
        elif data == 'add_admin':
            add_admin_callback(call)
        elif data == 'remove_admin':
            remove_admin_callback(call)
        elif data == 'list_admins':
            list_admins_callback(call)
        elif data == 'system_stats':
            system_stats_callback(call)
        elif data.startswith('broadcast_confirm_'):
            broadcast_confirm_callback(call)
        elif data == 'broadcast_cancel':
            broadcast_cancel_callback(call)
        elif data == 'back_to_main':
            back_to_main_callback(call)
        elif data == 'modules':
            modules_callback(call)
        elif data == 'manage_db':
            manage_db_callback(call)
        elif data.startswith('dbfile_'):
            dbfile_detail_callback(call)
        elif data.startswith('dbdelete_'):
            dbdelete_callback(call)
        else:
            bot.answer_callback_query(call.id, "❌ 𝐔𝐧𝐤𝐧𝐨𝐰𝐧 𝐜𝐨𝐦𝐦𝐚𝐧𝐝")
    except Exception as e:
        logger.error(f"❌ 𝐂𝐚𝐥𝐥𝐛𝐚𝐜𝐤 𝐞𝐫𝐫𝐨𝐫: {e}")
        try:
            bot.answer_callback_query(call.id, "❌ 𝐄𝐫𝐫𝐨𝐫 𝐩𝐫𝐨𝐜𝐞𝐬𝐬𝐢𝐧𝐠 𝐫𝐞𝐪𝐮𝐞𝐬𝐭")
        except:
            pass

# ================================
# 𝐂𝐀𝐋𝐋𝐁𝐀𝐂𝐊 𝐈𝐌𝐏𝐋𝐄𝐌𝐄𝐍𝐓𝐀𝐓𝐈𝐎𝐍𝐒
# ================================
def upload_callback(call):
    user_id = call.from_user.id
    file_limit = get_user_file_limit(user_id)
    current_files = get_user_file_count(user_id)
    if current_files >= file_limit:
        bot.answer_callback_query(call.id,
                                  B(f"⚠️ 𝐅𝐢𝐥𝐞 𝐥𝐢𝐦𝐢𝐭 𝐫𝐞𝐚𝐜𝐡𝐞𝐝 ({current_files}/{file_limit})"),
                                  show_alert=True)
        return
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, B("📤 𝐒𝐞𝐧𝐝 𝐲𝐨𝐮𝐫 .𝐩𝐲, .𝐣𝐬, 𝐨𝐫 .𝐳𝐢𝐩 𝐟𝐢𝐥𝐞."))

def check_files_callback(call):
    user_id = call.from_user.id
    # Use RAM directly

    files = user_files.get(user_id, [])
    if not files:
        bot.answer_callback_query(call.id, B("📭 𝐍𝐨 𝐟𝐢𝐥𝐞𝐬 𝐮𝐩𝐥𝐨𝐚𝐝𝐞𝐝"), show_alert=True)
        return

    markup = types.InlineKeyboardMarkup(row_width=1)
    for file_name, file_type in files:
        running = is_bot_running(user_id, file_name)
        status = "🟢" if running else "🔴"
        markup.add(types.InlineKeyboardButton(
            B(f"{status} {file_name} ({file_type})"),
            callback_data=f'file_{user_id}_{file_name}'
        ))
    markup.add(types.InlineKeyboardButton(B("🔙 𝐁𝐚𝐜𝐤"), callback_data='back_to_main'))
    bot.answer_callback_query(call.id)
    bot.edit_message_text(B("📂 𝐘𝐨𝐮𝐫 𝐅𝐢𝐥𝐞𝐬:"),
                          call.message.chat.id, call.message.message_id,
                          reply_markup=markup)

def file_control_callback(call):
    try:
        parts = call.data.split('_')
        if len(parts) < 3:
            return
        user_id = int(parts[1])
        file_name = '_'.join(parts[2:])

        if call.from_user.id != user_id and call.from_user.id not in admin_ids:
            bot.answer_callback_query(call.id, B("⚠️ 𝐏𝐞𝐫𝐦𝐢𝐬𝐬𝐢𝐨𝐧 𝐝𝐞𝐧𝐢𝐞𝐝"), show_alert=True)
            return

        files = user_files.get(user_id, [])
        file_info = next(((fn, ft) for fn, ft in files if fn == file_name), None)

        if not file_info:
            bot.answer_callback_query(call.id, B("❌ 𝐅𝐢𝐥𝐞 𝐧𝐨𝐭 𝐟𝐨𝐮𝐧𝐝"), show_alert=True)
            return

        is_running = is_bot_running(user_id, file_name)
        bot.answer_callback_query(call.id)
        bot.edit_message_text(
            B(f"⚙️ 𝐂𝐨𝐧𝐭𝐫𝐨𝐥𝐬 𝐟𝐨𝐫: `{file_name}`\n📁 𝐓𝐲𝐩𝐞: {file_info[1]}\n📊 𝐒𝐭𝐚𝐭𝐮𝐬: {'🟢 𝐑𝐮𝐧𝐧𝐢𝐧𝐠' if is_running else '🔴 𝐒𝐭𝐨𝐩𝐩𝐞𝐝'}"),
            call.message.chat.id, call.message.message_id,
            reply_markup=create_control_buttons(user_id, file_name, is_running),
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"❌ file_control_callback error: {e}")
        bot.answer_callback_query(call.id, B("❌ 𝐄𝐫𝐫𝐨𝐫 𝐩𝐫𝐨𝐜𝐞𝐬𝐬𝐢𝐧𝐠"))

def start_bot_callback(call):
    try:
        parts = call.data.split('_')
        user_id = int(parts[1])
        file_name = '_'.join(parts[2:])

        if call.from_user.id != user_id and call.from_user.id not in admin_ids:
            bot.answer_callback_query(call.id, B("⚠️ 𝐏𝐞𝐫𝐦𝐢𝐬𝐬𝐢𝐨𝐧 𝐝𝐞𝐧𝐢𝐞𝐝"), show_alert=True)
            return

        if is_bot_running(user_id, file_name):
            bot.answer_callback_query(call.id, B("✅ 𝐀𝐥𝐫𝐞𝐚𝐝𝐲 𝐫𝐮𝐧𝐧𝐢𝐧𝐠"), show_alert=True)
            return

        user_folder = get_user_folder(user_id)
        file_path = os.path.join(user_folder, file_name)

        if not os.path.exists(file_path):
            bot.answer_callback_query(call.id, B("❌ 𝐅𝐢𝐥𝐞 𝐧𝐨𝐭 𝐟𝐨𝐮𝐧𝐝"), show_alert=True)
            return

        file_type = next((ft for fn, ft in user_files.get(user_id, []) if fn == file_name), 'py')

        bot.answer_callback_query(call.id, B("🚀 𝐒𝐭𝐚𝐫𝐭𝐢𝐧𝐠 𝐬𝐜𝐫𝐢𝐩𝐭..."))

        if file_type == 'py':
            threading.Thread(target=run_script,
                             args=(file_path, user_id, user_folder, file_name, call.message)).start()
        elif file_type == 'js':
            threading.Thread(target=run_js_script,
                             args=(file_path, user_id, user_folder, file_name, call.message)).start()
        else:
            bot.answer_callback_query(call.id, B("❌ 𝐔𝐧𝐬𝐮𝐩𝐩𝐨𝐫𝐭𝐞𝐝 𝐟𝐢𝐥𝐞 𝐭𝐲𝐩𝐞"), show_alert=True)
    except Exception as e:
        logger.error(f"❌ start_bot_callback error: {e}")
        bot.answer_callback_query(call.id, B("❌ 𝐄𝐫𝐫𝐨𝐫 𝐬𝐭𝐚𝐫𝐭𝐢𝐧𝐠 𝐬𝐜𝐫𝐢𝐩𝐭"))

def stop_bot_callback(call):
    try:
        parts = call.data.split('_')
        user_id = int(parts[1])
        file_name = '_'.join(parts[2:])

        if call.from_user.id != user_id and call.from_user.id not in admin_ids:
            bot.answer_callback_query(call.id, B("⚠️ 𝐏𝐞𝐫𝐦𝐢𝐬𝐬𝐢𝐨𝐧 𝐝𝐞𝐧𝐢𝐞𝐝"), show_alert=True)
            return

        if not is_bot_running(user_id, file_name):
            bot.answer_callback_query(call.id, B("✅ 𝐀𝐥𝐫𝐞𝐚𝐝𝐲 𝐬𝐭𝐨𝐩𝐩𝐞𝐝"), show_alert=True)
            return

        script_key = f"{user_id}_{file_name}"
        if script_key in bot_scripts:
            kill_process_tree(bot_scripts[script_key])
            del bot_scripts[script_key]

        bot.answer_callback_query(call.id, B("🛑 𝐒𝐭𝐨𝐩𝐩𝐞𝐝 𝐬𝐜𝐫𝐢𝐩𝐭"))
        bot.edit_message_reply_markup(
            call.message.chat.id, call.message.message_id,
            reply_markup=create_control_buttons(user_id, file_name, False)
        )
    except Exception as e:
        logger.error(f"❌ stop_bot_callback error: {e}")
        bot.answer_callback_query(call.id, B("❌ 𝐄𝐫𝐫𝐨𝐫 𝐬𝐭𝐨𝐩𝐩𝐢𝐧𝐠 𝐬𝐜𝐫𝐢𝐩𝐭"))

def restart_bot_callback(call):
    try:
        parts = call.data.split('_')
        user_id = int(parts[1])
        file_name = '_'.join(parts[2:])

        if call.from_user.id != user_id and call.from_user.id not in admin_ids:
            bot.answer_callback_query(call.id, B("⚠️ 𝐏𝐞𝐫𝐦𝐢𝐬𝐬𝐢𝐨𝐧 𝐝𝐞𝐧𝐢𝐞𝐝"), show_alert=True)
            return

        if is_bot_running(user_id, file_name):
            script_key = f"{user_id}_{file_name}"
            if script_key in bot_scripts:
                kill_process_tree(bot_scripts[script_key])
                del bot_scripts[script_key]
            time.sleep(1)

        user_folder = get_user_folder(user_id)
        file_path = os.path.join(user_folder, file_name)

        if not os.path.exists(file_path):
            bot.answer_callback_query(call.id, B("❌ 𝐅𝐢𝐥𝐞 𝐧𝐨𝐭 𝐟𝐨𝐮𝐧𝐝"), show_alert=True)
            return

        file_type = next((ft for fn, ft in user_files.get(user_id, []) if fn == file_name), 'py')
        bot.answer_callback_query(call.id, B("🔄 𝐑𝐞𝐬𝐭𝐚𝐫𝐭𝐢𝐧𝐠 𝐬𝐜𝐫𝐢𝐩𝐭..."))

        if file_type == 'py':
            threading.Thread(target=run_script,
                             args=(file_path, user_id, user_folder, file_name, call.message)).start()
        elif file_type == 'js':
            threading.Thread(target=run_js_script,
                             args=(file_path, user_id, user_folder, file_name, call.message)).start()
    except Exception as e:
        logger.error(f"❌ restart_bot_callback error: {e}")
        bot.answer_callback_query(call.id, B("❌ 𝐄𝐫𝐫𝐨𝐫 𝐫𝐞𝐬𝐭𝐚𝐫𝐭𝐢𝐧𝐠 𝐬𝐜𝐫𝐢𝐩𝐭"))

def delete_bot_callback(call):
    try:
        parts = call.data.split('_')
        user_id = int(parts[1])
        file_name = '_'.join(parts[2:])

        if call.from_user.id != user_id and call.from_user.id not in admin_ids:
            bot.answer_callback_query(call.id, B("⚠️ 𝐏𝐞𝐫𝐦𝐢𝐬𝐬𝐢𝐨𝐧 𝐝𝐞𝐧𝐢𝐞𝐝"), show_alert=True)
            return

        if is_bot_running(user_id, file_name):
            script_key = f"{user_id}_{file_name}"
            if script_key in bot_scripts:
                kill_process_tree(bot_scripts[script_key])
                del bot_scripts[script_key]

        user_folder = get_user_folder(user_id)
        file_path = os.path.join(user_folder, file_name)
        log_path = os.path.join(user_folder, f"{os.path.splitext(file_name)[0]}.log")

        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(log_path):
            os.remove(log_path)

        remove_user_file_db(user_id, file_name)
        bot.answer_callback_query(call.id, B("🗑️ 𝐅𝐢𝐥𝐞 𝐝𝐞𝐥𝐞𝐭𝐞𝐝"))
        check_files_callback(call)
    except Exception as e:
        logger.error(f"❌ delete_bot_callback error: {e}")
        bot.answer_callback_query(call.id, B("❌ 𝐄𝐫𝐫𝐨𝐫 𝐝𝐞𝐥𝐞𝐭𝐢𝐧𝐠 𝐟𝐢𝐥𝐞"))

def logs_bot_callback(call):
    try:
        parts = call.data.split('_')
        user_id = int(parts[1])
        file_name = '_'.join(parts[2:])

        if call.from_user.id != user_id and call.from_user.id not in admin_ids:
            bot.answer_callback_query(call.id, B("⚠️ 𝐏𝐞𝐫𝐦𝐢𝐬𝐬𝐢𝐨𝐧 𝐝𝐞𝐧𝐢𝐞𝐝"), show_alert=True)
            return

        user_folder = get_user_folder(user_id)
        log_path = os.path.join(user_folder, f"{os.path.splitext(file_name)[0]}.log")

        if not os.path.exists(log_path):
            bot.answer_callback_query(call.id, B("📭 𝐍𝐨 𝐥𝐨𝐠𝐬 𝐟𝐨𝐮𝐧𝐝"), show_alert=True)
            return

        with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
            log_content = f.read()

        if len(log_content) > 3000:
            log_content = "...\n" + log_content[-3000:]

        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id,
                         B(f"📜 𝐋𝐨𝐠𝐬 𝐟𝐨𝐫 `{file_name}`:\n```\n{log_content}\n```"),
                         parse_mode='Markdown')
    except Exception as e:
        logger.error(f"❌ logs_bot_callback error: {e}")
        bot.answer_callback_query(call.id, B("❌ 𝐄𝐫𝐫𝐨𝐫 𝐠𝐞𝐭𝐭𝐢𝐧𝐠 𝐥𝐨𝐠𝐬"))

def stats_callback(call):
    user_id = call.from_user.id
    total_users = len(active_users)
    total_files = sum(len(files) for files in user_files.values())
    running_scripts = len([k for k, v in bot_scripts.items() if is_bot_running(v['user_id'], v['file_name'])])

    stats_text = B(f"""
📊 𝐒𝐘𝐒𝐓𝐄𝐌 𝐒𝐓𝐀𝐓𝐈𝐒𝐓𝐈𝐂𝐒

👥 𝐓𝐨𝐭𝐚𝐥 𝐔𝐬𝐞𝐫𝐬: {total_users}
📁 𝐓𝐨𝐭𝐚𝐥 𝐅𝐢𝐥𝐞𝐬: {total_files}
🟢 𝐑𝐮𝐧𝐧𝐢𝐧𝐠 𝐒𝐜𝐫𝐢𝐩𝐭𝐬: {running_scripts}
🔒 𝐁𝐨𝐭 𝐒𝐭𝐚𝐭𝐮𝐬: {'🔴 𝐋𝐨𝐜𝐤𝐞𝐝' if bot_locked else '🟢 𝐔𝐧𝐥𝐨𝐜𝐤𝐞𝐝'}

🎫 𝐓𝐢𝐞𝐫 𝐃𝐢𝐬𝐭𝐫𝐢𝐛𝐮𝐭𝐢𝐨𝐧:
• 𝐅𝐑𝐄𝐄: {len([uid for uid in active_users if get_user_tier(uid) == 'free'])}
• 𝐏𝐑𝐄𝐌𝐈𝐔𝐌: {len([uid for uid in active_users if get_user_tier(uid) == 'premium'])}
• 𝐎𝐖𝐍𝐄𝐑/𝐀𝐃𝐌𝐈𝐍: {len([uid for uid in active_users if get_user_tier(uid) == 'owner'])}
""")
    back_markup = types.InlineKeyboardMarkup()
    back_markup.add(types.InlineKeyboardButton(B("🔙 𝐁𝐚𝐜𝐤"), callback_data='back_to_main'))
    bot.answer_callback_query(call.id)
    bot.edit_message_text(stats_text, call.message.chat.id, call.message.message_id,
                          parse_mode='Markdown', reply_markup=back_markup)

def profile_callback(call):
    user_id = call.from_user.id
    tier = get_user_tier(user_id)
    tier_info = TIER_SYSTEM[tier]

    profile_text = B(f"""
👤 𝐏𝐑𝐎𝐅𝐈𝐋𝐄

🆔 𝐔𝐬𝐞𝐫 𝐈𝐃: `{user_id}`
👤 𝐍𝐚𝐦𝐞: {call.from_user.first_name}
🎫 𝐓𝐢𝐞𝐫: {tier_info['icon']} {tier_info['name']}
📁 𝐅𝐢𝐥𝐞𝐬: {get_user_file_count(user_id)}/{get_user_file_limit(user_id)}
🟢 𝐑𝐮𝐧𝐧𝐢𝐧𝐠: {len([1 for f in user_files.get(user_id, []) if is_bot_running(user_id, f[0])])}
""")
    back_markup = types.InlineKeyboardMarkup()
    back_markup.add(types.InlineKeyboardButton(B("🔙 𝐁𝐚𝐜𝐤"), callback_data='back_to_main'))
    bot.answer_callback_query(call.id)
    bot.edit_message_text(profile_text, call.message.chat.id, call.message.message_id,
                          parse_mode='Markdown', reply_markup=back_markup)

def admin_panel_callback(call):
    if call.from_user.id not in admin_ids:
        bot.answer_callback_query(call.id, B("⚠️ 𝐀𝐝𝐦𝐢𝐧 𝐩𝐞𝐫𝐦𝐢𝐬𝐬𝐢𝐨𝐧𝐬 𝐫𝐞𝐪𝐮𝐢𝐫𝐞𝐝"), show_alert=True)
        return
    bot.answer_callback_query(call.id)
    bot.edit_message_text(B("👑 𝐀𝐃𝐌𝐈𝐍 𝐏𝐀𝐍𝐄𝐋"),
                          call.message.chat.id, call.message.message_id,
                          reply_markup=create_admin_panel())

def broadcast_callback(call):
    if call.from_user.id not in admin_ids:
        bot.answer_callback_query(call.id, B("⚠️ 𝐀𝐝𝐦𝐢𝐧 𝐩𝐞𝐫𝐦𝐢𝐬𝐬𝐢𝐨𝐧𝐬 𝐫𝐞𝐪𝐮𝐢𝐫𝐞𝐝"), show_alert=True)
        return
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, B("📢 𝐒𝐞𝐧𝐝 𝐭𝐡𝐞 𝐦𝐞𝐬𝐬𝐚𝐠𝐞 𝐲𝐨𝐮 𝐰𝐚𝐧𝐭 𝐭𝐨 𝐛𝐫𝐨𝐚𝐝𝐜𝐚𝐬𝐭."))
    bot.register_next_step_handler(call.message, process_broadcast_message)

def lock_bot_callback(call):
    if call.from_user.id not in admin_ids:
        bot.answer_callback_query(call.id, B("⚠️ 𝐀𝐝𝐦𝐢𝐧 𝐩𝐞𝐫𝐦𝐢𝐬𝐬𝐢𝐨𝐧𝐬 𝐫𝐞𝐪𝐮𝐢𝐫𝐞𝐝"), show_alert=True)
        return
    global bot_locked
    bot_locked = True
    bot.answer_callback_query(call.id, B("🔒 𝐁𝐨𝐭 𝐥𝐨𝐜𝐤𝐞𝐝"))
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                  reply_markup=create_main_menu_inline(call.from_user.id))

def unlock_bot_callback(call):
    if call.from_user.id not in admin_ids:
        bot.answer_callback_query(call.id, B("⚠️ 𝐀𝐝𝐦𝐢𝐧 𝐩𝐞𝐫𝐦𝐢𝐬𝐬𝐢𝐨𝐧𝐬 𝐫𝐞𝐪𝐮𝐢𝐫𝐞𝐝"), show_alert=True)
        return
    global bot_locked
    bot_locked = False
    bot.answer_callback_query(call.id, B("🔓 𝐁𝐨𝐭 𝐮𝐧𝐥𝐨𝐜𝐤𝐞𝐝"))
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                  reply_markup=create_main_menu_inline(call.from_user.id))

def analytics_callback(call):
    if call.from_user.id not in admin_ids:
        bot.answer_callback_query(call.id, B("⚠️ 𝐀𝐝𝐦𝐢𝐧 𝐩𝐞𝐫𝐦𝐢𝐬𝐬𝐢𝐨𝐧𝐬 𝐫𝐞𝐪𝐮𝐢𝐫𝐞𝐝"), show_alert=True)
        return
    total_users = len(active_users)
    total_files = sum(len(files) for files in user_files.values())
    running_scripts = len([k for k, v in bot_scripts.items() if is_bot_running(v['user_id'], v['file_name'])])

    total_storage = 0
    for uid in user_files:
        user_folder = get_user_folder(uid)
        if os.path.exists(user_folder):
            for root, dirs, fls in os.walk(user_folder):
                for fl in fls:
                    total_storage += os.path.getsize(os.path.join(root, fl))
    total_storage_mb = round(total_storage / (1024 * 1024), 2)

    analytics_text = B(f"""
📈 𝐀𝐃𝐕𝐀𝐍𝐂𝐄𝐃 𝐀𝐍𝐀𝐋𝐘𝐓𝐈𝐂𝐒

👥 𝐔𝐬𝐞𝐫 𝐌𝐞𝐭𝐫𝐢𝐜𝐬:
• 𝐓𝐨𝐭𝐚𝐥 𝐔𝐬𝐞𝐫𝐬: {total_users}

📁 𝐒𝐭𝐨𝐫𝐚𝐠𝐞 𝐀𝐧𝐚𝐥𝐲𝐭𝐢𝐜𝐬:
• 𝐓𝐨𝐭𝐚𝐥 𝐅𝐢𝐥𝐞𝐬: {total_files}
• 𝐓𝐨𝐭𝐚𝐥 𝐒𝐭𝐨𝐫𝐚𝐠𝐞: {total_storage_mb} 𝐌𝐁
• 𝐀𝐯𝐠 𝐅𝐢𝐥𝐞𝐬/𝐔𝐬𝐞𝐫: {round(total_files/max(total_users, 1), 1)}

🚀 𝐏𝐞𝐫𝐟𝐨𝐫𝐦𝐚𝐧𝐜𝐞:
• 𝐑𝐮𝐧𝐧𝐢𝐧𝐠 𝐒𝐜𝐫𝐢𝐩𝐭𝐬: {running_scripts}

🎫 𝐑𝐞𝐯𝐞𝐧𝐮𝐞 𝐌𝐞𝐭𝐫𝐢𝐜𝐬:
• 𝐏𝐫𝐞𝐦𝐢𝐮𝐦 𝐔𝐬𝐞𝐫𝐬: {len([uid for uid in active_users if get_user_tier(uid) == 'premium'])}
""")
    back_markup = types.InlineKeyboardMarkup()
    back_markup.add(types.InlineKeyboardButton(B("🔙 𝐁𝐚𝐜𝐤"), callback_data='back_to_main'))
    bot.answer_callback_query(call.id)
    bot.edit_message_text(analytics_text, call.message.chat.id, call.message.message_id,
                          parse_mode='Markdown', reply_markup=back_markup)

def add_admin_callback(call):
    if call.from_user.id != OWNER_ID:
        bot.answer_callback_query(call.id, B("⚠️ 𝐎𝐧𝐥𝐲 𝐨𝐰𝐧𝐞𝐫 𝐜𝐚𝐧 𝐚𝐝𝐝 𝐚𝐝𝐦𝐢𝐧𝐬"), show_alert=True)
        return
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, B("👑 𝐄𝐧𝐭𝐞𝐫 𝐮𝐬𝐞𝐫 𝐈𝐃 𝐭𝐨 𝐚𝐝𝐝 𝐚𝐬 𝐚𝐝𝐦𝐢𝐧:"))
    bot.register_next_step_handler(call.message, process_add_admin)

def process_add_admin(message):
    if message.from_user.id != OWNER_ID:
        return
    try:
        new_admin_id = int(message.text.strip())
        add_admin_to_db(new_admin_id, message.from_user.id)
        admin_ids.add(new_admin_id)
        bot.reply_to(message, B(f"✅ 𝐔𝐬𝐞𝐫 `{new_admin_id}` 𝐚𝐝𝐝𝐞𝐝 𝐚𝐬 𝐚𝐝𝐦𝐢𝐧."))
    except ValueError:
        bot.reply_to(message, B("❌ 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐮𝐬𝐞𝐫 𝐈𝐃."))
    except Exception as e:
        bot.reply_to(message, B(f"❌ 𝐄𝐫𝐫𝐨𝐫: {str(e)}"))

def remove_admin_callback(call):
    if call.from_user.id != OWNER_ID:
        bot.answer_callback_query(call.id, B("⚠️ 𝐎𝐧𝐥𝐲 𝐨𝐰𝐧𝐞𝐫 𝐜𝐚𝐧 𝐫𝐞𝐦𝐨𝐯𝐞 𝐚𝐝𝐦𝐢𝐧𝐬"), show_alert=True)
        return
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, B("👑 𝐄𝐧𝐭𝐞𝐫 𝐮𝐬𝐞𝐫 𝐈𝐃 𝐭𝐨 𝐫𝐞𝐦𝐨𝐯𝐞 𝐚𝐝𝐦𝐢𝐧:"))
    bot.register_next_step_handler(call.message, process_remove_admin)

def process_remove_admin(message):
    if message.from_user.id != OWNER_ID:
        return
    try:
        target_id = int(message.text.strip())
        if target_id == OWNER_ID:
            bot.reply_to(message, B("❌ 𝐂𝐚𝐧𝐧𝐨𝐭 𝐫𝐞𝐦𝐨𝐯𝐞 𝐨𝐰𝐧𝐞𝐫."))
            return
        remove_admin_from_db(target_id)
        admin_ids.discard(target_id)
        bot.reply_to(message, B(f"✅ 𝐔𝐬𝐞𝐫 `{target_id}` 𝐫𝐞𝐦𝐨𝐯𝐞𝐝 𝐟𝐫𝐨𝐦 𝐚𝐝𝐦𝐢𝐧𝐬."))
    except ValueError:
        bot.reply_to(message, B("❌ 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐮𝐬𝐞𝐫 𝐈𝐃."))
    except Exception as e:
        bot.reply_to(message, B(f"❌ 𝐄𝐫𝐫𝐨𝐫: {str(e)}"))

def list_admins_callback(call):
    if call.from_user.id not in admin_ids:
        bot.answer_callback_query(call.id, B("⚠️ 𝐀𝐝𝐦𝐢𝐧 𝐩𝐞𝐫𝐦𝐢𝐬𝐬𝐢𝐨𝐧𝐬 𝐫𝐞𝐪𝐮𝐢𝐫𝐞𝐝"), show_alert=True)
        return
    admin_list = "\n".join([f"• `{aid}` {'👑' if aid == OWNER_ID else ''}" for aid in sorted(admin_ids)])
    back_markup = types.InlineKeyboardMarkup()
    back_markup.add(types.InlineKeyboardButton(B("🔙 𝐁𝐚𝐜𝐤"), callback_data='admin_panel'))
    bot.answer_callback_query(call.id)
    bot.edit_message_text(B(f"👑 𝐂𝐮𝐫𝐫𝐞𝐧𝐭 𝐀𝐝𝐦𝐢𝐧𝐬:\n\n{admin_list}"),
                          call.message.chat.id, call.message.message_id,
                          parse_mode='Markdown', reply_markup=back_markup)

def system_stats_callback(call):
    if call.from_user.id not in admin_ids:
        bot.answer_callback_query(call.id, B("⚠️ 𝐀𝐝𝐦𝐢𝐧 𝐩𝐞𝐫𝐦𝐢𝐬𝐬𝐢𝐨𝐧𝐬 𝐫𝐞𝐪𝐮𝐢𝐫𝐞𝐝"), show_alert=True)
        return
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    total_users = len(active_users)
    total_files = sum(len(files) for files in user_files.values())
    running_scripts = len([k for k, v in bot_scripts.items() if is_bot_running(v['user_id'], v['file_name'])])

    stats_text = B(f"""
🖥️ 𝐒𝐘𝐒𝐓𝐄𝐌 𝐒𝐓𝐀𝐓𝐔𝐒

𝐂𝐏𝐔 𝐔𝐬𝐚𝐠𝐞: {cpu_percent}%
𝐌𝐞𝐦𝐨𝐫𝐲: {memory.percent}% ({round(memory.used/(1024**3), 1)}𝐆𝐁 / {round(memory.total/(1024**3), 1)}𝐆𝐁)
𝐃𝐢𝐬𝐤: {disk.percent}% ({round(disk.used/(1024**3), 1)}𝐆𝐁 / {round(disk.total/(1024**3), 1)}𝐆𝐁)

🤖 𝐁𝐎𝐓 𝐒𝐓𝐀𝐓𝐒
𝐔𝐬𝐞𝐫𝐬: {total_users}
𝐅𝐢𝐥𝐞𝐬: {total_files}
𝐑𝐮𝐧𝐧𝐢𝐧𝐠: {running_scripts}
𝐒𝐭𝐚𝐭𝐮𝐬: {'🔴 𝐋𝐨𝐜𝐤𝐞𝐝' if bot_locked else '🟢 𝐔𝐧𝐥𝐨𝐜𝐤𝐞𝐝'}

📊 𝐏𝐄𝐑𝐅𝐎𝐑𝐌𝐀𝐍𝐂𝐄
𝐓𝐡𝐫𝐞𝐚𝐝𝐬: {threading.active_count()}
""")
    back_markup = types.InlineKeyboardMarkup()
    back_markup.add(types.InlineKeyboardButton(B("🔙 𝐁𝐚𝐜𝐤"), callback_data='admin_panel'))
    bot.answer_callback_query(call.id)
    bot.edit_message_text(stats_text, call.message.chat.id, call.message.message_id,
                          reply_markup=back_markup)

def broadcast_confirm_callback(call):
    if call.from_user.id not in admin_ids:
        bot.answer_callback_query(call.id, B("⚠️ 𝐀𝐝𝐦𝐢𝐧 𝐩𝐞𝐫𝐦𝐢𝐬𝐬𝐢𝐨𝐧𝐬 𝐫𝐞𝐪𝐮𝐢𝐫𝐞𝐝"), show_alert=True)
        return
    try:
        original_message = call.message.reply_to_message
        if not original_message:
            bot.answer_callback_query(call.id, B("❌ 𝐂𝐨𝐮𝐥𝐝 𝐧𝐨𝐭 𝐟𝐢𝐧𝐝 𝐨𝐫𝐢𝐠𝐢𝐧𝐚𝐥 𝐦𝐞𝐬𝐬𝐚𝐠𝐞"), show_alert=True)
            return

        bot.answer_callback_query(call.id, B("🚀 𝐒𝐭𝐚𝐫𝐭𝐢𝐧𝐠 𝐛𝐫𝐨𝐚𝐝𝐜𝐚𝐬𝐭..."))
        sent = 0
        failed = 0

        for uid in list(active_users):
            try:
                if original_message.text:
                    bot.send_message(uid, original_message.text)
                elif original_message.caption:
                    if original_message.photo:
                        bot.send_photo(uid, original_message.photo[-1].file_id, caption=original_message.caption)
                    elif original_message.video:
                        bot.send_video(uid, original_message.video.file_id, caption=original_message.caption)
                    elif original_message.document:
                        bot.send_document(uid, original_message.document.file_id, caption=original_message.caption)
                sent += 1
            except:
                failed += 1
            time.sleep(0.1)

        bot.edit_message_text(
            B(f"✅ 𝐁𝐫𝐨𝐚𝐝𝐜𝐚𝐬𝐭 𝐜𝐨𝐦𝐩𝐥𝐞𝐭𝐞!\n\n📤 𝐒𝐞𝐧𝐭: {sent}\n❌ 𝐅𝐚𝐢𝐥𝐞𝐝: {failed}\n👥 𝐓𝐨𝐭𝐚𝐥: {len(active_users)}"),
            call.message.chat.id, call.message.message_id
        )
    except Exception as e:
        logger.error(f"❌ broadcast_confirm_callback error: {e}")
        bot.answer_callback_query(call.id, B("❌ 𝐄𝐫𝐫𝐨𝐫 𝐢𝐧 𝐛𝐫𝐨𝐚𝐝𝐜𝐚𝐬𝐭"))

def broadcast_cancel_callback(call):
    bot.answer_callback_query(call.id, B("❌ 𝐁𝐫𝐨𝐚𝐝𝐜𝐚𝐬𝐭 𝐜𝐚𝐧𝐜𝐞𝐥𝐥𝐞𝐝"))
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass

def back_to_main_callback(call):
    user_id = call.from_user.id
    tier = get_user_tier(user_id)
    tier_info = TIER_SYSTEM[tier]

    welcome_text = B(f"""
┏━━━━━━━━━━━━━━━━━━━━━━┓
┃   🚀 𝐈𝐍𝐒𝐀𝐍𝐄 𝐁𝐎𝐓 𝐇𝐎𝐒𝐓𝐈𝐍𝐆   ┃
┃      𝐕𝐄𝐑𝐒𝐈𝐎𝐍 𝟑.𝟐     ┃
┗━━━━━━━━━━━━━━━━━━━━━━┛

👤 𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐛𝐚𝐜𝐤, {call.from_user.first_name}!
🆔 𝐔𝐬𝐞𝐫 𝐈𝐃: `{user_id}`
🎫 𝐓𝐢𝐞𝐫: {tier_info['icon']} {tier_info['name']}
📁 𝐅𝐢𝐥𝐞𝐬: {get_user_file_count(user_id)}/{get_user_file_limit(user_id)}

𝐔𝐬𝐞 𝐛𝐮𝐭𝐭𝐨𝐧𝐬 𝐛𝐞𝐥𝐨𝐰 𝐭𝐨 𝐧𝐚𝐯𝐢𝐠𝐚𝐭𝐞.
""")
    bot.answer_callback_query(call.id)
    bot.edit_message_text(welcome_text,
                          call.message.chat.id, call.message.message_id,
                          reply_markup=create_main_menu_inline(user_id),
                          parse_mode='Markdown')

def modules_callback(call):
    bot.answer_callback_query(call.id)
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton(B("🔙 𝐁𝐚𝐜𝐤"), callback_data="back_to_main"))
    bot.edit_message_text(B("""🐍 𝐌𝐎𝐃𝐔𝐋𝐄𝐒 𝐌𝐀𝐍𝐀𝐆𝐄𝐑

📦 𝐀𝐩𝐧𝐚 module name bhejo install karne ke liye
𝐄𝐱𝐚𝐦𝐩𝐥𝐞: requests, flask, numpy

𝐁𝐨𝐭 automatically install karega!"""),
                           call.message.chat.id, call.message.message_id,
                           reply_markup=markup)


# ================================
# 🗄️ MANAGE DATABASE FEATURE
# ================================
def show_manage_db(message):
    """Show all files in RAM."""
    if message.from_user.id not in admin_ids:
        return
    all_files = []
    for uid, files in user_files.items():
        for fn, ft in files:
            all_files.append((uid, fn, ft, ""))

    if not all_files:
        bot.reply_to(message, B("📭 No files in database."))
        return

    markup = types.InlineKeyboardMarkup(row_width=1)
    for uid, fname, ftype, uploaded in all_files:
        short_uid = str(uid)[-5:]
        label = f"📄 {fname} (User: ...{short_uid})"
        markup.add(types.InlineKeyboardButton(
            B(label), callback_data=f'dbfile_{uid}_{fname}'
        ))
    markup.add(types.InlineKeyboardButton(B("🔙 Back"), callback_data='back_to_main'))

    bot.reply_to(message,
                 B(f"🗄️ DATABASE MANAGER\n\nTotal Files: {len(all_files)}"),
                 reply_markup=markup)

def manage_db_callback(call):
    """Inline button for Manage DB."""
    if call.from_user.id not in admin_ids:
        bot.answer_callback_query(call.id, B("⚠️ Admin only"), show_alert=True)
        return
    all_files = []
    for uid, files in user_files.items():
        for fn, ft in files:
            all_files.append((uid, fn, ft, ""))

    if not all_files:
        bot.answer_callback_query(call.id, B("📭 No files in database"), show_alert=True)
        return

    markup = types.InlineKeyboardMarkup(row_width=1)
    for uid, fname, ftype, uploaded in all_files:
        short_uid = str(uid)[-5:]
        label = f"📄 {fname} (...{short_uid})"
        markup.add(types.InlineKeyboardButton(
            B(label), callback_data=f'dbfile_{uid}_{fname}'
        ))
    markup.add(types.InlineKeyboardButton(B("🔙 Back"), callback_data='back_to_main'))

    bot.answer_callback_query(call.id)
    bot.edit_message_text(
        B(f"🗄️ DATABASE MANAGER\n\nTotal Files in MongoDB: {len(all_files)}"),
        call.message.chat.id, call.message.message_id,
        reply_markup=markup
    )

def dbfile_detail_callback(call):
    """Show file details from DB."""
    if call.from_user.id not in admin_ids:
        bot.answer_callback_query(call.id)
        return
    try:
        parts = call.data.split('_', 2)
        uid = int(parts[1])
        fname = parts[2]
    except:
        bot.answer_callback_query(call.id, "❌ Error", show_alert=True)
        return

    # Find in RAM
    files_for_user = user_files.get(uid, [])
    row = next(((fn, ft) for fn, ft in files_for_user if fn == fname), None)

    if not row:
        bot.answer_callback_query(call.id, B("❌ File not found"), show_alert=True)
        return

    file_name, file_type, uploaded_at = row[0], row[1], ""
    is_running = is_bot_running(uid, file_name)
    status = "🟢 Running" if is_running else "🔴 Stopped"

    # Format uploaded time
    try:
        dt = datetime.fromisoformat(uploaded_at)
        uploaded_fmt = dt.strftime("%d %b %Y, %I:%M %p")
    except:
        uploaded_fmt = uploaded_at or "Unknown"

    # Running time
    script_key = f"{uid}_{file_name}"
    run_time = "Not running"
    if script_key in bot_scripts:
        start = bot_scripts[script_key].get('start_time')
        if start:
            diff = datetime.now() - start
            h, m = divmod(int(diff.total_seconds()) // 60, 60)
            run_time = f"{h}h {m}m"

    detail_text = f"""📄 FILE DETAILS

Name: {file_name}
Type: {file_type.upper()}
User ID: {uid}
Uploaded: {uploaded_fmt}
Running Time: {run_time}
Status: {status}"""

    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton(
        B("🗑️ Delete Full Database"), callback_data=f'dbdelete_{uid}_{fname}'
    ))
    markup.add(types.InlineKeyboardButton(B("🔙 Back"), callback_data='manage_db'))

    bot.answer_callback_query(call.id)
    bot.edit_message_text(
        B(detail_text),
        call.message.chat.id, call.message.message_id,
        reply_markup=markup
    )

def dbdelete_callback(call):
    """Permanently delete file from Supabase DB."""
    if call.from_user.id not in admin_ids:
        bot.answer_callback_query(call.id)
        return
    try:
        parts = call.data.split('_', 2)
        uid = int(parts[1])
        fname = parts[2]
    except:
        bot.answer_callback_query(call.id, "❌ Error", show_alert=True)
        return

    # Stop process if running
    script_key = f"{uid}_{fname}"
    if script_key in bot_scripts:
        kill_process_tree(bot_scripts[script_key])
        del bot_scripts[script_key]

    # Delete from Supabase
    remove_user_file_db(uid, fname)

    # Delete file from disk
    user_folder = get_user_folder(uid)
    file_path = os.path.join(user_folder, fname)
    log_path = os.path.join(user_folder, f"{os.path.splitext(fname)[0]}.log")
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(log_path):
            os.remove(log_path)
    except:
        pass

    bot.answer_callback_query(call.id, B(f"✅ {fname} permanently deleted!"), show_alert=True)
    manage_db_callback(call)

# ================================
# 𝐂𝐋𝐄𝐀𝐍𝐔𝐏
# ================================
def cleanup():
    logger.warning("🔴 𝐒𝐡𝐮𝐭𝐭𝐢𝐧𝐠 𝐝𝐨𝐰𝐧... 𝐂𝐥𝐞𝐚𝐧𝐢𝐧𝐠 𝐮𝐩 𝐩𝐫𝐨𝐜𝐞𝐬𝐬𝐞𝐬")
    for script_key, script_info in list(bot_scripts.items()):
        try:
            kill_process_tree(script_info)
        except:
            pass
    logger.info("✅ 𝐂𝐥𝐞𝐚𝐧𝐮𝐩 𝐜𝐨𝐦𝐩𝐥𝐞𝐭𝐞")

atexit.register(cleanup)

# ================================
# 𝐌𝐀𝐈𝐍
# ================================

def cleanup_dead_processes():
    """Remove dead processes + trim logs every 2 minutes."""
    while True:
        try:
            time.sleep(120)
            dead_keys = []
            for key in list(bot_scripts.keys()):
                try:
                    uid = int(key.split('_')[0])
                    fname = key.split('_', 1)[1]
                    if not is_bot_running(uid, fname):
                        dead_keys.append(key)
                except:
                    dead_keys.append(key)
            for key in dead_keys:
                bot_scripts.pop(key, None)
            # Trim log files
            if os.path.exists(UPLOAD_BOTS_DIR):
                for ud in os.listdir(UPLOAD_BOTS_DIR):
                    up = os.path.join(UPLOAD_BOTS_DIR, ud)
                    if not os.path.isdir(up): continue
                    for fn in os.listdir(up):
                        if not fn.endswith('.log'): continue
                        lp = os.path.join(up, fn)
                        try:
                            with open(lp,'r',encoding='utf-8',errors='ignore') as f:
                                lines = f.readlines()
                            if len(lines) > 500:
                                with open(lp,'w',encoding='utf-8') as f:
                                    f.writelines(lines[-500:])
                        except: pass
        except Exception as e:
            logger.error(f"Cleanup error: {e}")


def auto_restart_stopped_scripts():
    """Auto-restart scripts that stopped unexpectedly every 60 seconds."""
    while True:
        try:
            time.sleep(60)
            for key, info in list(bot_scripts.items()):
                try:
                    uid = info.get('user_id')
                    fname = info.get('file_name')
                    ftype = info.get('type', 'py')
                    script_path = info.get('script_path')

                    if not uid or not fname or not script_path:
                        continue
                    if not os.path.exists(script_path):
                        continue
                    if is_bot_running(uid, fname):
                        continue

                    # Script stopped — restart it
                    logger.info(f"🔄 Auto-restarting: {fname} for {uid}")
                    user_folder = get_user_folder(uid)
                    log_path = os.path.join(user_folder, f"{os.path.splitext(fname)[0]}.log")
                    log_file = open(log_path, 'a', encoding='utf-8', errors='ignore')

                    if ftype == 'py':
                        process = subprocess.Popen(
                            [sys.executable, script_path],
                            cwd=user_folder,
                            stdout=log_file, stderr=log_file,
                            stdin=subprocess.PIPE,
                            encoding='utf-8', errors='ignore'
                        )
                    else:
                        process = subprocess.Popen(
                            ['node', script_path],
                            cwd=user_folder,
                            stdout=log_file, stderr=log_file,
                            stdin=subprocess.PIPE,
                            encoding='utf-8', errors='ignore'
                        )

                    bot_scripts[key]['process'] = process
                    bot_scripts[key]['start_time'] = datetime.now()
                    bot_scripts[key]['log_file'] = log_file
                    logger.info(f"✅ Auto-restarted: {fname} PID={process.pid}")

                except Exception as re:
                    logger.error(f"Auto-restart error for {key}: {re}")
        except Exception as e:
            logger.error(f"Auto-restart loop error: {e}")

if __name__ == '__main__':
    logger.info("=" * 50)
    logger.info("🚀 𝐈𝐍𝐒𝐀𝐍𝐄 𝐁𝐎𝐓 𝐇𝐎𝐒𝐓𝐈𝐍𝐆 𝐕𝐄𝐑𝐒𝐈𝐎𝐍 𝟑.𝟐 - 𝐂𝐋𝐄𝐀𝐍𝐄𝐃")
    logger.info(f"👑 𝐎𝐰𝐧𝐞𝐫 𝐈𝐃: {OWNER_ID}")
    logger.info(f"🛡️ 𝐀𝐝𝐦𝐢𝐧𝐬: {len(admin_ids)}")
    logger.info(f"👥 𝐀𝐜𝐭𝐢𝐯𝐞 𝐔𝐬𝐞𝐫𝐬: {len(active_users)}")
    logger.info(f"📁 𝐓𝐨𝐭𝐚𝐥 𝐅𝐢𝐥𝐞𝐬: {sum(len(files) for files in user_files.values())}")
    logger.info("📊 𝐃𝐁: 𝐑𝐀𝐌 𝐌𝐎𝐃𝐄 - 𝐅𝐀𝐒𝐓")
    logger.info("=" * 50)

    try:
        bot_username = bot.get_me().username
        logger.info(f"🤖 𝐁𝐨𝐭: @{bot_username}")
    except Exception as e:
        logger.error(f"❌ 𝐁𝐨𝐭 𝐮𝐬𝐞𝐫𝐧𝐚𝐦𝐞 𝐞𝐫𝐫𝐨𝐫: {e}")

    threading.Thread(target=cleanup_dead_processes, daemon=True).start()
    threading.Thread(target=auto_restart_stopped_scripts, daemon=True).start()
    threading.Thread(target=cleanup_dead_processes, daemon=True).start()
    threading.Thread(target=auto_restart_stopped_scripts, daemon=True).start()
    keep_alive()

    logger.info("🤖 𝐒𝐭𝐚𝐫𝐭𝐢𝐧𝐠 𝐛𝐨𝐭 𝐩𝐨𝐥𝐥𝐢𝐧𝐠...")

    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=30)
        except requests.exceptions.ReadTimeout:
            logger.warning("⚠️ 𝐑𝐞𝐚𝐝 𝐓𝐢𝐦𝐞𝐨𝐮𝐭. 𝐑𝐞𝐬𝐭𝐚𝐫𝐭𝐢𝐧𝐠 𝐢𝐧 𝟓𝐬...")
            time.sleep(5)
        except requests.exceptions.ConnectionError as ce:
            logger.error(f"⚠️ 𝐂𝐨𝐧𝐧𝐞𝐜𝐭𝐢𝐨𝐧 𝐄𝐫𝐫𝐨𝐫: {ce}. 𝐑𝐞𝐭𝐫𝐲𝐢𝐧𝐠 𝐢𝐧 𝟏𝟓𝐬...")
            time.sleep(15)
        except Exception as e:
            logger.critical(f"💥 𝐔𝐧𝐫𝐞𝐜𝐨𝐯𝐞𝐫𝐚𝐛𝐥𝐞 𝐞𝐫𝐫𝐨𝐫: {e}", exc_info=True)
            logger.info("🔄 𝐑𝐞𝐬𝐭𝐚𝐫𝐭𝐢𝐧𝐠 𝐢𝐧 𝟑𝟎𝐬...")
            time.sleep(30)
        finally:
            logger.warning("🔴 𝐏𝐨𝐥𝐥𝐢𝐧𝐠 𝐬𝐭𝐨𝐩𝐩𝐞𝐝. 𝐑𝐞𝐬𝐭𝐚𝐫𝐭𝐢𝐧𝐠...")
            time.sleep(1)
