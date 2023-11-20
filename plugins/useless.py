from bot import Bot
from pyrogram.types import Message
from pyrogram import filters
from config import ADMINS, BOT_STATS_TEXT, USER_REPLY_TEXT, AI, OPENAI_API
from datetime import datetime
from helper_func import get_readable_time

@Bot.on_message(filters.command('stats') & filters.user(ADMINS))
async def stats(bot: Bot, message: Message):
    now = datetime.now()
    delta = now - bot.uptime
    time = get_readable_time(delta.seconds)
    await message.reply(BOT_STATS_TEXT.format(uptime=time))


from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client, filters
import openai
openai.api_key = OPENAI_API

# Import the required library
from googlesearch import search

# ... (previous code)

@Bot.on_message(filters.private & filters.text)
async def lazy_answer(client, message):
    if AI == True:
        user_id = message.from_user.id
        try:
            lazy_users_message = message.text
            prompt = f"Miss Dopamine, a female doctor, says: {lazy_users_message}"
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=lazy_users_message,
                temperature=0.5,
                max_tokens=1000,
                top_p=1,
                frequency_penalty=0.1,
                presence_penalty=0.0,
            )
            lazy_response = response.choices[0].text

            # Perform a Google image search
            image_query = f"{lazy_response} image"
            for url in search(image_query, stop=1):
                # Reply with the generated response and the first image URL from Google search
                await message.reply_photo(url, caption=lazy_response)

        except Exception as error:
            print(error)
            await message.reply_text(f'Error aa gya Lazy Bhaiya 😀\n\n{error}')
    else:
        return

