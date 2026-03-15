import asyncio
import importlib

from pyrogram import idle

import config
from config import BANNED_USERS
from ChampuMusic import HELPABLE, LOGGER, app, userbot
from ChampuMusic.core.call import Champu
from ChampuMusic.plugins import ALL_MODULES
from ChampuMusic.utils.database import get_banned_users, get_gbanned

async def init():
    # Session strings check karne ka aasaan tareeka
    if not any([config.STRING1, config.STRING2, config.STRING3, config.STRING4, config.STRING5]):
        LOGGER("ChampuMusic").error(
            "ᴀssɪsᴛᴀɴᴛ ᴄʟɪᴇɴᴛ ᴠᴀʀɪᴀʙʟᴇs ɴᴏᴛ ᴅᴇғɪɴᴇᴅ, ᴇxɪᴛɪɴɢ..."
        )
        return

    if not config.SPOTIFY_CLIENT_ID and not config.SPOTIFY_CLIENT_SECRET:
        LOGGER("ChampuMusic").warning(
            "ɴᴏ sᴘᴏᴛɪғʏ ᴠᴀʀs ᴅᴇғɪɴᴇᴅ. ʏᴏᴜʀ ʙᴏᴛ ᴡᴏɴ'ᴛ ʙᴇ ᴀʙʟᴇ ᴛᴏ ᴘʟᴀʏ sᴘᴏᴛɪғʏ ǫᴜᴇʀɪᴇs..."
        )

    # Bot aur Userbot ko start karna
    await app.start()
    await userbot.start()

    # Banned users ko load karna
    try:
        gbanned = await get_gbanned()
        for user_id in gbanned:
            BANNED_USERS.add(user_id)
        
        banned = await get_banned_users()
        for user_id in banned:
            BANNED_USERS.add(user_id)
    except Exception as e:
        LOGGER("ChampuMusic").error(f"Error loading banned users: {e}")

    # Modules ko dynamically import karna
    for all_module in ALL_MODULES:
        imported_module = importlib.import_module(all_module)

        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
                HELPABLE[imported_module.__MODULE__.lower()] = imported_module
    
    LOGGER("ChampuMusic.plugins").info("sᴜᴄᴄᴇssғᴜʟʟʏ ɪᴍᴘᴏʀᴛᴇᴅ ᴍᴏᴅᴜʟᴇs...")

    # Calling client start karna
    await Champu.start()
    await Champu.decorators()

    LOGGER("ChampuMusic").info("Champu Music Bot has been successfully started.")
    
    # Bot ko idle mode me rakhna jab tak stop na kiya jaye
    await idle()
    
    # Stop hone par cleanup
    await app.stop()
    await userbot.stop()
    LOGGER("ChampuMusic").info("Stopping Champu Music Bot... Goodbye!")

if __name__ == "__main__":
    try:
        asyncio.run(init())
    except KeyboardInterrupt:
        pass
