import asyncio
import uvloop

# --- Event Loop Fix for Python 3.10+ ---
try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

# uvloop install karna fast performance ke liye
uvloop.install()

import pyrogram
from pyrogram import Client
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import (
    BotCommand,
    BotCommandScopeAllChatAdministrators,
    BotCommandScopeAllGroupChats,
    BotCommandScopeAllPrivateChats,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from pyrogram.errors.exceptions.forbidden_403 import ChatWriteForbidden
import config

from ..logging import LOGGER


class ChampuBot(Client):
    def __init__(self):
        LOGGER(__name__).info(f"sᴛᴀʀᴛɪɴɢ ʙᴏᴛ...")
        super().__init__(
            "ChampuMusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            sleep_threshold=180, # Additional safety for flood waits
        )

    async def start(self):
        await super().start()
        get_me = await self.get_me()
        self.username = get_me.username
        self.id = get_me.id
        self.name = get_me.first_name + " " + (get_me.last_name or "")
        self.mention = get_me.mention

        # Create the button
        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="๏ ᴀᴅᴅ ᴍᴇ ɪɴ ɢʀᴏᴜᴘ ๏",
                        url=f"https://t.me/{self.username}?startgroup=true",
                    )
                ]
            ]
        )

        # Try to send a message to the logger group
        if config.LOGGER_ID:
            try:
                await self.send_photo(
                    config.LOGGER_ID,
                    photo=config.START_IMG_URL,
                    caption=f"╔════❰𝗪𝗘𝗟𝗖𝗢𝗠𝗘❱════❍⊱❁۪۪\n║\n║┣⪼🥀ʙᴏᴛ sᴛᴀʀᴛᴇᴅ🎉\n║\n║┣⪼ {self.name}\n║\n║┣⪼🎈ɪᴅ:- `{self.id}` \n║\n║┣⪼🎄@{self.username} \n║ \n║┣⪼💖ᴛʜᴀɴᴋs ғᴏʀ ᴜsɪɴɢ😍\n║\n╚════════════════❍⊱❁",
                    reply_markup=button,
                )
            except ChatWriteForbidden:
                LOGGER(__name__).error("Bot cannot write to the log group. Make sure it has permissions.")
            except Exception as e:
                LOGGER(__name__).error(f"Unexpected error while sending to log group: {e}")
                try:
                    await self.send_message(
                        config.LOGGER_ID,
                        f"╔═══❰𝗪𝗘𝗟𝗖𝗢𝗠𝗘❱═══❍⊱❁۪۪\n║\n║┣⪼🥀ʙᴏᴛ sᴛᴀʀᴛᴇᴅ🎉\n║\n║◈ {self.name}\n║\n║┣⪼🎈ɪᴅ:- `{self.id}` \n║\n║┣⪼🎄@{self.username} \n║ \n║┣⪼💖ᴛʜᴀɴᴋs ғᴏʀ ᴜsɪɴɢ😍\n║\n╚══════════════❍⊱❁",
                        reply_markup=button,
                    )
                except Exception:
                    pass
        else:
            LOGGER(__name__).warning(
                "LOGGER_ID is not set, skipping log group notifications."
            )

        # Setting commands
        if config.SET_CMDS:
            try:
                await self.set_bot_commands(
                    commands=[
                        BotCommand("start", "sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ"),
                        BotCommand("help", "ɢᴇᴛ ᴛʜᴇ ʜᴇʟᴘ ᴍᴇɴᴜ"),
                        BotCommand("ping", "ᴄʜᴇᴄᴋ ʙᴏᴛ ɪs ᴀʟɪᴠᴇ ᴏʀ ᴅᴇᴀᴅ"),
                    ],
                    scope=BotCommandScopeAllPrivateChats(),
                )
                await self.set_bot_commands(
                    commands=[
                        BotCommand("play", "Start playing requested song"),
                        BotCommand("stop", "Stop the current song"),
                        BotCommand("pause", "Pause the current song"),
                        BotCommand("resume", "Resume the paused song"),
                        BotCommand("queue", "Check the queue of songs"),
                        BotCommand("skip", "Skip the current song"),
                        BotCommand("volume", "Adjust the music volume"),
                        BotCommand("lyrics", "Get lyrics of the song"),
                    ],
                    scope=BotCommandScopeAllGroupChats(),
                )
                await self.set_bot_commands(
                    commands=[
                        BotCommand("start", "❥ ✨ᴛᴏ sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ✨"),
                        BotCommand("ping", "❥ 🍁ᴛᴏ ᴄʜᴇᴄᴋ ᴛʜᴇ ᴘɪɴɢ🍁"),
                        BotCommand("help", "❥ 🥺ᴛᴏ ɢᴇᴛ ʜᴇʟᴘ🥺"),
                        BotCommand("vctag", "❥ 😇ᴛᴀɢᴀʟʟ ғᴏʀ ᴠᴄ🙈"),
                        BotCommand("stopvctag", "❥ 📍sᴛᴏᴘ ᴛᴀɢᴀʟʟ ғᴏʀ ᴠᴄ 💢"),
                        BotCommand("tagall", "❥ 🔻ᴛᴀɢ ᴀʟʟ ᴍᴇᴍʙᴇʀs ʙʏ ᴛᴇxᴛ🔻"),
                        BotCommand("cancel", "❥ 🔻ᴄᴀɴᴄᴇʟ ᴛʜᴇ ᴛᴀɢɢɪɴɢ🔻"),
                        BotCommand("settings", "❥ 🔻ᴛᴏ ɢᴇᴛ ᴛʜᴇ sᴇᴛᴛɪɴɢs🔻"),
                        BotCommand("reload", "❥ 🪐ᴛᴏ ʀᴇʟᴏᴀᴅ ᴛʜᴇ ʙᴏᴛ🪐"),
                        BotCommand("play", "❥ ❣️ᴛᴏ ᴘʟᴀʏ ᴛʜᴇ sᴏɴɢ❣️"),
                        BotCommand("vplay", "❥ ❣️ᴛᴏ ᴘʟᴀʏ ᴛʜᴇ ᴍᴜsɪᴄ ᴡɪᴛʜ ᴠɪᴅᴇᴏ❣️"),
                        BotCommand("pause", "❥ 🥀ᴛᴏ ᴘᴀᴜsᴇ ᴛʜᴇ sᴏɴɢs🥀"),
                        BotCommand("resume", "❥ 💖ᴛᴏ ʀᴇsᴜᴍᴇ ᴛʜᴇ sᴏɴɢ💖"),
                        BotCommand("end", "❥ 🐚ᴛᴏ ᴇᴍᴘᴛʏ ᴛʜᴇ ϙᴜᴇᴜᴇ🐚"),
                        BotCommand("queue", "❥ 🤨ᴛᴏ ᴄʜᴇᴄᴋ ᴛʜᴇ ϙᴜᴇᴜᴇ🤨"),
                        BotCommand("playlist", "❥ 🕺ᴛᴏ ɢᴇᴛ ᴛʜᴇ ᴘʟᴀʏʟɪsᴛ🕺"),
                        BotCommand("stop", "❥ ❤‍🔥ᴛᴏ sᴛᴏᴘ ᴛʜᴇ sᴏɴɢs❤‍🔥"),
                        BotCommand("lyrics", "❥ 🕊️ᴛᴏ ɢᴇᴛ ᴛʜᴇ ʟʏʀɪᴄs🕊️"),
                        BotCommand("song", "❥ 🔸ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ᴛʜᴇ sᴏɴɢ🔸"),
                        BotCommand("video", "❥ 🔸ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ᴛʜᴇ ᴠɪᴅᴇᴏ sᴏɴɢ🔸"),
                        BotCommand("gali", "❥ 🔻ᴛᴏ ʀᴇᴘʟʏ ғᴏʀ ғᴜɴ🔻"),
                        BotCommand("shayri", "❥ 🔻ᴛᴏ ɢᴇᴛ ᴀ sʜᴀʏᴀʀɪ🔻"),
                        BotCommand("love", "❥ 🔻ᴛᴏ ɢᴇᴛ ᴀ ʟᴏᴠᴇ sʜᴀʏᴀʀɪ🔻"),
                        BotCommand("sudolist", "❥ 🌱ᴛᴏ ᴄʜᴇᴄᴋ ᴛʜᴇ sᴜᴅᴏʟɪsᴛ🌱"),
                        BotCommand("owner", "❥ 💝ᴛᴏ ᴄʜᴇᴄᴋ ᴛʜᴇ ᴏᴡɴᴇʀ💝"),
                        BotCommand("update", "❥ 🐲ᴛᴏ ᴜᴘᴅᴀᴛᴇ ʙᴏᴛ🐲"),
                        BotCommand("gstats", "❥ 💘ᴛᴏ sᴛᴀᴛs ᴏғ ᴛʜᴇ ʙᴏᴛ💘"),
                        BotCommand("repo", "❥ 🍌ᴛᴏ ᴄʜᴇᴄᴋ ᴛʜᴇ 𝚁𝙴𝙿𝙾🍌"),
                    ],
                    scope=BotCommandScopeAllChatAdministrators(),
                )
            except Exception as e:
                LOGGER(__name__).error(f"Failed to set bot commands: {e}")

        # Check if bot is an admin in the logger group
        if config.LOGGER_ID:
            try:
                chat_member_info = await self.get_chat_member(
                    config.LOGGER_ID, self.id
                )
                if chat_member_info.status != ChatMemberStatus.ADMINISTRATOR:
                    LOGGER(__name__).error(
                        "Please promote Bot as Admin in Logger Group"
                    )
            except Exception as e:
                LOGGER(__name__).error(f"Error occurred while checking bot status: {e}")

        LOGGER(__name__).info(f"MusicBot Started as {self.name}")

    async def stop(self):
        await super().stop()
