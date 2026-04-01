from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import InputStream, InputAudioStream
import yt_dlp
import asyncio

# 🔑 DETAILS
API_ID = 10324316
API_HASH = "9dbde6e2365389984aa3dd6e3d24b3f6"
BOT_TOKEN = "8787323027:AAHfijqRVcgwf3v5i-kUgTwPzU0c3RakCtM"

# assistant session string (optional but needed)
SESSION_STRING = "BQCdiVwAezxyHOA5jIKsucHS8D1XQlO5nMa0rF1C-4PKKW3qjF1JmgOI96jTpPpZwmUBQ7y4JpBtd2QSEPwmp04Omh9wAfvGfCJNWth_IMMPCDaUHHM7EHlmBUyqcwrEkIKmN-Mge9bkrEntpoSiWok0cytULOWGhB6F6rVjMR8IbPgB6UDHr09UHEQcwtYFNL4x5j44gcJ0AKto_F4GZ0_n67UhamLx5gTDqTgfOtMHibedoMA3M3joSelCGiDth0MHu-_OqaFt-7N-AwwEj3TDDqPSTa0_p6TIsqzEWEsaYziFcRQ3Icyke4Yy_jSuX5F3PxUx2T7hPqUT6m1FQhdKWl0v5wAAAAIF-3XVAA"

app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
assistant = Client("assistant", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

call = PyTgCalls(assistant)

# 🎵 PLAY COMMAND
@app.on_message(filters.command("play") & filters.group)
async def play(_, message):
    query = " ".join(message.command[1:])

    if not query:
        await message.reply("Use: /play song name")
        return

    await message.reply("🔍 Searching...")

    ydl_opts = {"format": "bestaudio", "quiet": True}

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)
            url = info['entries'][0]['url']
            title = info['entries'][0]['title']

        await message.reply(f"🎶 Playing: {title}")

        await call.join_group_call(
            message.chat.id,
            InputStream(InputAudioStream(url)),
        )

    except Exception as e:
        await message.reply("❌ Error")

# START
async def main():
    await app.start()
    await assistant.start()
    await call.start()
    print("Bot Started 🔥")

    await idle()

from pyrogram.idle import idle
asyncio.get_event_loop().run_until_complete(main())
