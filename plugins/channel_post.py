import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from bot import Bot
from config import ADMINS, CHANNEL_ID, DISABLE_CHANNEL_BUTTON, USER_REPLY_TEXT
from helper_func import encode

# Simple in-memory throttle for user requests
user_requests = {}

def throttle_requests(user_id):
    """Throttle user requests."""
    current_time = asyncio.get_event_loop().time()
    if user_id in user_requests:
        last_request_time = user_requests[user_id]
        if current_time - last_request_time < 5:  # 5 seconds throttle
            return False  # Throttle the request
    user_requests[user_id] = current_time
    return True

@Bot.on_message(filters.private & filters.user(ADMINS) & ~filters.command([...]))
async def channel_post(client: Client, message: Message):
    if not throttle_requests(message.from_user.id):
        await message.reply_text("You are sending requests too quickly. Please wait a moment.")
        return
    
    if not hasattr(client, 'db_channel') or not hasattr(client.db_channel, 'id'):
        await message.reply_text("Channel is not set up correctly. Please check your configuration.")
        return
    
    reply_text = await message.reply_text("Please Wait...! 🫷", quote=True)
    try:
        post_message = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        post_message = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
    except Exception as e:
        await reply_text.edit_text("Something went wrong!")
        print(e)
        return

    # Encoding and link generation
    converted_id = post_message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    
    try:
        base64_string = await encode(string)
    except Exception as e:
        await reply_text.edit_text("Error during encoding!")
        print(e)
        return
    
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])

    await reply_text.edit(f"<b>Here is your link:</b>\n{link}", reply_markup=reply_markup, disable_web_page_preview=True)

    if not DISABLE_CHANNEL_BUTTON:
        try:
            await post_message.edit_reply_markup(reply_markup)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await post_message.edit_reply_markup(reply_markup)
        except Exception as e:
            print(e)

@Bot.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL_ID))
async def new_post(client: Client, message: Message):
    if DISABLE_CHANNEL_BUTTON:
        return

    if not hasattr(client, 'db_channel') or not hasattr(client.db_channel, 'id'):
        print("Channel is not set up correctly. Skipping new post handling.")
        return

    # Encoding and link generation
    converted_id = message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    
    try:
        base64_string = await encode(string)
    except Exception as e:
        print(e)
        return
    
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])

    try:
        await message.edit_reply_markup(reply_markup)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        await message.edit_reply_markup(reply_markup)
    except Exception as e:
        print(e)
