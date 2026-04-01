from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import random

TOKEN = "8787323027:AAHfijqRVcgwf3v5i-kUgTwPzU0c3RakCtM"

# ===== DATA =====
xp = {}
level = {}
bad_words = ["fuck", "bc", "mc"]
game_data = {}

# ===== START =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    xp.setdefault(uid, 0)
    level.setdefault(uid, 1)
    await update.message.reply_text("🔥 Combo Bot Active!\nUse /help")

# ===== HELP =====
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/tagall - tag admins\n"
        "/rank - your level\n"
        "/top - leaderboard\n"
        "/repeat 3 hi\n"
        "/game - play game\n"
    )

# ===== TAG ALL =====
async def tagall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    admins = await context.bot.get_chat_administrators(chat.id)

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
    msg = "🏆 Top Users:\n"
    for i, (uid, pts) in enumerate(sorted_users[:5], start=1):
        msg += f"{i}. {pts} XP\n"
    await update.message.reply_text(msg)

# ===== CHAT + XP + FILTER =====
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    uid = update.effective_user.id

    # filter
    for word in bad_words:
        if word in text:
            try:
                await update.message.delete()
            except:
                pass
            await update.message.reply_text("⚠️ Abuse not allowed!")
            return

    # xp system
    xp[uid] = xp.get(uid, 0) + 2
    if xp[uid] >= level.get(uid, 1) * 50:
        level[uid] = level.get(uid, 1) + 1
        await update.message.reply_text(f"🎉 Level UP! {level[uid]}")

    # smart reply
    replies = ["Nice 😎", "Cool 😄", "Okay 👍", "Haha 😂"]
    await update.message.reply_text(random.choice(replies))

# ===== APP =====
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_cmd))
app.add_handler(CommandHandler("tagall", tagall))
app.add_handler(CommandHandler("repeat", repeat))
app.add_handler(CommandHandler("game", game))
app.add_handler(CommandHandler("rank", rank))
app.add_handler(CommandHandler("top", top))

app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), chat))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), guess))

print("Combo Bot Started 🔥")
app.run_polling()
