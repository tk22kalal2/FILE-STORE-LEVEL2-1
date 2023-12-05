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

openai.api_key = OPENAI_API

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

def fetch_unsplash_image(query):
    # Use the Unsplash API to fetch an image based on the query    
    try:
        response = requests.get(
            f"https://api.unsplash.com/photos/random?query={query}",
            headers={"Authorization": f"Client-ID {UNSPLASH_API_KEY}"}
        )
        data = response.json()
        image_url = data.get("urls", {}).get("regular")
        return image_url
    except Exception as e:
        print(f"Error fetching Unsplash image: {e}")
        return None
        
# Add your Unsplash API key here
UNSPLASH_API_KEY = "7vqvT8gDlgCu18v-GuT_EPyqxtRYPMVGNBmpBE59jac"

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
                           
                # Handle specific user messages
                lazy_users_message = message.text.lower().strip()
                if lazy_users_message in ["hi", "hello"]:
                    response_text = "Hi Doctor! I am ChatGPT . Ask me anything related to medical study Questions."
                    await message.reply(response_text)
                    return

                if message.text.lower().strip() == "#diagram":
                    # Get the user's previous messages
                    user_messages = user_conversations.get(user_id, [])
                    # Use the user's messages as a prompt
                    prompt = "\n".join(user_messages)
                    # Fetch a relevant image from Unsplash.com based on the user's messages
                    image_url = fetch_unsplash_image(prompt)
    
                    if image_url:
                    # Send the image to the user
                        await client.send_photo(message.chat.id, photo=image_url, caption="Here's a relevant diagram:")
                    else:
                        await message.reply("Sorry, I couldn't find a relevant diagram image.")
                    return


                # Get the user's previous messages
                user_messages = user_conversations.get(user_id, [])
                user_messages.append(message.text)

                # Use the user's messages as a prompt
                prompt = "\n".join(user_messages)

                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=prompt,
                    temperature=0.5,
                    max_tokens=1000,
                    top_p=1,
                    frequency_penalty=0.1,
                    presence_penalty=0.0,
                )
                footer_credit = "<b>ADMIN ID:</b>-@talktomembbs_bot\n<b>MBBS LECTURES:-</b><a href='https://sites.google.com/view/pavoladdder'>CLICK HERE</a>"

                lazy_response = response.choices[0].text

                await client.send_message(AI_LOGS, text=f"<b>Name - {message.from_user.mention}\n{user_id}\n</b>CONVERSATION HISTORY:-\n{prompt}\n</b>ANSWER:-\n{lazy_response}", parse_mode=ParseMode.HTML)

                # Add parse_mode parameter here when replying to the user
                await message.reply(f"{lazy_response}\n{footer_credit}", parse_mode=ParseMode.HTML, reply_markup=buttonz)

                # Update user conversation history
                user_conversations[user_id] = user_messages
            except Exception as error:
                print(error)
    else:
        return

