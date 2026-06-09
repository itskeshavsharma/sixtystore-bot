import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from telethon import TelegramClient, events
from PIL import Image

# ==========================================
# ⚙️ SETTINGS (Keys Render Dashboard se uthayega)
# ==========================================
API_ID = int(os.environ.get("API_ID", 1234567))  
API_HASH = os.environ.get("API_HASH", "placeholder_hash")

SOURCE_CHANNELS = ['BhramsBots1', 'megadealv1', 'pocket_tv_mod_app'] 
CONVERTOR_BOT = 'ekconverter16bot' 
MY_TARGET_CHANNEL = 'SixtyStore_loot' 
MY_BRAND_FOOTER = "\n\nJoin for more premium loots ❤️👇\nhttps://t.me/sixtystore_loot"

# 🔑 AAPKA SECRET KEYWORD (Jo posts ko track karega)
SECRET_KEYWORD = "##FROM_BHRAMSBOT##"

# 🧠 LOOP PROTECTION TRACKER
PROCESSED_MESSAGES = set()

# ==========================================
# 🤖 BOT INITIALIZATION
# ==========================================
client = TelegramClient('forwarder_session', API_ID, API_HASH)

# ------------------------------------------
# 🔄 STEP 1: AUTO-FORWARDER + KEYWORD INJECTOR
# ------------------------------------------
@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def instant_forward_handler(event):
    if not event.message:
        return
    
    # Pata karo ki post BhramsBots1 se aayi hai ya kahi aur se
    chat_entity = await event.get_chat()
    chat_username = getattr(chat_entity, 'username', '')
    
    print(f"📥 Source channel ({chat_username}) par naya post aaya!")
    
    try:
        # Agar post BhramsBots1 se aayi hai, toh text ke niche secret keyword chipka do
        if chat_username and chat_username.lower() == 'bhramsbots1':
            original_text = event.message.message or ""
            event.message.message = f"{original_text}\n{SECRET_KEYWORD}"
            print("🔑 Secret Keyword injected for BhramsBots1!")
            
        # Converter bot ko message bhejdo (ab modified message jayega)
        await client.send_message(CONVERTOR_BOT, event.message)
        print("✅ Converter bot ko safely bhej diya gaya!\n")
    except Exception as e:
        print(f"❌ Forward karne mein error: {e}\n")

# ------------------------------------------
# 🎯 STEP 2: KEYWORD DETECTOR & WATERMARKER (Sirf 2 Logos)
# ------------------------------------------
@client.on(events.NewMessage(chats=MY_TARGET_CHANNEL))
async def auto_logo_handler(event):
    if not event.message:
        return

    # 🛑 1. ID CHECK: Loop protection
    if event.message.id in PROCESSED_MESSAGES:
        return

    original_text = event.message.message or ""
    
    # 🛑 2. TEXT CHECK: Duplicate protection
    if "https://t.me/sixtystore_loot" in original_text:
        return

    PROCESSED_MESSAGES.add(event.message.id)

    # 🧠 CHECK KHARO KYA ISME HAMARA SECRET KEYWORD HAI?
    is_bhrams_post = SECRET_KEYWORD in original_text
    
    # Clean the text (Secret keyword ko main post se hamesha ke liye mita do)
    clean_text = original_text.replace(SECRET_KEYWORD, "").strip()

    # 📝 CASE A: AGAR PURE TEXT HAI (Bina Photo Ke)
    if not event.message.media:
        try:
            final_text = clean_text + MY_BRAND_FOOTER
            await client.edit_message(event.chat_id, event.message.id, final_text)
            print("📝 [SUCCESS] Pure text post par link add ho gayi!\n")
        except Exception as e:
            print(f"❌ Text edit karne mein error: {e}\n")
        return

    # 📸 CASE B: AGAR PHOTO WALA MESSAGE HAI
    # ⏩ AGAR SECRET KEYWORD NAHI MILA: Yaani yeh pocket_tv ya megadeal ki post hai, toh image edit SKIP karo
    if not is_bhrams_post:
        print("⏩ Kisi aur channel ki post hai, image edit SKIP. Sirf text link add hogi.")
        try:
            final_text = clean_text + MY_BRAND_FOOTER
            await client.edit_message(event.chat_id, event.message.id, final_text)
            print("📝 [SUCCESS] Normal post par link add ho gayi bina image chhede!\n")
        except Exception as e:
            print(f"❌ Just link edit error: {e}")
        return

    # 🎯 AGAR KEYWORD MIL GAYA: Toh image par logo lagao aur re-post karo!
    print("🎯 SECRET KEYWORD FOUND! BhramsBots1 verified. 2-Logo editing chalu...")
    try:
        photo_path = await event.message.download_media()
        base_img = Image.open(photo_path).convert("RGBA")
        img_w, img_h = base_img.size

        # 1️⃣ Image 1: Top-Left Logo placement
        if os.path.exists("logo.png"):
            logo_img = Image.open("logo.png").convert("RGBA")
            logo_img = logo_img.resize((110, 110)) 
            logo_position = (15, 15)
            base_img.paste(logo_img, logo_position, logo_img)
            print("🎨 Top-Left Logo pasted.")

        # 2️⃣ Image 2: Bottom-Center Strip placement
        if os.path.exists("footer_strip.png"):
            strip_img = Image.open("footer_strip.png").convert("RGBA")
            strip_w, strip_h = 190, 45
            strip_img = strip_img.resize((strip_w, strip_h))
            strip_x = int((img_w - strip_w) / 2)
            strip_y = int(img_h - strip_h - 15)
            base_img.paste(strip_img, (strip_x, strip_y), strip_img)
            print("🎨 Bottom Footer Strip pasted.")

        # Image save karo
        base_img = base_img.convert("RGB")
        base_img.save("edited_photo.jpg")
        
        # Purana post delete karo (jisme secret keyword dikh raha tha)
        await client.delete_messages(event.chat_id, event.message.id)
        print("🗑️ Old post with secret keyword deleted.")

        # Naya customized post bhejdo clean text aur footer ke sath
        final_text = clean_text + MY_BRAND_FOOTER
        sent_msg = await client.send_file(MY_TARGET_CHANNEL, "edited_photo.jpg", caption=final_text)
        PROCESSED_MESSAGES.add(sent_msg.id)
        print("💥 [SUCCESS] Clean text + 2-Logo post successfully re-uploaded!\n")

        # Safai
        if os.path.exists(photo_path): os.remove(photo_path)
        if os.path.exists("edited_photo.jpg"): os.remove("edited_photo.jpg")

    except Exception as e:
        print(f"❌ Photo processing error: {e}\n")

# ==========================================
# 🌍 DUMMY SERVER WITH TINY RESPONSE FOR CRON-JOB
# ==========================================
class TinyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Bot is awake!")
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

def run_dummy_server():
    port = int(os.environ.get("PORT", 8000))
    server = HTTPServer(('0.0.0.0', port), TinyRequestHandler)
    server.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()

client.start()
client.run_until_disconnected()