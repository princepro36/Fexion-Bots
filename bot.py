from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

TOKEN = "8787323027:AAHfijqRVcgwf3v5i-kUgTwPzU0c3RakCtM"

# ===== DATA =====
user_points = {}
user_names = {}
user_prefix = {}

# ===== START =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    user_names[uid] = update.effective_user.first_name
    user_points.setdefault(uid, 0)
    user_prefix.setdefault(uid, "🤖")

    await update.message.reply_text("🔥 Ranking Bot Active!\nUse /rank /top")

# ===== MESSAGE TRACK =====
async def track(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id

    user_points[uid] = user_points.get(uid, 0) + 1
    user_names[uid] = update.effective_user.first_name

# ===== RANK =====
async def rank(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    points = user_points.get(uid, 0)
    prefix = user_prefix.get(uid, "🤖")

    await update.message.reply_text(f"{prefix} You have {points} points!")

# ===== TOP =====
async def top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sorted_users = sorted(user_points.items(), key=lambda x: x[1], reverse=True)

    msg = "🏆 Top Users:\n"
    for i, (uid, pts) in enumerate(sorted_users[:5], start=1):
        name = user_names.get(uid, "User")
        msg += f"{i}. {name} - {pts}\n"

    await update.message.reply_text(msg)

# ===== CUSTOM PREFIX (CLONE FEEL) =====
async def setprefix(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id

    if not context.args:
        await update.message.reply_text("Use: /setprefix 😎")
        return

    prefix = context.args[0]
    user_prefix[uid] = prefix

    await update.message.reply_text(f"✅ Your bot prefix set to {prefix}")

# ===== APP =====
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("rank", rank))
app.add_handler(CommandHandler("top", top))
app.add_handler(CommandHandler("setprefix", setprefix))

app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), track))

print("Ranking Bot Started 🔥")
app.run_polling()
