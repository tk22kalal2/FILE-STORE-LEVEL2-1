from bot import Bot
from pyrogram.types import Message
from pyrogram import filters
from pyrogram.enums import ParseMode
from config import ADMINS, BOT_STATS_TEXT, USER_REPLY_TEXT, AI, OPENAI_API, AI_LOGS
from datetime import datetime
from helper_func import get_readable_time
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from pyrogram import Client, filters
import openai
import requests
import google.generativeai as genai
from database.database import full_userbase

genai.configure(api_key="AIzaSyBjcQWATZfQ9vwytmlWEuLPrgvntdixuk0")

buttonz = ReplyKeyboardMarkup(
    [
        ["newchat⚡️"],
    ],
    resize_keyboard=True
)

inline_button = InlineKeyboardMarkup(
    [[InlineKeyboardButton("🩺 MEDICAL LECTURES", url="https://sites.google.com/view/pavoladdder")]]
)
    
    
@Bot.on_message(filters.command('stats') & filters.user(ADMINS))
async def stats(bot: Bot, message: Message):
    now = datetime.now()
    delta = now - bot.uptime
    time = get_readable_time(delta.seconds)
    await message.reply(BOT_STATS_TEXT.format(uptime=time))

# Dictionary to store user/admin conversations
user_conversations = {}

@Bot.on_message(filters.private & filters.incoming)
async def forward_to_admin(client: Bot, m: Message):
    # Check if the message is from a private chat
    if m.chat.type == "private":
        # Check if user is already in a conversation
        if m.from_user.id in user_conversations:
            admin_id = user_conversations[m.from_user.id]
            await client.send_message(admin_id, f"User ID: {m.from_user.id}\nMessage: {m.text}")

            # Optionally, you can send a confirmation message to the user
            await m.reply_text("Your message has been forwarded to the admin.")
        else:
            await m.reply_text("You are not currently in a conversation with an admin.")

@Bot.on_message(filters.private & filters.outgoing)
async def forward_reply_to_user(client: Bot, m: Message):
    # Check if the reply is from an admin
    if m.from_user.id in ADMINS:
        # Check if the reply is part of a conversation
        if m.reply_to_message:
            user_id = m.reply_to_message.from_user.id

            # Store the admin ID in the user_conversations dictionary
            user_conversations[user_id] = m.from_user.id

            # Forward the admin's reply to the user
            await client.send_message(user_id, f"Admin reply: {m.text}")

            # Optionally, you can send a confirmation message to the admin
            await m.reply_text("Your reply has been sent to the user.")
        else:
            await m.reply_text("You can only reply to user messages within the bot.")
