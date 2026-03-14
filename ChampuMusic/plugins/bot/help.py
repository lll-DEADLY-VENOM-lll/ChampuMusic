import re
from math import ceil
from typing import Union

from pyrogram import Client, filters, types
# यहाँ CallbackQuery को जोड़ दिया गया है
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery

import config
from config import BANNED_USERS, START_IMG_URL
from strings import get_command, get_string, helpers # helpers को यहाँ इम्पोर्ट किया
from ChampuMusic import HELPABLE, app
from ChampuMusic.utils.database import get_lang, is_commanddelete_on
from ChampuMusic.utils.decorators.language import LanguageStart, languageCB
from ChampuMusic.utils.inline.help import private_help_panel

### Command
HELP_COMMAND = get_command("HELP_COMMAND")

COLUMN_SIZE = 4
NUM_COLUMNS = 3


class EqInlineKeyboardButton(InlineKeyboardButton):
    def __eq__(self, other):
        return self.text == other.text

    def __lt__(self, other):
        return self.text < other.text

    def __gt__(self, other):
        return self.text > other.text


def paginate_modules(page_n, module_dict, prefix, chat=None, close: bool = False):
    if not chat:
        modules = sorted(
            [
                EqInlineKeyboardButton(
                    x.__MODULE__,
                    callback_data="{}_module({},{})".format(
                        prefix, x.__MODULE__.lower(), page_n
                    ),
                )
                for x in module_dict.values()
            ]
        )
    else:
        modules = sorted(
            [
                EqInlineKeyboardButton(
                    x.__MODULE__,
                    callback_data="{}_module({},{},{})".format(
                        prefix, chat, x.__MODULE__.lower(), page_n
                    ),
                )
                for x in module_dict.values()
            ]
        )

    pairs = [modules[i : i + NUM_COLUMNS] for i in range(0, len(modules), NUM_COLUMNS)]

    max_num_pages = ceil(len(pairs) / COLUMN_SIZE) if len(pairs) > 0 else 1
    modulo_page = page_n % max_num_pages

    if len(pairs) > COLUMN_SIZE:
        pairs = pairs[modulo_page * COLUMN_SIZE : COLUMN_SIZE * (modulo_page + 1)] + [
            (
                EqInlineKeyboardButton(
                    "❮",
                    callback_data="{}_prev({})".format(
                        prefix,
                        modulo_page - 1 if modulo_page > 0 else max_num_pages - 1,
                    ),
                ),
                EqInlineKeyboardButton(
                    "ᴄʟᴏsᴇ" if close else "Bᴀᴄᴋ",
                    callback_data="close" if close else "feature",
                ),
                EqInlineKeyboardButton(
                    "❯",
                    callback_data="{}_next({})".format(prefix, modulo_page + 1),
                ),
            )
        ]
    else:
        pairs.append(
            [
                EqInlineKeyboardButton(
                    "ᴄʟᴏsᴇ" if close else "Bᴀᴄᴋ",
                    callback_data="close" if close else "feature",
                ),
            ]
        )

    return pairs


@app.on_message(filters.command(HELP_COMMAND) & filters.private & ~BANNED_USERS)
@app.on_callback_query(filters.regex("settings_back_helper") & ~BANNED_USERS)
async def helper_private(
    client: app, update: Union[Message, CallbackQuery]
):
    is_callback = isinstance(update, CallbackQuery)
    if is_callback:
        try:
            await update.answer()
        except:
            pass

        chat_id = update.message.chat.id
        language = await get_lang(chat_id)
        _ = get_string(language)
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))

        await update.edit_message_text(_["help_1"], reply_markup=keyboard)
    else:
        chat_id = update.chat.id
        if await is_commanddelete_on(update.chat.id):
            try:
                await update.delete()
            except:
                pass
        language = await get_lang(chat_id)
        _ = get_string(language)
        keyboard = InlineKeyboardMarkup(
            paginate_modules(0, HELPABLE, "help", close=True)
        )
        try:
            if update.chat.photo:
                userss_photo = await app.download_media(
                    update.chat.photo.big_file_id,
                )
            else:
                userss_photo = "assets/nodp.jpg"

            chat_photo = userss_photo if userss_photo else START_IMG_URL
        except AttributeError:
            chat_photo = "assets/nodp.jpg"

        await update.reply_photo(
            photo=chat_photo,
            caption=_["help_1"].format(config.SUPPORT_GROUP),
            reply_markup=keyboard,
        )


@app.on_message(filters.command(HELP_COMMAND) & filters.group & ~BANNED_USERS)
@LanguageStart
async def help_com_group(client, message: Message, _):
    try:
        if message.chat.photo:
            group_photo = await app.download_media(
                message.chat.photo.big_file_id,
            )
        else:
            group_photo = "assets/nodp.png"

        chat_photo = group_photo if group_photo else "assets/nodp.png"
    except AttributeError:
        chat_photo = "assets/nodp.png"

    keyboard = private_help_panel(_)
    await message.reply_photo(
        photo=chat_photo,
        caption=_["help_2"],
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def help_parser(name, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    return keyboard


@app.on_callback_query(filters.regex(r"help_(.*?)"))
async def help_button(client, query):
    home_match = re.match(r"help_home\((.+?)\)", query.data)
    mod_match = re.match(r"help_module\((.+?),(.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back\((\d+)\)", query.data)
    create_match = re.match(r"help_create", query.data)
    language = await get_lang(query.message.chat.id)
    _ = get_string(language)
    top_text = _["help_1"]

    if mod_match:
        module = mod_match.group(1)
        prev_page_num = int(mod_match.group(2))
        text = (
            f"<b><u>Hᴇʀᴇ Is Tʜᴇ Hᴇʟᴘ Fᴏʀ {HELPABLE[module].__MODULE__}:</u></b>\n"
            + HELPABLE[module].__HELP__
        )

        key = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="↪ ʙᴀᴄᴋ", callback_data=f"help_back({prev_page_num})"
                    ),
                    InlineKeyboardButton(text="🔄 ᴄʟᴏsᴇ", callback_data="close"),
                ],
            ]
        )

        await query.message.edit(
            text=text,
            reply_markup=key,
            disable_web_page_preview=True,
        )

    elif prev_match:
        curr_page = int(prev_match.group(1))
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(curr_page, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif next_match:
        next_page = int(next_match.group(1))
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(next_page, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif back_match:
        prev_page_num = int(back_match.group(1))
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(prev_page_num, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif create_match:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))

        await query.message.edit(
            text=top_text,
            reply_markup=keyboard,
            disable_web_page_preview=True,
        )

    await client.answer_callback_query(query.id)


@app.on_callback_query(filters.regex("music_callback") & ~BANNED_USERS)
@languageCB
async def music_helper_cb(client, callback_query: CallbackQuery, _):
    callback_data = callback_query.data.strip()
    cb = callback_data.split(None, 1)[1]
    from ChampuMusic.utils.inline.help import back_to_music
    keyboard = back_to_music(_)
    
    help_texts = {
        "hb1": helpers.HELP_1, "hb2": helpers.HELP_2, "hb3": helpers.HELP_3,
        "hb4": helpers.HELP_4, "hb5": helpers.HELP_5, "hb6": helpers.HELP_6,
        "hb7": helpers.HELP_7, "hb8": helpers.HELP_8, "hb9": helpers.HELP_9,
        "hb10": helpers.HELP_10, "hb11": helpers.HELP_11, "hb12": helpers.HELP_12,
        "hb13": helpers.HELP_13, "hb14": helpers.HELP_14, "hb15": helpers.HELP_15,
    }
    
    if cb in help_texts:
        await callback_query.edit_message_text(help_texts[cb], reply_markup=keyboard)


@app.on_callback_query(filters.regex("management_callback") & ~BANNED_USERS)
@languageCB
async def management_callback_cb(client, callback_query: CallbackQuery, _):
    callback_data = callback_query.data.strip()
    cb = callback_data.split(None, 1)[1]
    from ChampuMusic.utils.inline.help import back_to_management
    keyboard = back_to_management(_)
    
    if cb == "extra":
        await callback_query.edit_message_text(helpers.EXTRA_1, reply_markup=keyboard)
    else:
        mhelp_texts = {
            "hb1": helpers.MHELP_1, "hb2": helpers.MHELP_2, "hb3": helpers.MHELP_3,
            "hb4": helpers.MHELP_4, "hb5": helpers.MHELP_5, "hb6": helpers.MHELP_6,
            "hb7": helpers.MHELP_7, "hb8": helpers.MHELP_8, "hb9": helpers.MHELP_9,
            "hb10": helpers.MHELP_10, "hb11": helpers.MHELP_11, "hb12": helpers.MHELP_12,
        }
        if cb in mhelp_texts:
            await callback_query.edit_message_text(mhelp_texts[cb], reply_markup=keyboard)


@app.on_callback_query(filters.regex("tools_callback") & ~BANNED_USERS)
@languageCB
async def tools_callback_cb(client, callback_query: CallbackQuery, _):
    callback_data = callback_query.data.strip()
    cb = callback_data.split(None, 1)[1]
    from ChampuMusic.utils.inline.help import back_to_tools
    keyboard = back_to_tools(_)
    
    if cb == "ai":
        await callback_query.edit_message_text(helpers.AI_1, reply_markup=keyboard)
    else:
        thelp_texts = {
            "hb1": helpers.THELP_1, "hb2": helpers.THELP_2, "hb3": helpers.THELP_3,
            "hb4": helpers.THELP_4, "hb5": helpers.THELP_5, "hb6": helpers.THELP_6,
            "hb7": helpers.THELP_7, "hb8": helpers.THELP_8, "hb9": helpers.THELP_9,
            "hb10": helpers.THELP_10, "hb11": helpers.THELP_11, "hb12": helpers.THELP_12,
        }
        if cb in thelp_texts:
            await callback_query.edit_message_text(thelp_texts[cb], reply_markup=keyboard)


@app.on_callback_query(filters.regex("developer"))
async def about_callback(client: Client, callback_query: CallbackQuery):
    owner_id = config.OWNER_ID[0]
    buttons = [
        [
            InlineKeyboardButton(text="[ ᴏᴡɴᴇʀ ]", url=f"tg://openmessage?user_id={owner_id}"),
            InlineKeyboardButton(
                text="[ sᴜᴅᴏᴇʀs ]", url=f"https://t.me/{app.username}?start=sudo"
            ),
        ],
        [
            InlineKeyboardButton(text="[ ɪɴsᴛᴀ ]", url=f"https://www.instagram.com/nobita_bot_maker?igsh=MXgxbHR2N3Nlb3hhZQ%3D%3D&utm_source=qr"),
            InlineKeyboardButton(text="[ ʏᴏᴜᴛᴜʙᴇ ]", url=f"https://www.youtube.com/@NOBITA_HACKING_KING"),
        ],
        [
            InlineKeyboardButton(text="● ʙᴀᴄᴋ ●", callback_data="settings_back_helper")
        ],
    ]
    await callback_query.message.edit_text(
        "✦ **ᴛʜɪs ʙᴏᴛ ɪs ᴍᴀᴅᴇ ʙʏ ᴀ sᴋɪʟʟᴇᴅ ᴅᴇᴠᴇʟᴏᴘᴇʀ ᴛᴏ ᴍᴀᴋᴇ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴇᴀsʏ ᴛᴏ ᴍᴀɴᴀɢᴇ ᴀɴᴅ ᴍᴏʀᴇ ғᴜɴ.**\n\n✦ **ᴡɪᴛʜ ᴊᴜsᴛ ᴀ ғᴇᴡ ᴄʟɪᴄᴋs, ʏᴏᴜ ᴄᴀɴ ᴄᴏɴᴛʀᴏʟ ᴇᴠᴇʀʏᴛʜɪɴɢ—ʟɪᴋᴇ sᴇᴛᴛɪɴɢ ᴜᴘ ᴏᴡɴᴇʀ sᴇᴛᴛɪɴɢs, ᴄʜᴇᴄᴋɪɴɢ sᴜᴅᴏᴇʀs, ᴀɴᴅ ᴇᴠᴇɴ ᴇxᴘʟᴏʀɪɴɢ ɪɴsᴛᴀɢʀᴀᴍ ᴀɴᴅ ʏᴏᴜᴛᴜʙᴇ.**\n\n✦ **ᴛʜᴇ ʙᴏᴛ ɪs ᴅᴇsɪɢɴᴇᴅ ᴛᴏ ʜᴇʟᴘ ʏᴏᴜ ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ɢʀᴏᴜᴘ sᴍᴏᴏᴛʜʟʏ ᴀɴᴅ ᴇɴᴊᴏʏ ᴍᴜsɪᴄ ᴛᴏᴏ. ᴊᴜsᴛ ᴜsᴇ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ ᴀɴᴅ sᴇᴇ ʜᴏᴡ ᴇᴀsʏ ɪᴛ ɪs!**",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@app.on_callback_query(filters.regex("feature"))
async def feature_callback(client: Client, callback_query: CallbackQuery):
    keyboard = [
        [
            InlineKeyboardButton(
                text="● ᴛᴀᴘ ʜᴇʀᴇ ᴛᴏ ᴀᴅᴅ ᴍᴇ ●",
                url=f"https://t.me/{app.username}?startgroup=true",
            ),
        ],
        [
            InlineKeyboardButton(text="˹ᴍᴜsɪᴄ˼", callback_data="music"),
            InlineKeyboardButton(text="˹ᴍᴧɴᴧɢᴍᴇɴᴛ˼", callback_data="management"),
        ],
        [
            InlineKeyboardButton(text="˹ᴛᴏᴏʟs˼", callback_data="tools"),
            InlineKeyboardButton(text="˹ᴧʟʟ˼", callback_data="settings_back_helper"),
        ],
        [InlineKeyboardButton(text="✯ ʜᴏᴍᴇ ✯", callback_data="go_to_start")],
    ]
    k = f"**✨ ᴍᴇᴇᴛ {app.mention} !\n\n━━━━━━━━━━━━━━━\n🎶 ɪ’ᴍ ᴀ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ | ᴍᴜsɪᴄ ʙᴏᴛ\n\n🚀 ɴᴏ ʟᴀɢ, ɴᴏ ᴀᴅs, ɴᴏ ᴘʀᴏᴍᴏᴛɪᴏɴs\n🎧 𝟸𝟺/𝟽 ᴜᴘᴛɪᴍᴇ ᴡɪᴛʜ ᴛʜᴇ ʙᴇsᴛ sᴏᴜɴᴅ ǫᴜᴀʟɪᴛʏ\n💡 ᴛᴀᴘ ᴛʜᴇ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ᴛᴏ ᴇxᴘʟᴏʀᴇ ᴍʏ ᴍᴏᴅᴜʟᴇs ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅs!\n\n━━━━━━━━━━━━━━━\n❖ ᴘᴏᴡᴇʀᴇᴅ ʙʏ ➥ <a href=https://t.me/VNI0X>野买</a></b></blockquote>**"
    await callback_query.message.edit_text(
        text=k, reply_markup=InlineKeyboardMarkup(keyboard)
    )


@app.on_callback_query(filters.regex("music"))
async def music_callback(client: Client, callback_query: CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="Aᴅᴍɪɴ", callback_data="music_callback hb1"),
                InlineKeyboardButton(text="Aᴜᴛʜ", callback_data="music_callback hb2"),
                InlineKeyboardButton(text="Bʀᴏᴀᴅᴄᴀsᴛ", callback_data="music_callback hb3"),
            ],
            [
                InlineKeyboardButton(text="Bʟ-Cʜᴀᴛ", callback_data="music_callback hb4"),
                InlineKeyboardButton(text="Bʟ-Usᴇʀ", callback_data="music_callback hb5"),
                InlineKeyboardButton(text="C-Pʟᴀʏ", callback_data="music_callback hb6"),
            ],
            [
                InlineKeyboardButton(text="G-Bᴀɴ", callback_data="music_callback hb7"),
                InlineKeyboardButton(text="Lᴏᴏᴘ", callback_data="music_callback hb8"),
                InlineKeyboardButton(text="Mᴀɪɴᴛᴇɴᴀɴᴄᴇ", callback_data="music_callback hb9"),
            ],
            [
                InlineKeyboardButton(text="Pɪɴɢ", callback_data="music_callback hb10"),
                InlineKeyboardButton(text="Pʟᴀʏ", callback_data="music_callback hb11"),
                InlineKeyboardButton(text="Sʜᴜғғʟᴇ", callback_data="music_callback hb12"),
            ],
            [
                InlineKeyboardButton(text="Sᴇᴇᴋ", callback_data="music_callback hb13"),
                InlineKeyboardButton(text="Sᴏɴɢ", callback_data="music_callback hb14"),
                InlineKeyboardButton(text="Sᴘᴇᴇᴅ", callback_data="music_callback hb15"),
            ],
            [InlineKeyboardButton(text="✯ ʙᴀᴄᴋ ✯", callback_data="feature")],
        ]
    )

    await callback_query.message.edit(
        f"``**Cʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ ғᴏʀ ᴍᴏʀᴇ ɪɴғᴏʀᴍᴀᴛɪᴏɴ.  Iғ ʏᴏᴜ'ʀᴇ ғᴀᴄɪɴɢ ᴀɴʏ ᴘʀᴏʙʟᴇᴍ ʏᴏᴜ ᴄᴀɴ ᴀsᴋ ɪɴ [sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ.](t.me/Heroku_Club)**\n\n**Aʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ: /**``",
        reply_markup=keyboard,
    )


@app.on_callback_query(filters.regex("management"))
async def management_callback(client: Client, callback_query: CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text="єxᴛʀᴧ", callback_data="management_callback extra")],
            [
                InlineKeyboardButton(text="ʙᴧη", callback_data="management_callback hb1"),
                InlineKeyboardButton(text="ᴋɪᴄᴋs", callback_data="management_callback hb2"),
                InlineKeyboardButton(text="ϻυᴛє", callback_data="management_callback hb3"),
            ],
            [
                InlineKeyboardButton(text="ᴘɪη", callback_data="management_callback hb4"),
                InlineKeyboardButton(text="sᴛᴧғғ", callback_data="management_callback hb5"),
                InlineKeyboardButton(text="sєᴛ υᴘ", callback_data="management_callback hb6"),
            ],
            [
                InlineKeyboardButton(text="zσϻʙɪє", callback_data="management_callback hb7"),
                InlineKeyboardButton(text="ɢᴧϻє", callback_data="management_callback hb8"),
                InlineKeyboardButton(text="✯ ʙᴀᴄᴋ ✯", callback_data="feature"),
            ],
        ]
    )

    await callback_query.message.edit(
        f"``**Cʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ ғᴏʀ ᴍᴏʀᴇ ɪɴғᴏʀᴍᴀᴛɪᴏɴ.  Iғ ʏᴏᴜ'ʀᴇ ғᴀᴄɪɴɢ ᴀɴʏ ᴘʀᴏʙʟᴇᴍ ʏᴏᴜ ᴄᴀɴ ᴀsᴋ ɪɴ [sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ.](t.me/Heroku_Club)**\n\n**Aʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ: /**``",
        reply_markup=keyboard,
    )