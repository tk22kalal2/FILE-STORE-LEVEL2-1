#(©)Codexbotz

from pyrogram import __version__
from bot import Bot
from config import OWNER_ID
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters, __version__
from pyrogram.errors import MessageNotModified

# Define a dictionary to store user states
user_states = {}

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    chat_id = query.message.chat.id
    user_id = query.from_user.id

    if data == "about":
        await query.message.edit_text(
            text=f"<b>○ Creator : <a href='https://t.me/talktomembbs_bot'>This Person</a>\n"
                 f"○ Language : <code>Python3</code>\n"
                 f"○ Library : <a href='https://docs.pyrogram.org/'>Pyrogram asyncio {__version__}</a></b>",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("addbutton", callback_data="addbutton"),
                     InlineKeyboardButton("🔒 Close", callback_data="close")]
                ]
            )
        )
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass
    elif data == "addbutton":
        # Set the user state to 'waiting_for_button_name'
        user_states[user_id] = 'waiting_for_button_name'

        # Prompt the user to enter the name of the new button
        await query.message.edit_text(
            text="Please enter the name of the new button:",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔒 Close", callback_data="close")]])
        )


# Handle user input in a message
@Bot.on_message()
async def handle_message(client: Bot, message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    # Check if the user is in 'waiting_for_button_name' state
    if user_id in user_states and user_states[user_id] == 'waiting_for_button_name':
        # Retrieve the entered button name
        new_button_name = message.text

        # Perform the action with the new button name (e.g., add it to the inline keyboard)
        # Here, I'm just updating the message with the new button name
        try:
            await message.edit_text(
                text=f"Button added: {new_button_name}",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("🔒 Close", callback_data="close")]]
                )
            )
        except MessageNotModified:
            pass

        # Reset the user state
        del user_states[user_id]
