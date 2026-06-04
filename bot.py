import os
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
from telethon import TelegramClient, events

API_ID = int(os.environ.get("API_ID", 1234567))  
API_HASH = os.environ.get("API_HASH", "placeholder_hash")

SOURCE_CHANNELS = [
    'BhramsBots1',
    'megadealv1',
    'pocket_tv_mod_app'
] 

CONVERTOR_BOT = 'ekconverter16bot' 

OLD_LINK = 'https://t.me/megadealv1'
NEW_LINK = 'https://t.me/sixtystore_loot'


client = TelegramClient('forwarder_session', API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def instant_forward_handler(event):
    if not event.message:
        return

    print("⚡ Naya post aaya! Text check kar raha hoon...")
    
    message_text = event.message.message
    
    if message_text and OLD_LINK in message_text:
        print(f"🎯 Purani link mili! Replace kar raha hoon {NEW_LINK} se...")
        message_text = message_text.replace(OLD_LINK, NEW_LINK)
        event.message.message = message_text  # Updated text ko message object mein wapas set karna

    try:
        await client.forward_messages(CONVERTOR_BOT, event.message)
        print("✅ Post successfully edit aur forward ho gaya!\n")
    except Exception as e:
        print(f"❌ Forward karne mein error: {e}\n")


def run_dummy_server():
    port = int(os.environ.get("PORT", 8000))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    print(f"🌍 Dummy web server running on port {port}")
    server.serve_forever()


threading.Thread(target=run_dummy_server, daemon=True).start()


print("🚀 Bot active ho gaya hai... Naye posts ka wait kar raha hai.")
client.start()
client.run_until_disconnected()