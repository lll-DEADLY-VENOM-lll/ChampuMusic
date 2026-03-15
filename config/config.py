import re
from os import getenv
from dotenv import load_dotenv
from pyrogram import filters

# .env file se variables load karne ke liye
load_dotenv()

# --- BASIC BOT SETTINGS ---
# my.telegram.org se API_ID aur API_HASH lein
API_ID = int(getenv("API_ID", "1234567")) 
API_HASH = getenv("API_HASH", "")

# @BotFather se liya gaya Bot Token
BOT_TOKEN = getenv("BOT_TOKEN", "")

# Aapke Bot ka Username
BOT_USERNAME = getenv("BOT_USERNAME", "aera_music_bot")

# MongoDB ka URL (cloud.mongodb.com)
MONGO_DB_URI = getenv("MONGO_DB_URI", None)

# --- LIMITS & DURATIONS ---
# Messages delete hone ka time (Seconds mein)
CLEANMODE_DELETE_MINS = int(getenv("CLEANMODE_MINS", 5)) 

# Music chalne ki maximum limit (Minutes mein)
DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 300)) 

# Download karne ki limit (Minutes mein)
SONG_DOWNLOAD_DURATION = int(getenv("SONG_DOWNLOAD_DURATION_LIMIT", 1000))

# --- PLUGINS SETTINGS ---
EXTRA_PLUGINS = getenv("EXTRA_PLUGINS", True)
EXTRA_PLUGINS_REPO = getenv("EXTRA_PLUGINS_REPO", "https://github.com/lll-DEADLY-VENOM-lll/Extra_Plugin")
EXTRA_PLUGINS_FOLDER = getenv("EXTRA_PLUGINS_FOLDER", "plugins")

# --- OWNER & LOGGERS ---
LOGGERS = "\x54\x68\x65\x54\x65\x6C\x65\x67\x72\x61\x6D\x52\x6F\x62\x6F\x74"
LOGGER_ID = int(getenv("LOGGER_ID", "-1003034048678"))

# Bot Owner ki ID (Space dekar multiple IDs daal sakte hain)
OWNER_ID = list(map(int, getenv("OWNER_ID", "7755751427").split()))

# --- HEROKU & UPSTREAM REPO ---
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/TANYA-SINGH-VNS-UP/NO1")
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")
GIT_TOKEN = getenv("GIT_TOKEN", None)
GITHUB_REPO = getenv("GITHUB_REPO", "https://github.com/TANYA-SINGH-VNS-UP/NO1")

# --- SUPPORT LINKS ---
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/heroku_club")
SUPPORT_GROUP = getenv("SUPPORT_GROUP", "https://t.me/NOBITA_SUPPORT")

# --- ASSISTANT SETTINGS ---
AUTO_LEAVING_ASSISTANT = getenv("AUTO_LEAVING_ASSISTANT", True)
AUTO_LEAVE_ASSISTANT_TIME = int(getenv("ASSISTANT_LEAVE_TIME", 1800))
PRIVATE_BOT_MODE = getenv("PRIVATE_BOT_MODE", False)

# --- DOWNLOAD SLEEP TIME ---
YOUTUBE_DOWNLOAD_EDIT_SLEEP = int(getenv("YOUTUBE_EDIT_SLEEP", 3))
TELEGRAM_DOWNLOAD_EDIT_SLEEP = int(getenv("TELEGRAM_EDIT_SLEEP", 5))

# --- SPOTIFY SETTINGS ---
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "a29b0b331adf4c428ce3a73a9b20a306")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", "e463dede19b04610ad27dc43eb19b56e")

# --- FILE SIZE LIMITS ---
VIDEO_STREAM_LIMIT = int(getenv("VIDEO_STREAM_LIMIT", 999))
SERVER_PLAYLIST_LIMIT = int(getenv("SERVER_PLAYLIST_LIMIT", 500))
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", 500))
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", 104857600)) 
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", 2145386496))

# --- COMMANDS AUTO-SETUP ---
SET_CMDS = getenv("SET_CMDS", False)

# --- STRING SESSIONS ---
STRING1 = getenv("STRING_SESSION", None)
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)

# --- INTERNAL VARIABLES (DO NOT TOUCH) ---
BANNED_USERS = filters.user()
YTDOWNLOADER = 1
LOG = 2
LOG_FILE_NAME = "musiclogs.txt"
TEMP_DB_FOLDER = "tempdb"
adminlist = {}
lyrical = {}
chatstats = {}
votemode = {}
confirmer = {}
userstats = {}
clean = {}
autoclean = []

# --- IMAGE URLS (Yahan aapki saari images hain) ---
# Default Link: https://files.catbox.moe/uohequ.jpg

START_IMG_URL = getenv("START_IMG_URL", "https://files.catbox.moe/uohequ.jpg")
PING_IMG_URL = getenv("PING_IMG_URL", "https://files.catbox.moe/uohequ.jpg")
PLAYLIST_IMG_URL = getenv("PLAYLIST_IMG_URL", "https://files.catbox.moe/uohequ.jpg")
GLOBAL_IMG_URL = getenv("GLOBAL_IMG_URL", "https://files.catbox.moe/uohequ.jpg")
STATS_IMG_URL = getenv("STATS_IMG_URL", "https://files.catbox.moe/uohequ.jpg")
TELEGRAM_AUDIO_URL = getenv("TELEGRAM_AUDIO_URL", "https://files.catbox.moe/uohequ.jpg")
TELEGRAM_VIDEO_URL = getenv("TELEGRAM_VIDEO_URL", "https://files.catbox.moe/uohequ.jpg")
STREAM_IMG_URL = getenv("STREAM_IMG_URL", "https://files.catbox.moe/uohequ.jpg")
SOUNCLOUD_IMG_URL = getenv("SOUNCLOUD_IMG_URL", "https://files.catbox.moe/uohequ.jpg")
YOUTUBE_IMG_URL = getenv("YOUTUBE_IMG_URL", "https://files.catbox.moe/uohequ.jpg")
SPOTIFY_ARTIST_IMG_URL = getenv("SPOTIFY_ARTIST_IMG_URL", "https://files.catbox.moe/uohequ.jpg")
SPOTIFY_ALBUM_IMG_URL = getenv("SPOTIFY_ALBUM_IMG_URL", "https://files.catbox.moe/uohequ.jpg")
SPOTIFY_PLAYLIST_IMG_URL = getenv("SPOTIFY_PLAYLIST_IMG_URL", "https://files.catbox.moe/uohequ.jpg")

# --- HELPER FUNCTIONS ---
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))

DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))
SONG_DOWNLOAD_DURATION_LIMIT = int(time_to_seconds(f"{SONG_DOWNLOAD_DURATION}:00"))

# --- URL VALIDATION LOGIC ---
# Yeh check karega ki aapne links sahi daale hain ya nahi
def check_url(name, url):
    if url and url != "https://files.catbox.moe/uohequ.jpg":
        if not re.match("(?:http|https)://", url):
            print(f"[ERROR] - Aapka {name} link galat hai! Please check karein.")

# Saare Links ko bari-bari check karna
check_url("SUPPORT_CHANNEL", SUPPORT_CHANNEL)
check_url("SUPPORT_GROUP", SUPPORT_GROUP)
check_url("UPSTREAM_REPO", UPSTREAM_REPO)
check_url("GITHUB_REPO", GITHUB_REPO)
check_url("PING_IMG_URL", PING_IMG_URL)
check_url("PLAYLIST_IMG_URL", PLAYLIST_IMG_URL)
check_url("GLOBAL_IMG_URL", GLOBAL_IMG_URL)
check_url("STATS_IMG_URL", STATS_IMG_URL)
check_url("TELEGRAM_AUDIO_URL", TELEGRAM_AUDIO_URL)
check_url("STREAM_IMG_URL", STREAM_IMG_URL)
check_url("SOUNCLOUD_IMG_URL", SOUNCLOUD_IMG_URL)
check_url("YOUTUBE_IMG_URL", YOUTUBE_IMG_URL)
check_url("TELEGRAM_VIDEO_URL", TELEGRAM_VIDEO_URL)