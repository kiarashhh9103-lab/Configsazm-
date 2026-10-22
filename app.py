import os, threading, telebot, random, datetime, time, json, base64, urllib.request, pymongo
from flask import Flask
from telebot import types

# 🔴 توکن و لینک دیتابیس مستقیم توی کد قرار گرفتند
BOT_TOKEN = "8906649902:AAEJHKZq-K7mVqXrIbt7OYTf_YjC8cey_h4"
MONGO_URI = "mongodb+srv://KiarashAi:KiarashAi@cluster0.xl9mcbq.mongodb.net/"
SUPER_ADMIN_ID = 8639658675
BOT_USERNAME = "Kiawirebot"

CLEAN_IPS = ["8.34.70.64:2408", "8.6.112.224:2408", "188.114.98.12:2408", "8.34.70.120:2408", "8.35.211.2:2408", "188.114.96.70:2408", "188.114.99.75:2408", "8.39.214.218:2408", "188.114.99.6:2408", "8.34.70.169:2408"]
RANDOM_NAMES = ["Ghost", "Ninja", "Warp", "Pro", "Shadow", "Turbo", "VIP", "Smart", "Ultra", "Fast"]
JUNK_I1 = "<b 0xc10000000114367096bb0fb3f58f3a3fb8aaacd61d63a1c8a40e14f7374b8a62dccba6431716c3abf6f5afbcfb39bd008000047c32e268567c652e6f4db58bff759bc8c5aaca183b87cb4d22938fe7d8dca22a679a79e4d9ee62e4bbb3a380dd78d4e8e48f26b38a1d42d76b371a5a9a0444827a69d1ab5872a85749f65a4104e931740b4dc1e2dd77733fc7fac4f93011cd622f2bb47e85f71992e2d585f8dc765a7a12ddeb879746a267393ad023d267c4bd79f258703e27345155268bd3cc0506ebd72e2e3c6b5b0f005299cd94b67ddabe30389c4f9b5c2d512dcc298c14f14e9b7f931e1dc397926c31fbb7cebfc668349c218672501031ecce151d4cb03c4c660b6c6fe7754e75446cd7de09a8c81030c5f6fb377203f551864f3d83e27de7b86499736cbbb549b2f37f436db1cae0a4ea39930f0534aacdd1e3534bc87877e2afabe959ced261f228d6362e6fd277c88c312d966c8b9f67e4a92e757773db0b0862fb8108d1d8fa262a40a1b4171961f0704c8ba314da2482ac8ed9bd28d4b50f7432d89fd800c25a50c5e2f5c0710544fef5273401116aa0572366d8e49ad758fcb29e6a92912e644dbe227c247cb3417eabfab2db16796b2fba420de3b1dc94e8361f1f324a331ddaf1e626553138860757fd0bf687566108b77b70fb9f8f8962eca599c4a70ed373666961a8cb506b96756d9e28b94122b20f16b54f118c0e603ce0b831efea614ad836df6cf9affbdd09596412547496967da758cec9080295d853b0861670b71d9abde0d562b1a6de82782a5b0c14d297f27283a895abc889a5f6703f0e6eb95f67b2da45f150d0d8ab805612d570c2d5cb6997ac3a7756226c2f5c8982ffbd480c5004b0660a3c9468945efde90864019a2b519458724b55d766e16b0da25c0557c01f3c11ddeb024b62e303640e17fdd57dedb3aeb4a2c1b7c93059f9c1d7118d77caac1cd0f6556e46cbc991c1bb16970273dea833d01e5090d061a0c6d25af2415cd2878af97f6d0e7f1f936247b394ecb9bd484da6be936dee9b0b92dc90101a1b4295e97a9772f2263eb09431995aa173df4ca2abd687d87706f0f93eaa5e13cbe3b574fa3cfe94502ace25265778da6960d561381769c24e0cbd7aac73c16f95ae74ff7ec38124f7c722b9cb151d4b6841343f29be8f35145e1b27021056820fed77003df8554b4155716c8cf6049ef5e318481460a8ce3be7c7bfac695255be84dc491c19e9dedc449dd3471728cd2a3ee51324ccb3eef121e3e08f8e18f0006ea8957371d9f2f739f0b89e4db11e5c6430ada61572e589519fbad4498b460ce6e4407fc2d8f2dd4293a50a0cb8fcaaf35cd9a8cc097e3603fbfa08d9036f52b3e7fcce11b83ad28a4ac12dba0395a0cc871cefd1a2856fffb3f28d82ce35cf80579974778bab13d9b3578d8c75a2d196087a2cd439aff2bb33f2db24ac175fff4ed91d36a4cdbfaf3f83074f03894ea40f17034629890da3efdbb41141b38368ab532209b69f057ddc559c19bc8ae62bf3fd564c9a35d9a83d14a95834a92bae6d9a29ae5e8ece07910d16433e4c6230c9bd7d68b47de0de9843988af6dc88b5301820443bd4d0537778bf6b4c1dd067fcf14b81015f2a67c7f2a28f9cb7e0684d3cb4b1c24d9b343122a086611b489532f1c3a26779da1706c6759d96d8ab>"

bot = telebot.TeleBot(BOT_TOKEN)
user_data, admin_state = {}, {}

# اتصال به دیتابیس ابری (MongoDB)
client = pymongo.MongoClient(MONGO_URI)
db = client['kiawire_bot']
users_col = db['users']
configs_col = db['configs']
settings_col = db['settings']
draws_col = db['draws']
parts_col = db['participants']

def is_admin(uid): return uid == SUPER_ADMIN_ID or (users_col.find_one({"user_id": uid}) or {}).get("is_admin", 0) == 1
def is_banned(uid): return (users_col.find_one({"user_id": uid}) or {}).get("is_banned", 0) == 1
def get_setting(k): return (settings_col.find_one({"key": k}) or {}).get("value", "0")
def set_setting(k, v): settings_col.update_one({"key": k}, {"$set": {"value": str(v)}}, upsert=True)

def add_user(uid, name, user):
    if not users_col.find_one({"user_id": uid}):
        users_col.insert_one({"user_id": uid, "first_name": name, "username": user, "join_date": str(datetime.datetime.now()), "is_admin": 0, "is_banned": 0})
        return True
    return False

def gen_config():
    try:
        req = urllib.request.Request("https://wgcli.vercel.app/v0a2158/reg", data=json.dumps({"key": base64.b64encode(os.urandom(32)).decode(), "install_id": "", "fcm_token": "", "tos": datetime.datetime.now().isoformat()+"Z", "model": "PC"}).encode(), headers={'Content-Type': 'application/json', 'User-Agent': 'okhttp/3.12.1'})
        resp = json.loads(urllib.request.urlopen(req, timeout=5).read().decode())
        pk, pub = resp['config']['interface']['private_key'], resp['config']['peers'][0]['public_key']
    except: pk, pub = "AGgMU5NwgOb1W3t4ZV0sFl/xnoj3+vvBN0FFPSLuRGg=", "bmXOC+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo="
    return f"[Interface]\nAddress = 172.16.0.2/32\nPrivateKey = {pk}\nDNS = 1.1.1.1, 1.0.0.1\nJc = 6\nJmin = 10\nJmax = 50\nI1 = {JUNK_I1}\n\n[Peer]\nPublicKey = {pub}\nEndpoint = {random.choice(CLEAN_IPS)}\nAllowedIPs = 0.0.0.0/0\nPersistentKeepalive = 25"

def scheduler():
    while True:
        now = (datetime.datetime.utcnow() + datetime.timedelta(hours=3, minutes=30)).strftime("%Y-%m-%d %H:%M:%S")
        active_draws = draws_col.find({"status": "active", "end_time": {"$lte": now}})
        for d in active_draws:
            did = d['id']
            parts = list(parts_col.find({"draw_id": did}))
            if parts:
                for w in random.sample(parts, min(d['winners_count'], len(parts))):
                    try: 
                        kb_app = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("📥 دانلود برنامه NikaNG", url="https://github.com/mahsanet/NikaNG/releases/latest", style="primary"))
                        bot.send_message(w['user_id'], f"🎉 **تبریک {w['first_name']}!**\nشما برنده **{d['title']}** شدید.\n\n✅ **کانفیگ AWG شما:**\n\n```\n{gen_config()}\n```\n🎮 **توجه:** هم سرور گیمینگ و هم کانفیگ.", reply_markup=kb_app, parse_mode='Markdown')
                        
                        consent_text = "از شما خواهش میکنیم از طریق دکمه زیر رضایت خود را از چالش اعلام کنید."
                        kb_consent = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("✅ اعلام رضایت", callback_data=f"consent_{did}_{w['user_id']}", style="primary"))
                        bot.send_message(w['user_id'], consent_text, reply_markup=kb_consent, parse_mode='Markdown')
                    except: pass
                try: bot.send_message(d['channel'], f"🏆 **برندگان {d['title']}:**\n" + "\n".join([f"- {w['first_name']}" for w in random.sample(parts, min(d['winners_count'], len(parts)))]), reply_to_message_id=d['message_id'])
                except: pass
            else:
                try: bot.send_message(d['channel'], f"⚠️ **{d['title']}**\nهیچ‌کس شرکت نکرد!", reply_to_message_id=d['message_id'])
                except: pass
            draws_col.update_one({"id": did}, {"$set": {"status": "finished"}})
        time.sleep(15)

@bot.message_handler(commands=['start'])
def start(m):
    uid, cid, name = m.from_user.id, m.chat.id, m.from_user.first_name
    if is_banned(uid): return bot.send_message(cid, "⛔️ مسدود هستید.")
    is_new = add_user(uid, name, m.from_user.username)
    
    args = m.text.split()
    if len(args) > 1 and args[1].startswith("draw_"):
        did = int(args[1].split("_")[1])
        draw = draws_col.find_one({"id": did})
        if draw and draw['status']=='active':
            cnt = parts_col.count_documents({"draw_id": did})
            if draw['max_parts'] > 0 and cnt >= draw['max_parts']: return bot.send_message(cid, "⚠️ ظرفیت پر شده!")
            if not parts_col.find_one({"draw_id": did, "user_id": uid}):
                parts_col.insert_one({"draw_id": did, "user_id": uid, "first_name": name})
                m2 = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🎁 شرکت در قرعه‌کشی", url=f"https://t.me/{BOT_USERNAME}?start=draw_{did}", style="primary"), types.InlineKeyboardButton(f"{cnt+1} شرکت کننده 💫", callback_data="noop", style="primary"))
                try: bot.edit_message_reply_markup(chat_id=draw['channel'], message_id=draw['message_id'], reply_markup=m2)
                except: pass
                return bot.send_message(cid, "✅ با موفقیت شرکت کردی!")
            bot.send_message(cid, "⚠️ قبلاً شرکت کردی!")
        else: bot.send_message(cid, "❌ بسته شده.")
        return

    if is_new and not is_admin(uid):
        nm = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🚫 بن", callback_data=f"ban_{uid}", style="danger"), types.InlineKeyboardButton("👑 ادمین", callback_data=f"adm_{uid}", style="success"))
        try: bot.send_message(SUPER_ADMIN_ID, f"🔔 **کاربر جدید!**\n👤 {name}\n🆔 `{uid}`", reply_markup=nm, parse_mode='Markdown')
        except: pass

    m_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if is_admin(uid):
        m_kb.add("🛠 ساخت کانفیگ", "👑 پنل", "📢 پیام همگانی")
        bot.send_message(cid, f"سلام {name} عزیز، به پنل خوش اومدی 👑", reply_markup=m_kb)
    else:
        m_kb.add("🛠 ساخت کانفیگ", "📚 آموزش اتصال")
        bot.send_message(cid, f"سلام {name} عزیز، خوش اومدی 🚀", reply_markup=m_kb)

@bot.callback_query_handler(func=lambda c: c.data == "noop")
def noop(c): bot.answer_callback_query(c.id, "برای شرکت روی دکمه آبی کلیک کن.")

@bot.callback_query_handler(func=lambda call: call.data.startswith("consent_"))
def user_consent(call):
    bot.answer_callback_query(call.id, "درخواست شما ارسال شد.")
    _, did, uid = call.data.split("_")
    did, uid = int(did), int(uid)
    
    user = users_col.find_one({"user_id": uid})
    draw = draws_col.find_one({"id": did})
    u_name = user['first_name'] if user else "ناشناس"
    title = draw['title'] if draw else "قرعه‌کشی"
    
    admin_text = f"👤 **کاربر {u_name}** (ID: `{uid}`) رضایت خود را از چالش **{title}** اعلام کرد.\n\nآیا تایید می‌کنید؟"
    admin_kb = types.InlineKeyboardMarkup(row_width=2).add(
        types.InlineKeyboardButton("✅ تایید", callback_data=f"app_c_{did}_{uid}", style="success"),
        types.InlineKeyboardButton("❌ رد", callback_data=f"rej_c_{uid}", style="danger")
    )
    bot.send_message(SUPER_ADMIN_ID, admin_text, reply_markup=admin_kb, parse_mode='Markdown')
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)

@bot.callback_query_handler(func=lambda call: call.data.startswith("app_c_"))
def admin_approve_consent(call):
    if call.from_user.id != SUPER_ADMIN_ID: return bot.answer_callback_query(call.id, "فقط ادمین!")
    bot.answer_callback_query(call.id, "تایید شد.")
    _, _, did, uid = call.data.split("_")
    did, uid = int(did), int(uid)
    
    user = users_col.find_one({"user_id": uid})
    draw = draws_col.find_one({"id": did})
    u_name = user['first_name'] if user else "ناشناس"
    title = draw['title'] if draw else "قرعه‌کشی"
    channel = draw['channel'] if draw else ""
    
    bot.edit_message_text(f"✅ رضایت کاربر {u_name} تایید شد و به کانال ارسال شد.", call.message.chat.id, call.message.message_id, reply_markup=None)
    try: bot.send_message(channel, f"🎊 **کاربر {u_name}** رسماً رضایت خود را از چالش **{title}** اعلام کرد. 🎉", parse_mode='Markdown')
    except: pass
    try: bot.send_message(uid, "✅ رضایت شما توسط مدیریت تایید شد.")
    except: pass

@bot.callback_query_handler(func=lambda call: call.data.startswith("rej_c_"))
def admin_reject_consent(call):
    if call.from_user.id != SUPER_ADMIN_ID: return bot.answer_callback_query(call.id, "فقط ادمین!")
    bot.answer_callback_query(call.id, "رد شد.")
    bot.edit_message_text("❌ رضایت کاربر رد شد.", call.message.chat.id, call.message.message_id, reply_markup=None)

@bot.message_handler(func=lambda m: m.text == "🔙 لغو")
def cancel(m):
    user_data.pop(m.from_user.id, None); admin_state.pop(m.from_user.id, None)
    bot.send_message(m.chat.id, "✅ لغو شد."); start(m)

@bot.message_handler(func=lambda m: m.text == "👑 پنل" and is_admin(m.chat.id))
def admin_panel(m):
    u = users_col.count_documents({}); cf = configs_col.count_documents({})
    lim, lk = get_setting('limit'), get_setting('bot_locked')
    text = f"👑 **آمار**\n👥 کاربران: {u}\n⚙️ کانفیگ‌ها: {cf}\n📊 محدودیت: {lim}\n🔒 وضعیت: {'🔴 قفل' if lk=='1' else '🟢 باز'}"
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(types.InlineKeyboardButton("📊 آمار و لیست کاربران", callback_data="list_users", style="primary"))
    kb.add(types.InlineKeyboardButton("⚙️ تنظیم محدودیت کاربران", callback_data="set_limit", style="primary"))
    kb.add(types.InlineKeyboardButton("🎁 تنظیم قرعه‌کشی", callback_data="setup_draw", style="success"))
    lock_btn_style = "danger" if lk != '1' else "success"
    lock_btn_text = "🔐 قفل کردن ربات" if lk != '1' else "🔓 باز کردن ربات"
    kb.add(types.InlineKeyboardButton(lock_btn_text, callback_data="toggle_lock", style=lock_btn_style))
    bot.send_message(m.chat.id, text, reply_markup=kb, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda c: c.data == "setup_draw" and is_admin(c.from_user.id))
def wiz_start(c):
    bot.answer_callback_query(c.id); admin_state[c.from_user.id] = {}
    msg = bot.send_message(c.message.chat.id, "📝 **گام ۱/۵: نام قرعه‌کشی** را بنویس:", reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("❌ لغو", callback_data="c_draw", style="danger")), parse_mode='Markdown')
    bot.register_next_step_handler(msg, wiz_title)

@bot.callback_query_handler(func=lambda c: c.data == "c_draw")
def wiz_cancel(c):
    bot.answer_callback_query(c.id); admin_state.pop(c.from_user.id, None)
    bot.edit_message_text("❌ لغو شد.", c.message.chat.id, c.message.message_id); start(c.message)

def wiz_title(m):
    if not is_admin(m.from_user.id): return
    admin_state[m.from_user.id]['title'] = m.text
    kb = types.InlineKeyboardMarkup(row_width=3).add(*[types.InlineKeyboardButton(f"⏱ {t}", callback_data=f"d_{v}", style="primary") for t,v in [("۵ د",5),("۱۰ د",10),("۳۰ د",30),("۱ س",60),("۲ س",120),("۲۴ س",1440)]], types.InlineKeyboardButton("✅ دستی", callback_data="m_dur", style="success"), types.InlineKeyboardButton("❌ لغو", callback_data="c_draw", style="danger"))
    bot.send_message(m.chat.id, "⏳ **گام ۲/۵: مدت زمان**", reply_markup=kb, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda c: (c.data.startswith("d_") or c.data=="m_dur") and is_admin(c.from_user.id))
def wiz_dur(c):
    bot.answer_callback_query(c.id)
    if c.data == "m_dur":
        msg = bot.send_message(c.message.chat.id, "⏳ دقیقه را وارد کن (مثلاً `45`):")
        return bot.register_next_step_handler(msg, wiz_dur_m)
    mins = int(c.data.split("_")[1])
    admin_state[c.from_user.id]['end_time'] = (datetime.datetime.utcnow() + datetime.timedelta(hours=3, minutes=30+mins)).strftime("%Y-%m-%d %H:%M:%S")
    bot.edit_message_text(f"✅ زمان: {mins} دقیقه", c.message.chat.id, c.message.message_id)
    kb = types.InlineKeyboardMarkup(row_width=3).add(*[types.InlineKeyboardButton(f"👥 {t}", callback_data=f"c_{v}", style="primary") for t,v in [("۱۰",10),("۵۰",50),("۱۰۰",100),("۵۰۰",500)]], types.InlineKeyboardButton("♾ نامحدود", callback_data="c_0", style="success"), types.InlineKeyboardButton("✅ دستی", callback_data="m_cap", style="success"), types.InlineKeyboardButton("❌ لغو", callback_data="c_draw", style="danger"))
    bot.send_message(c.message.chat.id, "🚀 **گام ۳/۵: ظرفیت**", reply_markup=kb, parse_mode='Markdown')

def wiz_dur_m(m):
    if not is_admin(m.from_user.id) or not m.text.isdigit(): return bot.send_message(m.chat.id, "❌ عدد بفرست!")
    admin_state[m.from_user.id]['end_time'] = (datetime.datetime.utcnow() + datetime.timedelta(hours=3, minutes=30+int(m.text))).strftime("%Y-%m-%d %H:%M:%S")
    bot.send_message(m.chat.id, f"✅ زمان: {m.text} دقیقه")
    kb = types.InlineKeyboardMarkup(row_width=3).add(*[types.InlineKeyboardButton(f"👥 {t}", callback_data=f"c_{v}", style="primary") for t,v in [("۱۰",10),("۵۰",50),("۱۰۰",100),("۵۰۰",500)]], types.InlineKeyboardButton("♾ نامحدود", callback_data="c_0", style="success"), types.InlineKeyboardButton("✅ دستی", callback_data="m_cap", style="success"), types.InlineKeyboardButton("❌ لغو", callback_data="c_draw", style="danger"))
    bot.send_message(m.chat.id, "🚀 **گام ۳/۵: ظرفیت**", reply_markup=kb, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda c: (c.data.startswith("c_") or c.data=="m_cap") and is_admin(c.from_user.id))
def wiz_cap(c):
    bot.answer_callback_query(c.id)
    if c.data == "m_cap":
        msg = bot.send_message(c.message.chat.id, "🚀 ظرفیت را وارد کن (0=نامحدود):")
        return bot.register_next_step_handler(msg, wiz_cap_m)
    admin_state[c.from_user.id]['max_parts'] = int(c.data.split("_")[1])
    bot.edit_message_text("✅ ظرفیت ثبت شد.", c.message.chat.id, c.message.message_id)
    kb = types.InlineKeyboardMarkup(row_width=3).add(*[types.InlineKeyboardButton(f"🏆 {v} برنده", callback_data=f"w_{v}", style="primary") for v in [1,2,3,5,10]], types.InlineKeyboardButton("✅ دستی", callback_data="m_win", style="success"), types.InlineKeyboardButton("❌ لغو", callback_data="c_draw", style="danger"))
    bot.send_message(c.message.chat.id, "🎁 **گام ۴/۵: تعداد برنده**", reply_markup=kb, parse_mode='Markdown')

def wiz_cap_m(m):
    if not is_admin(m.from_user.id) or not m.text.isdigit(): return bot.send_message(m.chat.id, "❌ عدد بفرست!")
    admin_state[m.from_user.id]['max_parts'] = int(m.text)
    bot.send_message(m.chat.id, "✅ ظرفیت ثبت شد.")
    kb = types.InlineKeyboardMarkup(row_width=3).add(*[types.InlineKeyboardButton(f"🏆 {v} برنده", callback_data=f"w_{v}", style="primary") for v in [1,2,3,5,10]], types.InlineKeyboardButton("✅ دستی", callback_data="m_win", style="success"), types.InlineKeyboardButton("❌ لغو", callback_data="c_draw", style="danger"))
    bot.send_message(m.chat.id, "🎁 **گام ۴/۵: تعداد برنده**", reply_markup=kb, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda c: (c.data.startswith("w_") or c.data=="m_win") and is_admin(c.from_user.id))
def wiz_win(c):
    bot.answer_callback_query(c.id)
    if c.data == "m_win":
        msg = bot.send_message(c.message.chat.id, "🎁 تعداد برنده‌ها را وارد کن (مثلاً `5`):")
        return bot.register_next_step_handler(msg, wiz_win_m)
    admin_state[c.from_user.id]['winners'] = int(c.data.split("_")[1])
    bot.edit_message_text("✅ ثبت شد.", c.message.chat.id, c.message.message_id)
    msg = bot.send_message(c.message.chat.id, "📢 **گام ۵/۵: کانال**\nآیدی کانال (مثلاً `@MyChannel`):")
    bot.register_next_step_handler(msg, wiz_chan)

def wiz_win_m(m):
    if not is_admin(m.from_user.id) or not m.text.isdigit(): return bot.send_message(m.chat.id, "❌ عدد بفرست!")
    admin_state[m.from_user.id]['winners'] = int(m.text)
    msg = bot.send_message(m.chat.id, "📢 **گام ۵/۵: کانال**\nآیدی کانال (مثلاً `@MyChannel`):")
    bot.register_next_step_handler(msg, wiz_chan)

def wiz_chan(m):
    if not is_admin(m.from_user.id): return
    data = admin_state[m.from_user.id]; channel = m.text
    
    new_draw = {
        "id": int(time.time()), "channel": channel, "end_time": data['end_time'], 
        "title": data['title'], "status": "active", "message_id": 0, 
        "max_parts": data['max_parts'], "winners_count": data['winners']
    }
    draws_col.insert_one(new_draw)
    did = new_draw['id']
    
    admin_state.pop(m.from_user.id, None)
    kb = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🎁 شرکت در قرعه‌کشی", url=f"https://t.me/{BOT_USERNAME}?start=draw_{did}", style="primary"), types.InlineKeyboardButton("0 شرکت کننده 💫", callback_data="noop", style="primary"))
    try:
        mid = bot.send_message(channel, f"🎉 **{data['title']}**\nبرای شرکت کلیک کن:", reply_markup=kb, parse_mode='Markdown').message_id
        draws_col.update_one({"id": did}, {"$set": {"message_id": mid}})
        bot.send_message(m.chat.id, f"✅ **قرعه‌کشی ارسال شد!**\nلینک: `https://t.me/{BOT_USERNAME}?start=draw_{did}`", parse_mode='Ma
