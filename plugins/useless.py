from bot import Bot
from pyrogram.types import Message
from pyrogram import filters
from config import ADMINS, BOT_STATS_TEXT, USER_REPLY_TEXT
from datetime import datetime
from helper_func import get_readable_time

@Bot.on_message(filters.command('stats') & filters.user(ADMINS))
async def stats(bot: Bot, message: Message):
    now = datetime.now()
    delta = now - bot.uptime
    time = get_readable_time(delta.seconds)
    await message.reply(BOT_STATS_TEXT.format(uptime=time))


import openai
from telegram import Update
from telegram.ext import Filters, MessageHandler, Updater

# Set your OpenAI GPT-3 API key
openai.api_key = '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'

@Bot.on_message(filters.private & filters.incoming)
def handle_messages(update: Update, context):
    # Get the user's message
    user_message = update.message.text

    # Use the user's message as input to ChatGPT
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=user_message,
        max_tokens=50  # Adjust as needed
    )

    # Extract the generated response from ChatGPT
    chatgpt_reply = response.choices[0].text.strip()

    # Send the generated response back to the user
    update.message.reply_text(chatgpt_reply)

# Set up the Telegram Bot
updater = Updater(token='YOUR_TELEGRAM_BOT_TOKEN', use_context=True)
dispatcher = updater.dispatcher

# Register the message handler
message_handler = MessageHandler(Filters.private & Filters.text & Filters.incoming, handle_messages)
dispatcher.add_handler(message_handler)

# Start the bot
updater.start_polling()
updater.idle()
