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

genai.configure(api_key="AIzaSyBjcQWATZfQ9vwytmlWEuLPrgvntdixuk0")

buttonz = ReplyKeyboardMarkup(
    [
        ["newchat⚡️"],
    ],
    resize_keyboard=True
)

@Bot.on_message(filters.command('stats') & filters.user(ADMINS))
async def stats(bot: Bot, message: Message):
    now = datetime.now()
    delta = now - bot.uptime
    time = get_readable_time(delta.seconds)
    await message.reply(BOT_STATS_TEXT.format(uptime=time))

user_conversations = {}

@Client.on_message((filters.private & filters.text) | (filters.command("newchat") | filters.regex('newchat⚡️')))
async def lazy_answer(client: Client, message: Message):
    if AI:
        user_id = message.from_user.id
        if user_id:
            try:
                # Check if user wants to start a new chat
                if message.text.lower().strip() == "/newchat" or message.text.strip() == 'newchat⚡️':
                    user_conversations.pop(user_id, None)  # Remove user's conversation history
                    response_text = "New chat started. Ask me anything!"
                    await message.reply(response_text)
                    return

                # Get the user's previous messages
                user_messages = user_conversations.get(user_id, [])
                user_messages.append(message.text)

                # Use the user's messages as a prompt
                prompt = "\n".join(user_messages)

                # Set up the model
                generation_config = {
                    "temperature": 0.9,
                    "top_p": 1,
                    "top_k": 1,
                    "max_output_tokens": 2048,
                }

                safety_settings = [
                    {
                        "category": "HARM_CATEGORY_HARASSMENT",
                        "threshold": "BLOCK_ONLY_HIGH"
                    },
                    {
                        "category": "HARM_CATEGORY_HATE_SPEECH",
                        "threshold": "BLOCK_ONLY_HIGH"
                    },
                    {
                        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        "threshold": "BLOCK_ONLY_HIGH"
                    },
                    {
                        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                        "threshold": "BLOCK_ONLY_HIGH"
                    },
                ]

                model = genai.GenerativeModel(model_name="gemini-pro",
                                              generation_config=generation_config,
                                              safety_settings=safety_settings)
                prompt_parts = [prompt]

                response = model.generate_content(prompt_parts)

                footer_credit = "<b>ADMIN ID:</b>-@talktomembbs_bot\n<b>MBBS LECTURES:-</b><a href='https://sites.google.com/view/pavoladdder'>CLICK HERE</a>"

                lazy_response = response.text

                WAIT_MSG = "</b>...........Processing..........</b>"
                msg = await client.send_message(text=WAIT_MSG)
                await msg.edit(
                    AI_LOGS,
                    text=f"<b>Name - {message.from_user.mention}\n{user_id}\n</b>CONVERSATION HISTORY:-\n{prompt}\n</b>ANSWER:-\n{lazy_response}",
                    parse_mode=ParseMode.HTML
                )
                
                # Add parse_mode parameter here when replying to the user
                await message.reply(f"{lazy_response}\n{footer_credit}", parse_mode=ParseMode.HTML, reply_markup=buttonz)

                # Update user conversation history
                user_conversations[user_id] = user_messages
            except Exception as error:
                print(error)
    else:
        return
