import os
import threading
from flask import Flask
import telebot
from telebot import types
import sqlite3
import random
import datetime
import time
import json
import base64
import urllib.request

# ⚠️ توکن رباتت رو اینجا بین دوتا کوتیشن بذار
BOT_TOKEN = "8735994962:AAEfZRriGcaIhUkIGj8QcwVTd9zfGV2mDWM"
SUPER_ADMIN_ID = 8639658675

CLEAN_IPS = ["8.34.70.64:2408", "8.6.112.224:2408", "188.114.98.12:2408", "8.34.70.120:2408", "8.35.211.2:2408", "188.114.96.70:2408", "188.114.99.75:2408", "8.39.214.218:2408", "188.114.99.6:2408", "8.34.70.169:2408"]
RANDOM_NAMES = ["Ghost-Gaming", "Cloud-Ninja", "Warp-Speed", "Pro-Config", "Shadow-Net", "Turbo-Ping", "VIP-Wire", "Smart-Link", "Ultra-Game", "Fast-Warp"]

JUNK_JC = "6"
JUNK_JMIN = "10"
JUNK_JMAX = "50"
JUNK_I1 = "<b 0xc10000000114367096bb0fb3f58f3a3fb8aaacd61d63a1c8a40e14f7374b8a62dccba6431716c3abf6f5afbcfb39bd008000047c32e268567c652e6f4db58bff759bc8c5aaca183b87cb4d22938fe7d8dca22a679a79e4d9ee62e4bbb3a380dd78d4e8e48f26b38a1d42d76b371a5a9a0444827a69d1ab5872a85749f65a4104e931740b4dc1e2dd77733fc7fac4f93011cd622f2bb47e85f71992e2d585f8dc765a7a12ddeb879746a267393ad023d267c4bd79f258703e27345155268bd3cc0506ebd72e2e3c6b5b0f005299cd94b67ddabe30389c4f9b5c2d512dcc298c14f14e9b7f931e1dc397926c31fbb7cebfc668349c218672501031ecce151d4cb03c4c660b6c6fe7754e75446cd7de09a8c81030c5f6fb377203f551864f3d83e27de7b86499736cbbb549b2f37f436db1cae0a4ea39930f0534aacdd1e3534bc87877e2afabe959ced261f228d6362e6fd277c88c312d966c8b9f67e4a92e757773db0b0862fb8108d1d8fa262a40a1b4171961f0704c8ba314da2482ac8ed9bd28d4b50f7432d89fd800c25a50c5e2f5c0710544fef5273401116aa0572366d8e49ad758fcb29e6a92912e644dbe227c247cb3417eabfab2db16796b2fba420de3b1dc94e8361f1f324a331ddaf1e626553138860757fd0bf687566108b77b70fb9f8f8962eca599c4a70ed373666961a8cb506b96756d9e28b94122b20f16b54f118c0e603ce0b831efea614ad836df6cf9affbdd09596412547496967da758cec9080295d853b0861670b71d9abde0d562b1a6de82782a5b0c14d297f27283a895abc889a5f6703f0e6eb95f67b2da45f150d0d8ab805612d570c2d5cb6997ac3a7756226c2f5c8982ffbd480c5004b0660a3c9468945efde90864019a2b519458724b55d766e16b0da25c0557c01f3c11ddeb024b62e303640e17fdd57dedb3aeb4a2c1b7c93059f9c1d7118d77caac1cd0f6556e46cbc991c1bb16970273dea833d01e5090d061a0c6d25af2415cd2878af97f6d0e7f1f936247b394ecb9bd484da6be936dee9b0b92dc90101a1b4295e97a9772f2263eb09431995aa173df4ca2abd687d87706f0f93eaa5e13cbe3b574fa3cfe94502ace25265778da6960d561381769c24e0cbd7aac73c16f95ae74ff7ec38124f7c722b9cb151d4b6841343f29be8f35145e1b27021056820fed77003df8554b4155716c8cf6049ef5e318481460a8ce3be7c7bfac695255be84dc491c19e9dedc449dd3471728cd2a3ee51324ccb3eef121e3e08f8e18f0006ea8957371d9f2f739f0b89e4db11e5c6430ada61572e589519fbad4498b460ce6e4407fc2d8f2dd4293a50a0cb8fcaaf35cd9a8cc097e3603fbfa08d9036f52b3e7fcce11b83ad28a4ac12dba0395a0cc871cefd1a2856fffb3f28d82ce35cf80579974778bab13d9b3578d8c75a2d196087a2cd439aff2bb33f2db24ac175fff4ed91d36a4cdbfaf3f83074f03894ea40f17034629890da3efdbb41141b38368ab532209b69f057ddc559c19bc8ae62bf3fd564c9a35d9a83d14a95834a92bae6d9a29ae5e8ece07910d16433e4c6230c9bd7d68b47de0de9843988af6dc88b5301820443bd4d0537778bf6b4c1dd067fcf14b81015f2a67c7f2a28f9cb7e0684d3cb4b1c24d9b343122a086611b489532f1c3a26779da1706c6759d96d8ab>"

FALLBACK_PRIVATE_KEY = "AGgMU5NwgOb1W3t4ZV0sFl/xnoj3+vvBN0FFPSLuRGg="
FALLBACK_PUBLIC_KEY = "bmXOC+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo="

bot = telebot.TeleBot(BOT_TOKEN)
user_data = {}
admin_state = {}

def init_db():
    conn = sqlite3.connect('bot_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, first_name TEXT, username TEXT, join_date TEXT, is_admin INTEGER DEFAULT 0, is_banned INTEGER DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS configs (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, config_name TEXT, size TEXT, time TEXT, created_at TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)''')
    c.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('limit', '3')")
    c.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('bot_locked', '0')")
    conn.commit()
    conn.close()

init_db()

def add_user(user_id, first_name, username):
    conn = sqlite3.connect('bot_data.db')
    c = conn.cursor()
    c.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    exists = c.fetchone()
    if not exists:
        c.execute("INSERT INTO users (user_id, first_name, username, join_date) VALUES (?, ?, ?, ?)", (user_id, first_name, username, str(datetime.datetime.now())))
        conn.commit()
        conn.close()
        return True
    conn.commit()
    conn.close()
    return False

def is_admin(user_id):
    if user_id == SUPER_ADMIN_ID: return True
    conn = sqlite3.connect('bot_data.db')
    c = conn.cursor()
    c.execute("SELECT is_admin FROM users WHERE user_id = ?", (user_id,))
    res = c.fetchone()
    conn.close()
    return res and res[0] == 1

def is_banned(user_id):
    conn = sqlite3.connect('bot_data.db')
    c = conn.cursor()
    c.execute("SELECT is_banned FROM users WHERE user_id = ?", (user_id,))
    res = c.fetchone()
    conn.close()
    return res and res[0] == 1

def get_setting(key):
    conn = sqlite3.connect('bot_data.db')
    c = conn.cursor()
    c.execute("SELECT value FROM settings WHERE key = ?", (key,))
    res = c.fetchone()
    conn.close()
    return res[0] if res else '0'

def set_setting(key, value):
    conn = sqlite3.connect('bot_data.db')
    c = conn.cursor()
    c.execute("UPDATE settings SET value = ? WHERE key = ?", (str(value), key))
    conn.commit()
    conn.close()

def save_config(user_id, config_name, size, time):
    conn = sqlite3.connect('bot_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO configs (user_id, config_name, size, time, created_at) VALUES (?, ?, ?, ?, ?)", (user_id, config_name, size, time, str(datetime.datetime.now())))
    conn.commit()
    conn.close()

def check_rate_limit(user_id):
    if is_admin(user_id): return True
    limit = int(get_setting('limit'))
    if limit == 0: return False
    conn = sqlite3.connect('bot_data.db')
    c = conn.cursor()
    yesterday = str(datetime.datetime.now() - datetime.timedelta(days=1))
    c.execute("SELECT COUNT(*) FROM configs WHERE user_id = ? AND created_at > ?", (user_id, yesterday))
    count = c.fetchone()[0]
    conn.close()
    return count < limit

def generate_warp_keys():
    RELAY_URLS = ["https://wgcli.vercel.app/v0a2158/reg", "https://api.cloudflareclient.com/v0a2158/reg"]
    data = {"key": base64.b64encode(os.urandom(32)).decode(), "install_id": "", "fcm_token": "", "tos": datetime.datetime.now().isoformat() + "Z", "model": "PC", "serial_number": "", "locale": "en_US"}
    for url in RELAY_URLS:
        try:
            req = urllib.request.Request(url, data=json.dumps(data).encode(), headers={'Content-Type': 'application/json', 'User-Agent': 'okhttp/3.12.1'})
            resp = urllib.request.urlopen(req, timeout=10).read().decode()
            res_data = json.loads(resp)
            return res_data['config']['interface']['private_key'], res_data['config']['peers'][0]['public_key']
        except Exception: continue
    return FALLBACK_PRIVATE_KEY, FALLBACK_PUBLIC_KEY

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if is_banned(user_id):
        bot.send_message(user_id, "⛔️ شما مسدود شده‌اید.")
        return
        
    is_new = add_user(user_id, message.from_user.first_name, message.from_user.username)
    chat_id = message.chat.id
    name = message.from_user.first_name
    
    if is_new and not is_admin(user_id):
        username = f"@{message.from_user.username}" if message.from_user.username else "ندارد"
        notify_text = f"🔔 **کاربر جدید!**\n\n👤 نام: {name}\n🆔 یوزرنیم: {username}\n🆔 آیدی: `{user_id}`"
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("🚫 بن کاربر", callback_data=f"ban_{user_id}", style="danger"),
            types.InlineKeyboardButton("👑 تنظیم ادمین", callback_data=f"admin_{user_id}", style="success")
        )
        try: bot.send_message(SUPER_ADMIN_ID, notify_text, reply_markup=markup, parse_mode='Markdown')
        except: pass

    welcome_text = f"سلام {name} عزیز، به بات ساخت کانفیگ خوش اومدی 🚀\n\n🤖 **این ربات توسط @KiarashAi ساخته شده است.**\n\nاز منوی پایین انتخاب کن:"
    if is_admin(user_id):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("🛠 ساخت کانفیگ جدید"), types.KeyboardButton("👑 پنل مدیریت"))
        markup.add(types.KeyboardButton("📁 کانفیگ‌های من"), types.KeyboardButton("📢 ارسال پیام همگانی"))
        bot.send_message(chat_id, f"سلام {name} عزیز، به پنل مدیریت خوش اومدی 👑", reply_markup=markup, parse_mode='Markdown')
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("🛠 ساخت کانفیگ جدید"), types.KeyboardButton("📁 کانفیگ‌های من"))
        markup.add(types.KeyboardButton("📚 آموزش اتصال"))
        bot.send_message(chat_id, welcome_text, reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text == "🔙 لغو و بازگشت")
def global_cancel(message):
    user_id = message.from_user.id
    if user_id in user_data: del user_data[user_id]
    if user_id in admin_state: del admin_state[user_id]
    bot.send_message(user_id, "✅ عملیات لغو شد.")
    start(message)

@bot.message_handler(func=lambda message: message.text == "👑 پنل مدیریت" and is_admin(message.chat.id))
def admin_panel_btn(message):
    conn = sqlite3.connect('bot_data.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users"); total_users = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM configs"); total_configs = c.fetchone()[0]
    conn.close()
    current_limit = get_setting('limit')
    is_locked = get_setting('bot_locked') == '1'
    lock_status = "🔴 قفل" if is_locked else "🟢 باز"
    text = f"👑 **آمار ربات**\n\n👥 کل کاربرا: {total_users}\n⚙️ کل کانفیگ‌ها: {total_configs}\n\n📊 محدودیت: {current_limit} کانفیگ در ۲۴ ساعت\n🔒 وضعیت ربات: {lock_status}"
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("📊 آمار و لیست کاربران", callback_data="list_users", style="primary"))
    markup.add(types.InlineKeyboardButton("⚙️ تنظیم محدودیت کاربران", callback_data="set_limit", style="primary"))
    lock_btn_style = "danger" if not is_locked else "success"
    lock_btn_text = "🔐 قفل کردن ربات" if not is_locked else "🔓 باز کردن ربات"
    markup.add(types.InlineKeyboardButton(lock_btn_text, callback_data="toggle_lock", style=lock_btn_style))
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == "list_users" and is_admin(call.from_user.id))
def list_users(call):
    bot.answer_callback_query(call.id)
    conn = sqlite3.connect('bot_data.db')
    c = conn.cursor()
    c.execute("SELECT user_id, first_name FROM users LIMIT 20")
    users = c.fetchall()
    conn.close()
    if not users:
        bot.send_message(call.message.chat.id, "هیچ کاربری یافت نشد.")
        return
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(f"{u_name}", callback_data=f"user_panel_{u_id}", style="primary") for u_id, u_name in users]
    markup.add(*buttons)
    bot.send_message(call.message.chat.id, "👥 **لیست کاربران (برای مشاهده جزئیات کلیک کنید):**", reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data.startswith("user_panel_") and is_admin(call.from_user.id))
def user_panel(call):
    bot.answer_callback_query(call.id)
    target_id = int(call.data.split("_")[2])
    conn = sqlite3.connect('bot_data.db')
    c = conn.cursor()
    c.execute("SELECT first_name, username, join_date, is_admin, is_banned FROM users WHERE user_id = ?", (target_id,))
    user = c.fetchone()
    
    if not user:
        bot.send_message(call.message.chat.id, "کاربر یافت نشد.")
        conn.close()
        return
        
    name, username, join_date, adm, ban = user
    c.execute("SELECT COUNT(*) FROM configs WHERE user_id = ?", (target_id,))
    config_count = c.fetchone()[0]
    conn.close()
    
    status = "🚫 مسدود" if ban else "🟢 فعال"
    role = "👑 ادمین" if adm else "👤 کاربر عادی"
    user_link = f"@{username}" if username else "ندارد"
    reg_date = join_date[:10] if join_date else "نامشخص"
    
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🚫 مسدود کردن", callback_data=f"ban_{target_id}", style="danger"),
        types.InlineKeyboardButton("👑 تنظیم ادمین", callback_data=f"admin_{target_id}", style="success")
    )
    
    text = (
        f"👤 **پنل کاربر:** {name}\n"
        f"🆔 **آیدی عددی:** `{target_id}`\n"
        f"🔗 **یوزرنیم:** {user_link}\n"
        f"📅 **تاریخ عضویت:** {reg_date}\n\n"
        f"⚙️ **تعداد کانفیگ‌های ساخته شده:** {config_count}\n\n"
        f"📊 **وضعیت:** {status}\n"
        f"👑 **نقش:** {role}"
    )
    
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data.startswith("ban_") or call.data.startswith("admin_"))
def admin_actions(call):
    if call.from_user.id != SUPER_ADMIN_ID: 
        bot.answer_callback_query(call.id, "فقط مدیر کل!")
        return
    action, target_id = call.data.split("_")
    target_id = int(target_id)
    conn = sqlite3.connect('bot_data.db')
    c = conn.cursor()
    if action == "ban":
        c.execute("UPDATE users SET is_banned = 1 WHERE user_id = ?", (target_id,))
        msg = "کاربر بن شد. 🚫"
        try: bot.send_message(target_id, "⛔️ شما مسدود شدید.")
        except: pass
    elif action == "admin":
        c.execute("UPDATE users SET is_admin = 1 WHERE user_id = ?", (target_id,))
        msg = "کاربر ادمین شد. 👑"
        try: bot.send_message(target_id, "👑 شما ادمین شدید.")
        except: pass
    conn.commit()
    conn.close()
    bot.answer_callback_query(call.id, msg)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)

@bot.callback_query_handler(func=lambda call: call.data == "toggle_lock" and is_admin(call.from_user.id))
def toggle_lock(call):
    current = get_setting('bot_locked')
    new_val = '0' if current == '1' else '1'
    set_setting('bot_locked', new_val)
    bot.answer_callback_query(call.id, f"وضعیت تغییر کرد.")
    admin_panel_btn(call.message)

@bot.callback_query_handler(func=lambda call: call.data == "set_limit" and is_admin(call.from_user.id))
def ask_new_limit(call):
    bot.answer_callback_query(call.id)
    admin_state[call.from_user.id] = "waiting_for_limit"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🔙 لغو و بازگشت"))
    msg = bot.send_message(call.message.chat.id, "عدد جدید رو بفرست:", reply_markup=markup)
    bot.register_next_step_handler(msg, save_new_limit)

def save_new_limit(message):
    if not is_admin(message.from_user.id) or admin_state.get(message.from_user.id) != "waiting_for_limit": return
    if message.text == "🔙 لغو و بازگشت": return global_cancel(message)
    if not message.text.isdigit():
        bot.send_message(message.chat.id, "❌ فقط عدد!")
        return
    set_setting('limit', int(message.text))
    admin_state[message.from_user.id] = None
    bot.send_message(message.chat.id, f"✅ محدودیت تنظیم شد.", parse_mode='Markdown')
    start(message)

@bot.message_handler(func=lambda message: message.text == "📢 ارسال پیام همگانی" and is_admin(message.chat.id))
def broadcast_btn(message):
    admin_state[message.from_user.id] = "waiting_for_broadcast"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🔙 لغو و بازگشت"))
    msg = bot.send_message(message.chat.id, "متن پیام همگانی:", reply_markup=markup)
    bot.register_next_step_handler(msg, send_broadcast)

def send_broadcast(message):
    if not is_admin(message.from_user.id) or admin_state.get(message.from_user.id) != "waiting_for_broadcast": return
    if message.text == "🔙 لغو و بازگشت": return global_cancel(message)
    admin_state[message.from_user.id] = None
    conn = sqlite3.connect('bot_data.db')
    c = conn.cursor()
    c.execute("SELECT user_id FROM users WHERE is_banned = 0")
    users = c.fetchall()
    conn.close()
    success = 0
    for user in users:
        try:
            bot.send_message(user[0], f"📢 **پیام همگانی:**\n\n{message.text}", parse_mode='Markdown')
            success += 1
            time.sleep(0.05)
        except: pass
    bot.send_message(message.chat.id, f"✅ برای {success} نفر ارسال شد.")
    start(message)

@bot.message_handler(func=lambda message: message.text == "🛠 ساخت کانفیگ جدید")
def start_config(message):
    user_id = message.from_user.id
    if is_banned(user_id): return
    if get_setting('bot_locked') == '1' and not is_admin(user_id):
        bot.send_message(user_id, "⛔️ دسترسی ساخت کانفیگ بسته شده است.")
        return
    if not check_rate_limit(user_id):
        bot.send_message(user_id, f"❌ محدودیت ساخت ({get_setting('limit')} بار در روز) پر شده.")
        return
    
    user_data[user_id] = {}
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📥 دانلود NikaNG", url="https://github.com/mahsanet/NikaNG/releases/latest", style="success"))
    markup.add(types.InlineKeyboardButton("✅ دانلود کردم، ادامه", callback_data="config_step_1", style="primary"))
    markup.add(types.InlineKeyboardButton("🔙 لغو و بازگشت", callback_data="cancel_flow", style="danger"))
    
    bot.send_message(user_id, "ابتدا برنامه **NikaNG** را دانلود کنید.\n\nپس از دانلود، روی دکمه **«✅ دانلود کردم، ادامه»** کلیک کنید:", reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == "config_step_1")
def config_step_1(call):
    chat_id = call.message.chat.id
    if chat_id not in user_data: user_data[chat_id] = {}
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🎲 اسم خودکار", callback_data="random_name", style="primary"))
    markup.add(types.InlineKeyboardButton("🔙 لغو و بازگشت", callback_data="cancel_flow", style="danger"))
    
    bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="حالا یه اسم برای کانفیگت بنویس، یا از دکمه زیر استفاده کن:", reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == "cancel_flow")
def cancel_inline_flow(call):
    chat_id = call.message.chat.id
    if chat_id in user_data: del user_data[chat_id]
    bot.edit_message_text("❌ عملیات ساخت کانفیگ لغو شد.", chat_id, call.message.message_id)
    start(call.message)

@bot.callback_query_handler(func=lambda call: call.data == "random_name")
def random_name_selected(call):
    chat_id = call.message.chat.id
    if chat_id not in user_data: return
    chosen_name = random.choice(RANDOM_NAMES) + "-" + str(random.randint(10, 99))
    user_data[chat_id]['name'] = f"{chosen_name} (KiarashAi)"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("نامحدود ♾", callback_data="Unlimited", style="success"))
    markup.add(types.InlineKeyboardButton("🔙 لغو و بازگشت", callback_data="cancel_flow", style="danger"))
    bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=f"اسم شد: **{chosen_name} (KiarashAi)**\n\nدکمه زیر بزن:", reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.chat.id in user_data and 'name' not in user_data[message.chat.id])
def get_name(message):
    chat_id = message.chat.id
    final_name = f"{message.text} (KiarashAi)"
    user_data[chat_id]['name'] = final_name
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("نامحدود ♾", callback_data="Unlimited", style="success"))
    markup.add(types.InlineKeyboardButton("🔙 لغو و بازگشت", callback_data="cancel_flow", style="danger"))
    bot.send_message(chat_id, f"اسم شد **{final_name}**.\nدکمه زیر بزن:", reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == 'Unlimited')
def get_size(call):
    chat_id = call.message.chat.id
    if chat_id not in user_data: return
    user_data[chat_id]['size'] = "نامحدود"
    user_data[chat_id]['time'] = "تا زمانی که پنل بن شود"
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ تایید و ادامه", callback_data="generate_final", style="success"))
    markup.add(types.InlineKeyboardButton("🔙 لغو و بازگشت", callback_data="cancel_flow", style="danger"))
    
    bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, 
                          text="حجم: نامحدود ♾\nمدت زمان: **تا زمانی که پنل بن شود**", 
                          reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == 'generate_final')
def generate_final(call):
    chat_id = call.message.chat.id
    if chat_id not in user_data: return
    bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="⏳ صبر کن، دارم کانفیگ AWG رو می‌سازم...")
    try:
        private_key, public_key = generate_warp_keys()
        selected_ip = random.choice(CLEAN_IPS)
        config_text = f"""[Interface]
Address = 172.16.0.2/32
PrivateKey = {private_key}
DNS = 1.1.1.1, 1.0.0.1
Jc = {JUNK_JC}
Jmin = {JUNK_JMIN}
Jmax = {JUNK_JMAX}
I1 = {JUNK_I1}

[Peer]
PublicKey = {public_key}
Endpoint = {selected_ip}
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25"""
        save_config(chat_id, user_data[chat_id]['name'], user_data[chat_id]['size'], user_data[chat_id]['time'])
        
        text_caption = (
            f"✅ **کانفیگ AWG شما:**\n\n"
            f"```\n{config_text}\n```\n\n"
            f"📚 **آموزش:** متن بالا رو کپی کن، توی NikaNG گزینه Import from Clipboard رو بزن.\n\n"
            f"♾ **توجه:** کانفیگ‌های کلادفلر که تولید می‌شوند نامحدود و بدون محدودیت زمانی هستند.\n"
            f"این کانفیگ‌ها تا زمانی که پنل بن نشود کار می‌کنند.\n\n"
            f"⚠️ **هشدار:** برای جلوگیری از حذف شدن پنل، در ماه بیشتر از ۴۰۰ گیگ مصرف نکنید."
        )
        bot.send_message(chat_id, text_caption, parse_mode='Markdown')
        
        admin_text = (
            f"🔔 **کاربر کانفیگ ساخت!**\n\n"
            f"👤 نام: {call.message.chat.first_name}\n"
            f"🆔 آیدی: `{chat_id}`\n"
            f"📛 اسم کانفیگ: {user_data[chat_id]['name']}"
        )
        bot.send_message(SUPER_ADMIN_ID, admin_text, parse_mode='Markdown')
    except Exception as e:
        bot.send_message(SUPER_ADMIN_ID, f"⚠️ خطا: {e}")
    if chat_id in user_data: del user_data[chat_id]

app = Flask(__name__)
@app.route('/')
def index(): return "Bot is running!"
@app.route('/health')
def health(): return "OK"

def run_bot():
    print("ربات روشن شد...")
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
