import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait

from bot import Bot
from config import ADMINS, CHANNEL_ID, DISABLE_CHANNEL_BUTTON, USER_REPLY_TEXT
from helper_func import encode

@Bot.on_message(filters.private & filters.user(ADMINS) & 
                ~filters.command(['start', 'users', 'broadcast', 'batch', 'genlink', 
                                  'stats', 'auth_secret', 'deauth_secret', 'auth', 
                                  'sbatch', 'exit', 'add_admin', 'del_admin', 
                                  'admins', 'add_prem', 'ping', 'restart', 'ch2l', 'cancel']))
async def channel_post(client: Client, message: Message):
    # Ensure client.db_channel is initialized
    if not hasattr(client, 'db_channel') or not hasattr(client.db_channel, 'id'):
        await message.reply_text("Channel is not set up correctly. Please check your configuration.")
        return
    
    reply_text = await message.reply_text("Please Wait...! 🫷", quote=True)

    try:
        # Attempt to copy the message to the channel
        post_message = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
        # Optionally notify the user of success
        await reply_text.edit_text("Message successfully posted to the channel!")
    except FloodWait as e:
        # Handle Telegram's flood limit
        await asyncio.sleep(e.x)  # Use e.x to get the wait time
        post_message = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
        await reply_text.edit_text("Message successfully posted to the channel after waiting!")
    except Exception as e:
        print(e)  # Consider using logging instead
        await reply_text.edit_text("Something went wrong!")
        return 

    # Encode the message ID and generate the link
converted_id = post_message.id * abs(client.db_channel.id)
string = f"get-{converted_id}"

try:
    base64_string = await encode(string)
except Exception as e:
    # Consider using logging instead of print
    print(f"Encoding error: {e}")  # Log the error for debugging
    await reply_text.edit_text("Error during encoding!")
    return

link = f"https://t.me/{client.username}?start={base64_string}"

# Inform the user about the generated link
await reply_text.edit_text(f"Message successfully posted to the channel!\nHere is your link: {link}")

    # Create inline keyboard for sharing the URL
reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])

await reply_text.edit(f"<b>Here is your link:</b>\n{link}", reply_markup=reply_markup, disable_web_page_preview=True)

if not DISABLE_CHANNEL_BUTTON:
    try:
        await post_message.edit_reply_markup(reply_markup)
    except FloodWait as e:
        await asyncio.sleep(e.x)  # Use e.x to get the wait time
        try:
            await post_message.edit_reply_markup(reply_markup)
        except Exception as inner_e:
            print(f"Error editing post message markup after flood wait: {inner_e}")  # Consider using logging
    except Exception as e:
        print(f"Error editing post message markup: {e}")  # Consider using logging
      
@Bot.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL_ID))
async def new_post(client: Client, message: Message):
    if DISABLE_CHANNEL_BUTTON:
        return

    # Ensure client.db_channel is initialized
    if not hasattr(client, 'db_channel') or not hasattr(client.db_channel, 'id'):
        print("Channel is not set up correctly. Skipping new post handling.")
        return

    # Encode the message ID and generate the link
    converted_id = message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    
    try:
        base64_string = await encode(string)
    except Exception as e:
        print(f"Encoding error: {e}")  # Use logging instead of print in production
        return
    
    link = f"https://t.me/{client.username}?start={base64_string}"

    # Create inline keyboard for sharing the URL
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])

    # Attempt to edit the message reply markup
    try:
        await message.edit_reply_markup(reply_markup)
    except FloodWait as e:
        await asyncio.sleep(e.x)  # Use e.x for better clarity
        try:
            await message.edit_reply_markup(reply_markup)
        except Exception as inner_e:
            print(f"Error editing reply markup after flood wait: {inner_e}")  # Use logging
    except Exception as e:
        print(f"Error editing reply markup: {e}")  # Use logging
