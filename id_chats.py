

from pyrogram import Client
API_ID = ""
API_HASH = ""

with Client("my_account", api_id=API_ID, api_hash=API_HASH) as app:
    for dialog in app.get_dialogs():
        chat = dialog.chat
        print(f"Nome: {chat.title or chat.first_name} | ID: {chat.id} | Tipo: {chat.type}")
