from bot import Bot
from pyrogram.types import Message
from pyrogram import filters
from config import ADMINS, BOT_STATS_TEXT, USER_REPLY_TEXT, AI, OPENAI_API, AI_LOGS
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

# Assuming you have a global variable to store the conversation state
conversation_state = {}

@Bot.on_message(filters.private & filters.text)
async def lazy_answer(client, message):
    global conversation_state
    
    if AI:
        user_id = message.from_user.id
        if user_id:
            try:
                lazy_users_message = message.text
                
                # Check if this is a new chat or a continuation of the previous one
                if user_id in conversation_state and conversation_state[user_id]['in_progress']:
                    # Continuing the conversation
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
                    await message.reply(f"{lazy_response}")
                else:
                    # Starting a new chat
                    if lazy_users_message in ["hi", "hello"]:
                        response_text = "Hi Doctor! My name is Miss Dopamine."
                        await message.reply_text(response_text)
                    else:
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
                        await lazy_response.forward(chat_id=AI_LOGS)
                        await message.reply(f"{lazy_response}")
                    
                    # Update conversation state
                    conversation_state[user_id] = {'in_progress': True, 'last_message': lazy_users_message}
                    
            except Exception as error:
                print(error)
                await message.reply_text(f'{error}')
        else:
            return
