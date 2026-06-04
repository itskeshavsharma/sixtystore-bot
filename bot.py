import os
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
from telethon import TelegramClient, events

# ==========================================
# ⚙️ SETTINGS (Keys Render Dashboard se uthayega)
# ==========================================
API_ID = int(os.environ.get("API_ID", 1234567))  
API_HASH = os.environ.get("API_HASH", "placeholder_hash")

# 1. Jin source channels se deals uthani hain
SOURCE_CHANNELS = [
    'BhramsBots1',
    'megadealv1',
    'pocket_tv_mod_app'
] 

# 2. EarnKaro Converter Bot ka username (Bina @ ke)
CONVERTOR_BOT = 'ekconverter16bot' 

# 3. ⚠️ AAPKA APNA CHANNEL: Jahan deals post hoti hain (Bina @ ke username daalein)
MY_TARGET_CHANNEL = 'SixtyStore_loot' 

# 4. 🔥 APNA BRAND LINK: Jo har post ke end mein automatic judega
MY_BRAND_FOOTER = "\n\nJoin for more premium loots ❤️👇\nhttps://t.me/sixtystore_loot"

# ==========================================
# 🤖 BOT INITIALIZATION
# ==========================================
client = TelegramClient('forwarder_session', API_ID, API_HASH)

# ------------------------------------------
# 🔄 STEP 1: AUTO-FORWARDER (Source -> Converter Bot)
# ------------------------------------------
@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def instant_forward_handler(event):
    if not event.message:
        return

    print("📥 Source channel par naya post aaya! Converter bot ko forward kar raha hoon...")
    try:
        # Original message ko jaisa ka taisa converter bot ko bhej do
        await client.forward_messages(CONVERTOR_BOT, event.message)
        print("✅ Converter bot ko safely forward ho gaya!\n")
    except Exception as e:
        print(f"❌ Forward karne mein error: {e}\n")

# ------------------------------------------
# 🎯 STEP 2: AUTO-EDITOR (Aapka Channel -> Auto Edit Footer)
# ------------------------------------------
@client.on(events.NewMessage(chats=MY_TARGET_CHANNEL))
async def auto_edit_handler(event):
    if not event.message or not event.message.message:
        return

    print("🎯 Mere channel par naya post aaya! Edit karne jaa raha hoon...")
    original_text = event.message.message
    
    # Check karna ki hamari link pehle se na ho (taaki infinite loop na bane)
    if "https://t.me/sixtystore_loot" not in original_text:
        updated_text = original_text + MY_BRAND_FOOTER
        
        try:
            # Message ko instantly edit karna aapke footer link ke sath
            await client.edit_message(event.chat_id, event.message.id, updated_text)
            print("💥 [SUCCESS] Post successfully edit ho gaya aur brand link jud gayi!\n")
        except Exception as e:
            print(f"❌ Channel post edit karne mein error: {e}\n")

# ==========================================
# 🌍 DUMMY SERVER FOR RENDER FREE TIER
# ==========================================
def run_dummy_server():
    port = int(os.environ.get("PORT", 8000))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    print(f"🌍 Dummy web server running on port {port}")
    server.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()

# ==========================================
# 🚀 START THE BOT
# ==========================================
print("🚀 Master Combo Bot active ho gaya hai... Forwarding + Editing dono chalu hain!")
client.start()
client.run_until_disconnected()