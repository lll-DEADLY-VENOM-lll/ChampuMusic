# Copyright (C) 2024 by THE-VIP-BOY-OP@Github
import asyncio
import threading
import uvloop
from flask import Flask
from pyrogram import Client, idle
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import ChatWriteForbidden, PeerIdInvalid
from pyrogram.types import (
    BotCommand,
    BotCommandScopeAllChatAdministrators,
    BotCommandScopeAllGroupChats,
    BotCommandScopeAllPrivateChats,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

import config
from ..logging import LOGGER

uvloop.install()

# Flask for Keep-Alive (Render/Heroku)
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running"

def run_flask():
    app.run(host="0.0.0.0", port=8000, debug=False)

class ChampuBot(Client):
    def __init__(self):
        LOGGER(__name__).info("Starting Bot...")
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

        # LOG_GROUP_ID Check
        if hasattr(config, 'LOG_GROUP_ID') and config.LOG_GROUP_ID:
            try:
                LOGGER_ID = int(config.LOG_GROUP_ID)
                await self.send_photo(
                    chat_id=LOGGER_ID,
                    photo=config.START_IMG_URL if hasattr(config, 'START_IMG_URL') else None,
                    caption=f"╔════❰𝐖𝐄𝐋𝐂𝐎𝐌𝐄❱════❍⊱❁۪۪\n║\n║┣⪼🥀𝐁𝐨𝐭 𝐒𝐭𝐚𝐫𝐭𝐞𝐝 𝐁𝐚𝐛𝐲🎉\n║\n║┣⪼ {self.name}\n║\n║┣⪼🎈𝐈𝐃:- `{self.id}` \n║\n║┣⪼🎄@{self.username} \n║ \n║┣⪼💖𝐓𝐡𝐚𝐧𝐤𝐬 𝐅𝐨𝐫 𝐔𝐬𝐢𝐧𝐠😍\n║\n╚════════════════❍⊱❁",
                    reply_markup=button,
                )
            except (PeerIdInvalid, ValueError):
                LOGGER(__name__).error("Log Group ID galat hai ya Bot group mein nahi hai!")
            except ChatWriteForbidden:
                LOGGER(__name__).error("Bot ke paas Log Group mein message bhejne ki permission nahi hai!")
            except Exception as e:
                LOGGER(__name__).error(f"Unexpected Log Error: {e}")
        else:
            LOGGER(__name__).warning("LOG_GROUP_ID config mein nahi mila. Startup message skip kiya gaya.")

        # Commands Set Karne ke liye
        if hasattr(config, 'SET_CMDS') and config.SET_CMDS:
            try:
                await self.set_bot_commands(
                    commands=[
                        BotCommand("start", "Start the bot"),
                        BotCommand("help", "Get the help menu"),
                        BotCommand("ping", "Check bot status"),
                    ],
                    scope=BotCommandScopeAllPrivateChats(),
                )
                await self.set_bot_commands(
                    commands=[
                        BotCommand("play", "Play song"),
                        BotCommand("stop", "Stop music"),
                        BotCommand("pause", "Pause music"),
                        BotCommand("resume", "Resume music"),
                        BotCommand("skip", "Skip current song"),
                    ],
                    scope=BotCommandScopeAllGroupChats(),
                )
            except Exception as e:
                LOGGER(__name__).error(f"Failed to set commands: {e}")

        LOGGER(__name__).info(f"MusicBot Started as {self.name}")

async def anony_boot():
    bot = ChampuBot()
    await bot.start()
    await idle()

if __name__ == "__main__":
    # Flask ko separate thread mein chalayein
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()
    
    # Bot ko main loop mein chalayein
    asyncio.run(anony_boot())
