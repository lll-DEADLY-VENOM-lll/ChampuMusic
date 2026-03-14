import asyncio
import threading
import uvloop
from flask import Flask
from pyrogram import Client, idle
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import ChatWriteForbidden, PeerIdInvalid
from pyrogram.types import (
    BotCommand,
    BotCommandScopeAllGroupChats,
    BotCommandScopeAllPrivateChats,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

import config  # यह config.py को इम्पोर्ट कर रहा है
from ..logging import LOGGER

uvloop.install()

# Flask for Health Checks
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive and running!"

def run_flask():
    try:
        app.run(host="0.0.0.0", port=8000, debug=False)
    except Exception as e:
        print(f"Flask Error: {e}")

class ChampuBot(Client):
    def __init__(self):
        LOGGER(__name__).info("Initializing Champu Bot...")
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

        button = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="๏ ᴀᴅᴅ ᴍᴇ ɪɴ ɢʀᴏᴜᴘ ๏", url=f"https://t.me/{self.username}?startgroup=true")]]
        )

        # LOG_GROUP_ID Logic (Fixing the Warning)
        log_id = getattr(config, 'LOG_GROUP_ID', None)

        if log_id:
            try:
                await self.send_photo(
                    chat_id=int(log_id),
                    photo=getattr(config, 'START_IMG_URL', None),
                    caption=f"╔════❰𝐖𝐄𝐋𝐂𝐎𝐌𝐄❱════❍⊱❁۪۪\n║\n║┣⪼🥀𝐁𝐨𝐭 𝐒𝐭𝐚𝐫𝐭𝐞𝐝 𝐁𝐚𝐛𝐲🎉\n║\n║┣⪼ {self.name}\n║\n║┣⪼🎈𝐈𝐃:- `{self.id}` \n║\n║┣⪼🎄@{self.username} \n║ \n║┣⪼💖𝐓𝐡𝐚𝐧𝐤𝐬 𝐅𝐨𝐫 𝐔𝐬𝐢𝐧𝐠😍\n║\n╚════════════════❍⊱❁",
                    reply_markup=button,
                )
                LOGGER(__name__).info(f"Startup message sent to Log Group: {log_id}")
            except (PeerIdInvalid, ValueError):
                LOGGER(__name__).error("LOG_GROUP_ID invalid hai! Check karein ki ID -100 se start ho.")
            except ChatWriteForbidden:
                LOGGER(__name__).error("Bot log group mein admin nahi hai ya message nahi bhej sakta!")
            except Exception as e:
                LOGGER(__name__).error(f"Startup Error: {e}")
        else:
            LOGGER(__name__).warning("LOG_GROUP_ID config.py mein nahi mila!")

        # Set Commands
        if getattr(config, 'SET_CMDS', False):
            try:
                await self.set_bot_commands(
                    [BotCommand("start", "Start Bot"), BotCommand("ping", "Check Status")],
                    scope=BotCommandScopeAllPrivateChats()
                )
                await self.set_bot_commands(
                    [BotCommand("play", "Play Music"), BotCommand("skip", "Skip Song")],
                    scope=BotCommandScopeAllGroupChats()
                )
            except Exception as e:
                LOGGER(__name__).error(f"Commands set nahi ho paaye: {e}")

        LOGGER(__name__).info(f"MusicBot Started as @{self.username}")

async def main():
    bot = ChampuBot()
    await bot.start()
    await idle()

if __name__ == "__main__":
    # Start Flask Server
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()
    
    # Start Bot
    asyncio.run(main())
