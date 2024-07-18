# (c) NobiDeveloper
from pyrogram import Client
import pyromod.listen
from config import *
from os import getcwd

StreamBot = Client(
    name='Web Streamer',
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    sleep_threshold=Var.SLEEP_THRESHOLD,
    workers=Var.WORKERS
)

multi_clients = {}
work_loads = {}
