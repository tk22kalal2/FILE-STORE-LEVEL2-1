from bot import Bot
from pyrogram.types import Message
from pyrogram import filters
from config import ADMINS, BOT_STATS_TEXT, USER_REPLY_TEXT, AI, OPENAI_API, AI_LOGS
from datetime import datetime
from helper_func import get_readable_time
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client, filters
import openai
openai.api_key = OPENAI_API

@Bot.on_message(filters.command('stats') & filters.user(ADMINS))
async def stats(bot: Bot, message: Message):
    now = datetime.now()
    delta = now - bot.uptime
    time = get_readable_time(delta.seconds)
    await message.reply(BOT_STATS_TEXT.format(uptime=time))



@Bot.on_message(filters.private & filters.text)
async def lazy_answer(client: Bot, message: Message):
    if AI == True: 
        user_id = message.from_user.id
        if user_id:
            try:
                lazy_users_message = message.text
                user_id = message.from_user.id
                response = openai.Completion.create(
                    model = "text-davinci-003",
                    prompt = lazy_users_message,
                    temperature = 0.5, 
                    max_tokens = 1000,
                    top_p=1,
                    frequency_penalty=0.1,
                    presence_penalty = 0.0,
                )
                lazy_response = response.choices[0].text
                formatted_response = "\n".join(f"{i + 1}. {line}" for i, line in enumerate(lazy_response.split("\n")))
                await client.send_message(AI_LOGS, text=f"</b>Name - {message.from_user.mention} \n{user_id} \n</b>QUESTION:-</b> \n{lazy_users_message}\n</b>ANSWER:-</b> \n{lazy_response}")
                await message.reply(f"{formatted_response}")
            except Exception as error:
                print(error)
    else:
        return
