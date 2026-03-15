import asyncio
from os import getenv
from dotenv import load_dotenv
from pyrogram import Client
import config
from ..logging import LOGGER

load_dotenv()

BOT_TOKEN = getenv("BOT_TOKEN", "")
MONGO_DB_URI = getenv("MONGO_DB_URI", "")
STRING_SESSION = getenv("STRING_SESSION", "")

assistants = []
assistantids = []

class Userbot(Client):
    def __init__(self):
        self.clients = []
        # List of session strings from config
        self.sessions = [
            config.STRING1, config.STRING2, config.STRING3, 
            config.STRING4, config.STRING5
        ]
        
        for i, session in enumerate(self.sessions, start=1):
            if session:
                client = Client(
                    name=f"ChampuAss{i}",
                    api_id=config.API_ID,
                    api_hash=config.API_HASH,
                    session_string=str(session),
                    no_updates=False if i == 1 else True,
                )
                self.clients.append(client)
                # Dynamic attribute assignment like self.one, self.two etc.
                setattr(self, ["one", "two", "three", "four", "five"][i-1], client)

    async def start(self):
        LOGGER(__name__).info("sᴛᴀʀᴛɪɴɢ ᴀssɪsᴛᴀɴᴛs...")
        
        for i, client in enumerate(self.clients, start=1):
            try:
                await client.start()
                
                # Join support chats
                for chat in ["about_deadly_venom", "NOBITA_SUPPORT"]:
                    try:
                        await client.join_chat(chat)
                    except Exception:
                        pass
                
                assistants.append(i)
                
                # Get Me info
                me = await client.get_me()
                client.id = me.id
                client.name = me.mention
                client.username = me.username
                assistantids.append(me.id)
                
                # Notification to Logger Group
                try:
                    await client.send_message(
                        config.LOGGER_ID, 
                        f"✅ **ᴀssɪsᴛᴀɴᴛ {i} sᴛᴀʀᴛᴇᴅ**\n\n**Name:** {me.first_name}\n**ID:** {me.id}"
                    )
                    
                    # NOTE: Security risk - avoid sending sensitive info like MONGO_DB_URI to Telegram chats
                    # Maine sirf startup alert rakha hai.
                    if i == 1:
                        log_msg = await client.send_message(config.LOGGERS, "Assistant 1 is online!")
                        await asyncio.sleep(2)
                        await log_msg.delete()

                except Exception as e:
                    LOGGER(__name__).error(f"Assistant {i} failed to send message to log group: {e}")

                LOGGER(__name__).info(f"ᴀssɪsᴛᴀɴᴛ {i} sᴛᴀʀᴛᴇᴅ ᴀs {me.first_name}")
                
            except Exception as e:
                LOGGER(__name__).error(f"ᴀssɪsᴛᴀɴᴛ {i} failed to start: {str(e)}")

    async def stop(self):
        LOGGER(__name__).info("sᴛᴏᴘᴘɪɴɢ ᴀssɪsᴛᴀɴᴛs...")
        for client in self.clients:
            try:
                await client.stop()
            except Exception:
                pass
