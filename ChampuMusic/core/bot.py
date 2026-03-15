import asyncio
import threading
import uvloop
import logging
from flask import Flask
from pyrogram import Client, idle
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import ChatWriteForbidden, PeerIdInvalid, FloodWait
from pyrogram.types import (
    BotCommand,
    BotCommandScopeAllGroupChats,
    BotCommandScopeAllPrivateChats,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

import config  # config.py file ko import kar raha hai

# UVLOOP Optimization
uvloop.install()

# LOGGING SETUP
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)
LOGGER = logging.getLogger("ChampuBot")

# FLASK FOR HEALTH CHECKS (Uptime ke liye)
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive and running!"

def run_flask():
    try:
        # Port 8000 default hai (Render/Koyeb ke liye perfect)
        app.run(host="0.0.0.0", port=8000, debug=False)
    except Exception as e:
        LOGGER.error(f"Flask Error: {e}")

# BOT CLASS
class ChampuBot(Client):
    def __init__(self):
        LOGGER.info("Initializing Champu Bot...")
        super().__init__(
            "ChampuMusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            ipv6=False,
        )

    async def start(self):
        await super().start()
        get_me = await self.get_me()
        self.username = get_me.username
        self.id = get_me.id
        self.name = f"{get_me.first_name} {get_me.last_name or ''}"
        self.mention = get_me.mention

        # Startup Button
        button = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="๏ ᴀᴅᴅ ᴍᴇ ɪɴ ɢʀᴏᴜᴘ ๏", url=f"https://t.me/{self.username}?startgroup=true")]]
        )

        # LOG_GROUP_ID LOGIC
        log_id = getattr(config, 'LOG_GROUP_ID', None)

        if log_id:
            try:
                # Group ID ko integer mein confirm karna
                chat_id = int(log_id)
                
                await self.send_photo(
                    chat_id=chat_id,
                    photo=config.START_IMG_URL,
                    caption=(
                        f"╔════❰ 𝐖𝐄𝐋𝐂𝐎𝐌𝐄 ❱════❍⊱❁۪۪\n"
                        f"║\n"
                        f"║┣⪼ 🥀 𝐁𝐨𝐭 𝐒𝐭𝐚𝐫𝐭𝐞𝐝 𝐁𝐚𝐛𝐲 🎉\n"
                        f"║\n"
                        f"║┣⪼ {self.name}\n"
                        f"║\n"
                        f"║┣⪼ 🎈 𝐈𝐃:- `{self.id}`\n"
                        f"║\n"
                        f"║┣⪼ 🎄 @{self.username}\n"
                        f"║\n"
                        f"║┣⪼ 💖 𝐓𝐡𝐚𝐧𝐤𝐬 𝐅𝐨𝐫 𝐔𝐬𝐢𝐧𝐠 😍\n"
                        f"║\n"
                        f"╚════════════════❍⊱❁"
                    ),
                    reply_markup=button,
                )
                LOGGER.info(f"Startup message sent to Log Group: {chat_id}")
            except PeerIdInvalid:
                LOGGER.error("LOG_GROUP_ID Invalid hai! Bot ko pehle us group mein add karke admin banayein.")
            except ChatWriteForbidden:
                LOGGER.error("Bot ko log group mein message bhejne ki permission nahi hai (Admin nahi hai).")
            except FloodWait as e:
                await asyncio.sleep(e.value)
            except Exception as e:
                LOGGER.error(f"Startup Message Error: {e}")
        else:
            LOGGER.warning("LOG_GROUP_ID config.py mein missing hai! Log group message nahi jayega.")

        # SET BOT COMMANDS
        if config.SET_CMDS:
            try:
                await self.set_bot_commands(
                    [
                        BotCommand("start", "Start the Bot"),
                        BotCommand("help", "Get Help Menu"),
                        BotCommand("ping", "Check Bot Status"),
                    ],
                    scope=BotCommandScopeAllPrivateChats()
                )
                await self.set_bot_commands(
                    [
                        BotCommand("play", "Play Music"),
                        BotCommand("skip", "Skip Current Song"),
                        BotCommand("stop", "Stop Music"),
                        BotCommand("vc", "VC Control"),
                    ],
                    scope=BotCommandScopeAllGroupChats()
                )
                LOGGER.info("Bot commands auto-set successfully.")
            except Exception as e:
                LOGGER.error(f"Commands set nahi ho paaye: {e}")

        LOGGER.info(f"MusicBot Started successfully as @{self.username}")

    async def stop(self):
        await super().stop()
        LOGGER.info("Bot Stopped. Bye!")

# MAIN RUN FUNCTION
async def main():
    bot = ChampuBot()
    await bot.start()
    await idle()

if __name__ == "__main__":
    # 1. Flask server ko alag thread mein chalayein
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()
    
    # 2. Bot ko run karein
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
