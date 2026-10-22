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
    # حذف روز هفته از جدول قرعه کشی و اضافه شدن وضعیت ذخیره کانال
    c.execute('''CREATE TABLE IF NOT EXISTS draws 
                 (id INTEGER PRIMARY KEY, channel TEXT, start_hour TEXT, end_hour TEXT, title TEXT, status TEXT, message_id INTEGER, date TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS participants (draw_id INTEGER, user_id INTEGER, first_name TEXT)''')
    c.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('limit', '3')")
    c.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('bot_locked', '0')")
    c.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('saved_channel', '')")
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

def generate_config_text(private_key, public_key):
    selected_ip = random.choice(CLEAN_IPS)
    return f"""[Interface]
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

# 🕒 سیستم زمان‌بندی قرعه کشی
def draw_scheduler():
    while True:
        try:
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M")
            today_date = now.strftime("%Y-%m-%d")
            
            conn = sqlite3.connect('bot_data.db')
            c = conn.cursor()
            
            # 1. شروع قرعه کشی
            c.execute("SELECT id, channel, title FROM draws WHERE status = 'pending' AND start_hour = ? AND date = ?", (current_time, today_date))
            start_draws = c.fetchall()
            for draw in start_draws:
                draw_id, channel, title = draw
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("🎁 شرکت در قرعه‌کشی", callback_data=f"join_{draw_id}", style="primary"))
                try:
                    msg = bot.send_message(channel, f"🎉 **{title}**\n\nبرای شرکت در قرعه کشی روی دکمه زیر کلیک کنید:", reply_markup=markup, parse_mode='Markdown')
                    c.execute("UPDATE draws SET status = 'active', message_id = ? WHERE id = ?", (msg.message_id, draw_id))
                    conn.commit()
                except Exception as e:
                    print(f"Error sending to channel: {e}")

            # 2. پایان قرعه کشی
            c.execute("SELECT id, channel, title, message_id FROM draws WHERE status = 'active' AND end_hour = ? AND date = ?", (current_time, today_date))
            end_draws = c.fetchall()
            for draw in end_draws:
                draw_id, channel, title, msg_id = draw
                c.execute("SELECT user_id, first_name FROM participants WHERE draw_id = ?", (draw_id,))
                parts = c.fetchall()
                
                if not parts:
                    bot.send_message(channel, f"⚠️ **{title}**\n\nمتاسفانه هیچ‌کس در این قرعه‌کشی شرکت نکرد!", reply_to_message_id=msg_id)
                else:
                    winner = random.choice(parts)
                    winner_id, winner_name = winner
                    private_key, public_key = generate_warp_keys()
                    config_text = generate_config_text(private_key, public_key)
                    winner_text = (
                        f"🎉 **تبریک {winner_name}!**\n\n"
                        f"شما برنده قرعه‌کشی **{title}** شدید. 🥇\n\n"
                        f"✅ **کانفیگ AWG شما:**\n\n```\n{config_text}\n```\n\n"
                        f"📚 **آموزش:** متن بالا رو کپی کن، توی NikaNG گزینه Import from Clipboard رو بزن.\n\n"
                        f"⚠️ **هشدار:** بیش از ۴۰۰ گیگ در ماه مصرف نکنید."
                    )
                    try:
                        bot.send_message(winner_id, winner_text, parse_mode='Markdown')
                        bot.send_message(channel, f"🏆 **برنده قرعه‌کشی {title}:**\n\n{winner_name}\n\n(کانفیگ به دایرکت ایشون ارسال شد)", reply_to_message_id=msg_id)
                    except Exception as e:
                        bot.send_message(channel, f"⚠️ برنده انتخاب شد ({winner_name}) اما چون ربات رو استارت نکرده بود، نتونستم کانفیگ رو بفرستم.", reply_to_message_id=msg_id)

                c.execute("UPDATE draws SET status = 'finished' WHERE id = ?", (draw_id,))
                conn.commit()
            conn.close()
        except Exception as e:
            print(f"Scheduler error: {e}")
        
        time.sleep(30) # هر ۳۰ ثانیه چک میکنه که دقیق باشه
# ================= تنظیمات قرعه کشی =================
@bot.callback_query_handler(func=lambda call: call.data == "setup_draw" and is_admin(call.from_user.id))
def start_draw_setup(call):
    bot.answer_callback_query(call.id)
    saved_channel = get_setting('saved_channel')
    
    if saved_channel:
        admin_state[call.from_user.id] = {"channel": saved_channel}
        admin_state[call.from_user.id]['state'] = "waiting_draw_title"
        msg = bot.send_message(call.message.chat.id, f"۵️⃣ **عنوان قرعه‌کشی** را وارد کنید (مثلاً: `قرعه‌کشی کانفیگ رایگان`):")
        bot.register_next_step_handler(msg, process_draw_title)
    else:
        admin_state[call.from_user.id] = {}
        admin_state[call.from_user.id]['state'] = "waiting_draw_channel"
        msg = bot.send_message(call.message.chat.id, "۱️⃣ **آیدی کانال** خود را وارد کنید (مثلاً `@MyChannel`).\n\n⚠️ ربات باید ادمین کانال باشد!", parse_mode='Markdown')
        bot.register_next_step_handler(msg, process_draw_channel)

def process_draw_channel(message):
    if not is_admin(message.from_user.id): return
    channel = message.text
    set_setting('saved_channel', channel)
    admin_state[message.from_user.id] = {"channel": channel}
    admin_state[message.from_user.id]['state'] = "waiting_draw_title"
    msg = bot.send_message(message.chat.id, "۵️⃣ **عنوان قرعه‌کشی** را وارد کنید (مثلاً: `قرعه‌کشی کانفیگ رایگان`):")
    bot.register_next_step_handler(msg, process_draw_title)

def process_draw_title(message):
    if not is_admin(message.from_user.id): return
    title = message.text
    admin_state[message.from_user.id]['title'] = title
    admin_state[message.from_user.id]['state'] = "waiting_draw_start"
    msg = bot.send_message(message.chat.id, "۳️⃣ **ساعت شروع** قرعه‌کشی را وارد کنید (مثلاً `14:00`):")
    bot.register_next_step_handler(msg, process_draw_start)

def process_draw_start(message):
    if not is_admin(message.from_user.id): return
    start_time = message.text
    admin_state[message.from_user.id]['start_hour'] = start_time
    admin_state[message.from_user.id]['state'] = "waiting_draw_end"
    msg = bot.send_message(message.chat.id, "۴️⃣ **ساعت پایان** قرعه‌کشی را وارد کنید (مثلاً `18:00`):")
    bot.register_next_step_handler(msg, process_draw_end)

def process_draw_end(message):
    if not is_admin(message.from_user.id): return
    end_time = message.text
    data = admin_state[message.from_user.id]
    
    conn = sqlite3.connect('bot_data.db')
    c = conn.cursor()
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # ذخیره در دیتابیس با تاریخ امروز
    c.execute("INSERT INTO draws (channel, start_hour, end_hour, title, status, date) VALUES (?, ?, ?, ?, 'pending', ?)",
              (data['channel'], data['start_hour'], end_time, data['title'], today_date))
    conn.commit()
    conn.close()
    
    del admin_state[message.from_user.id]
    bot.send_message(message.chat.id, f"✅ **قرعه‌کشی با موفقیت تنظیم شد!**\n\n📅 تاریخ: امروز\n⏰ از {data['start_hour']} تا {end_time}\n📢 کانال: {data['channel']}\n🎁 عنوان: {data['title']}\n\nربات در زمان مشخص شده، خودکار در کانال پیام می‌ذاره و برنده رو انتخاب می‌کنه.", reply_markup=types.ReplyKeyboardRemove(), parse_mode='Markdown')
    start(message)@bot.callback_query_handler(func=lambda call: call.data.startswith("join_"))
def join_draw(call):
    draw_id = int(call.data.split("_")[1])
    user_id = call.from_user.id
    first_name = call.from_user.first_name
    
    conn = sqlite3.connect('bot_data.db')
    c = conn.cursor()
    
    c.execute("SELECT * FROM participants WHERE draw_id = ? AND user_id = ?", (draw_id, user_id))
    if c.fetchone():
        bot.answer_callback_query(call.id, "شما قبلاً در این قرعه‌کشی شرکت کرده‌اید!", show_alert=True)
        conn.close()
        return
        
    c.execute("INSERT INTO participants (draw_id, user_id, first_name) VALUES (?, ?, ?)", (draw_id, user_id, first_name))
    conn.commit()
    conn.close()
    
    bot.answer_callback_query(call.id, "✅ با موفقیت در قرعه‌کشی شرکت کردید!", show_alert=True)
    
