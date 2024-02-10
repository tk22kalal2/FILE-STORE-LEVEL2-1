#(©)CodeXBotz




import os
import asyncio
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from bot import Bot
from config import ADMINS, FORCE_MSG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT
from helper_func import subscribed, encode, decode, get_messages
from database.database import add_user, del_user, full_userbase, present_user



SECONDS = int(os.getenv("SECONDS", "10")) #add time im seconds for waitingwaiting before delete

async def fetch_and_add_users():
    try:
        async for member in Client.iter_chat_members(CHANNEL_ID):
            # Add the user ID to the database
            await add_user(member.user.id)
    except Exception as e:
        print(f"Error fetching or adding users: {e}") 
        
@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    await fetch_and_add_users()
    if present_user:
    await message.reply("Users fetched from the channel and added to the database.")
    
        
    
    
#=====================================================================================##

WAIT_MSG = """"<b>Processing ...</b>"""

REPLY_ERROR = """<code>Use this command as a replay to any telegram message with out any spaces.</code>"""

#=====================================================================================##

    
    
@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    buttons = [
        [
            InlineKeyboardButton(
                "Join Channel",
                url = client.invitelink)
        ]
    ]
    try:
        buttons.append(
            [
                InlineKeyboardButton(
                    text = 'Try Again',
                    url = f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ]
        )
    except IndexError:
        pass

    await message.reply(
        text = FORCE_MSG.format(
                first = message.from_user.first_name,
                last = message.from_user.last_name,
                username = None if not message.from_user.username else '@' + message.from_user.username,
                mention = message.from_user.mention,
                id = message.from_user.id
            ),
        reply_markup = InlineKeyboardMarkup(buttons),
        quote = True,
        disable_web_page_preview = True
    )


from config import ADMINS, CHANNEL_ID



# Fetch users from channel and add them to the user database


# Command to trigger fetching and adding users from the channel to the database
@Bot.on_message(filters.command('fetch_and_add_users') & filters.private & filters.user(ADMINS))
async def fetch_and_add_users_command(client, message):
    await fetch_and_add_users()
    await message.reply("Users fetched from the channel and added to the database.")















