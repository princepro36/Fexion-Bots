from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters, ConversationHandler
)
import random

TOKEN = "8787323027:AAEQ43eIv8q0CnNUo6-LweHMhWt7lJeYYfw"

# ===== DATA =====
xp = {}
level = {}
warnings = {}
game_data = {}

bad_words = ["fuck", "bc", "mc"]
MAX_WARN = 3

# ===== START =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    xp.setdefault(uid, 0)
    level.setdefault(uid, 1)
    await update.message.reply_text("🔥 Ultimate Bot Active!\nUse /help")

# ===== HELP =====
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/tagall\n/rank\n/top\n/repeat 3 hi\n/game\n/clone"
    )

# ===== TAGALL =====
async def tagall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admins = await context.bot.get_chat_administrators(update.effective_chat.id)
    msg = "📢 Attention:\n\n"
    for user in admins:
        msg += f"[{user.user.first_name}](tg://user?id={user.user.id}) "
    await update.message.reply_text(msg, parse_mode="Markdown")

# ===== REPEAT =====
async def repeat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        count = int(context.args[0])
        msg = " ".join(context.args[1:])
        for _ in range(min(count, 5)):
            await update.message.reply_text(msg)
    except:
        await update.message.reply_text("Use: /repeat 3 hello")

# ===== GAME =====
async def game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    num = random.randint(1, 20)
    game_data[update.effective_user.id] = num
    await update.message.reply_text("🎮 Guess number (1-20)")

async def guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in game_data:
        return
    try:
        g = int(update.message.text)
        real = game_data[uid]
        if g == real:
            await update.message.reply_text("🎉 Correct!")
            del game_data[uid]
        elif g > real:
            await update.message.reply_text("📉 Too high")
        else:
            await update.message.reply_text("📈 Too low")
    except:
        pass

# ===== RANK =====
async def rank(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    await update.message.reply_text(f"XP: {xp.get(uid,0)} | Level: {level.get(uid,1)}")

# ===== TOP =====
async def top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sorted_users = sorted(xp.items(), key=lambda x: x[1], reverse=True)
    msg = "🏆 Leaderboard:\n"
    for i, (uid, pts) in enumerate(sorted_users[:5], start=1):
        msg += f"{i}. {pts} XP\n"
    await update.message.reply_text(msg)

# ===== FILTER + XP =====
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    uid = update.effective_user.id

    # filter + warning
    for word in bad_words:
        if word in text:
            try:
                await update.message.delete()
            except:
                pass

            warnings[uid] = warnings.get(uid, 0) + 1
            count = warnings[uid]

            await update.message.reply_text(f"⚠️ Warning {count}/{MAX_WARN}")

            if count >= MAX_WARN:
                try:
                    await context.bot.ban_chat_member(update.effective_chat.id, uid)
                    await update.message.reply_text("🚫 User banned!")
                except:
                    await update.message.reply_text("❌ Cannot ban user")
            return

    # XP system
    xp[uid] = xp.get(uid, 0) + 2
    if xp[uid] >= level.get(uid, 1) * 50:
        level[uid] = level.get(uid, 1) + 1
        await update.message.reply_text(f"🎉 Level UP! {level[uid]}")

    # chatbot reply
    replies = ["Nice 😎", "Cool 👍", "Okay 🤖", "Haha 😂"]
    await update.message.reply_text(random.choice(replies))

# ===== CLONE SYSTEM =====
ASK_TOKEN = 1

async def clone(update, context):
    await update.message.reply_text("🤖 Send your bot token:")
    return ASK_TOKEN

async def process_token(update, context):
    token = update.message.text.strip()

    guide = f"""
🔥 CLONE READY!

1. Create GitHub repo
2. Add bot.py:

TOKEN = "{token}"

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Clone Bot Running 😎")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()

3. requirements.txt:
python-telegram-bot==20.7

4. Deploy on Render 😎
"""

    await update.message.reply_text(guide)
    return ConversationHandler.END

async def cancel(update, context):
    await update.message.reply_text("❌ Cancelled")
    return ConversationHandler.END

# ===== APP =====
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_cmd))
app.add_handler(CommandHandler("tagall", tagall))
app.add_handler(CommandHandler("repeat", repeat))
app.add_handler(CommandHandler("game", game))
app.add_handler(CommandHandler("rank", rank))
app.add_handler(CommandHandler("top", top))

clone_handler = ConversationHandler(
    entry_points=[CommandHandler("clone", clone)],
    states={
        ASK_TOKEN: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_token)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

app.add_handler(clone_handler)

app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), chat))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), guess))

print("Ultimate Bot Started 🔥")
app.run_polling()
