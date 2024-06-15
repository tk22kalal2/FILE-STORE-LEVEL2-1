#(©)Codexbotz

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot
from config import ADMINS, CUSTOM_CAPTION
from helper_func import encode, get_message_id
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('batch'))
async def batch(client: Client, message: Message):
    while True:
        try:
            # Prompt the user to provide the first message from the DB Channel
            first_message = await client.ask(
                text="Forward the First Message from DB Channel (with Quotes)..\n\nor Send the DB Channel Post Link",
                chat_id=message.from_user.id,
                filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
                timeout=60
            )
        except:
            return  # Return if there's an exception (e.g., timeout)

        # Get the message ID from the provided message or link
        f_msg_id = await get_message_id(client, first_message)

        if f_msg_id:
            break
        else:
            # Inform the user of an error if the message/link is not from the DB Channel
            await first_message.reply("❌ Error\n\nthis Forwarded Post is not from my DB Channel or this Link is taken from DB Channel", quote=True)
            continue

    while True:
        try:
            # Prompt the user to provide the last message from the DB Channel
            second_message = await client.ask(
                text="Forward the Last Message from DB Channel (with Quotes)..\nor Send the DB Channel Post link",
                chat_id=message.from_user.id,
                filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
                timeout=60
            )
        except:
            return  # Return if there's an exception (e.g., timeout)

        # Get the message ID from the provided message or link
        s_msg_id = await get_message_id(client, second_message)

        if s_msg_id:
            break
        else:
            # Inform the user of an error if the message/link is not from the DB Channel
            await second_message.reply("❌ Error\n\nthis Forwarded Post is not from my DB Channel or this Link is taken from DB Channel", quote=True)
            continue

    # Generate a list of links for each message between the first and second message
    # Generate a list of links for each message between the first and second message
    message_links = []
    for msg_id in range(min(f_msg_id, s_msg_id), max(f_msg_id, s_msg_id) + 1):
        try:
            string = f"get-{msg_id * abs(client.db_channel.id)}"
            base64_string = await encode(string)
            link = f"https://t.me/{client.username}?start={base64_string}"
            message_links.append((link, msg_id))  # Append a tuple with link and msg_id
        except Exception as e:
            await message.reply(f"Error generating link for message {msg_id}: {e}")
    
    # Send the generated links to the user
    for link, msg_id in message_links:
        try:
            # Fetch the message object for the current msg_id
            current_message = await client.get_messages(client.db_channel.id, msg_id)
    
            # Determine the caption for this message
            if bool(CUSTOM_CAPTION) and current_message.document:
                caption = CUSTOM_CAPTION.format(
                    previouscaption="" if not current_message.caption else current_message.caption.html,
                    filename=current_message.document.file_name
                )
            else:
                caption = "" if not current_message.caption else current_message.caption.html
    
            
            # Send the caption followed by the link
            try:
                await client.send_message(chat_id=message.from_user.id, text=f"{caption}\n{link}")
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await client.send_message(chat_id=message.from_user.id, text=f"{caption}\n{link}")

        except Exception as e:
            await message.reply(f"Error processing message {msg_id}: {e}")

    # Inform the user that batch processing is completed
    await message.reply("Batch processing completed.")
    
    
@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('genlink'))
async def link_generator(client: Client, message: Message):
    while True:
        try:
            channel_message = await client.ask(text = "Forward Message from the DB Channel (with Quotes)..\nor Send the DB Channel Post link", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        msg_id = await get_message_id(client, channel_message)
        if msg_id:
            break
        else:
            await channel_message.reply("❌ Error\n\nthis Forwarded Post is not from my DB Channel or this Link is not taken from DB Channel", quote = True)
            continue

    base64_string = await encode(f"get-{msg_id * abs(client.db_channel.id)}")
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    await channel_message.reply_text(f"<b>Here is your link</b>\n\n{link}", quote=True, reply_markup=reply_markup)
