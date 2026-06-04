import os
from telethon import TelegramClient, events


API_ID = int(os.environ.get("API_ID", 1234567))  
API_HASH = os.environ.get("API_HASH", "placeholder_hash")

SOURCE_CHANNELS = [
    'BhramsBots1'
] 

CONVERTOR_BOT = 'Sixtystore_bot' 

client = TelegramClient('instant_middleman_session', API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def instant_forward_handler(event):
    if not event.message:
        return

    print("⚡ Naya post aaya! Convertor bot ko forward kar raha hoon...")
    
    try:
        await client.forward_messages(CONVERTOR_BOT, event.message)
        print("✅ Post successfully forward ho gaya!\n")
    except Exception as e:
        print(f"❌ Forward karne mein error: {e}\n")

print("🚀 Bot active ho gaya hai... Naye posts ka wait kar raha hai.")
client.start()
client.run_until_disconnected()