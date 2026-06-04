import os
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
from telethon import TelegramClient, events

API_ID = int(os.environ.get("API_ID", 1234567))  
API_HASH = os.environ.get("API_HASH", "placeholder_hash")


SOURCE_CHANNELS = [
    'BhramsBots1'
] 

CONVERTOR_BOT = 'ekconverter16bot' 

client = TelegramClient('forwarder_session', API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def instant_forward_handler(event):
    if not event.message:
        return

    print("⚡️ Naya post aaya! Convertor bot ko forward kar raha hoon...")
    
    try:
        # Message ko turant convertor bot ko bhej dega
        await client.forward_messages(CONVERTOR_BOT, event.message)
        print("✅ Post successfully forward ho gaya!\n")
    except Exception as e:
        print(f"❌ Forward karne mein error: {e}\n")

def run_dummy_server():
    # Render ko khush rakhne ke liye ek port bind karna zaroori hai
    port = int(os.environ.get("PORT", 8000))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    print(f"🌍 Dummy web server running on port {port}")
    server.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()


print("🚀 Bot active ho gaya hai... Naye posts ka wait kar raha hai.")
client.start()
client.run_until_disconnected()