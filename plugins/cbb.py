#(©)Codexbotz

from pyrogram import __version__
from bot import Bot
from config import OWNER_ID
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery


@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    chat_id = query.message.chat.id

    if data == "about":
        await query.message.edit_text(
            text=f"<b>○ Creator : <a href='https://t.me/talktomembbs_bot'>This Person</a>\n○ Language : <code>Python3</code>\n○ Library : <a href='https://docs.pyrogram.org/'>Pyrogram asyncio {__version__}</a></b>",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("🔒 Close", callback_data="close")]
                ]
            )
        )
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass
    elif data.startswith("add_button:"):
        # Extract the button label from the callback data
        new_button_label = data.split(":")[1]

        # Add the new button to the existing inline keyboard
        inline_keyboard = query.message.reply_markup.inline_keyboard
        inline_keyboard.insert(-1, [InlineKeyboardButton(new_button_label, callback_data=f"button:{new_button_label}")])

        # Edit the message to reflect the updated inline keyboard
        await query.message.edit_reply_markup(InlineKeyboardMarkup(inline_keyboard))

# ... (other code)

@Bot.on_message(filter.command("new_button"))
async def new_button_command(bot: Bot, message: Message):
    # Extract the new button label from the command
    new_button_label = message.text.split(" ", 1)[1]

    # Send a message with the new button and a "Close" button
    await message.reply(
        text=f"New button added: {new_button_label}",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(new_button_label, callback_data=f"button:{new_button_label}")],
                [InlineKeyboardButton("🔒 Close", callback_data="close")]
            ]
        )
    )

