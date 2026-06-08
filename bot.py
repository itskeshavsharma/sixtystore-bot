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

# SOURCE_CHANNELS jahan se bot forward karega
SOURCE_CHANNELS = ['BhramsBots1','megadealv1', 'pocket_tv_mod_app'] 
CONVERTOR_BOT = 'ekconverter16bot' 
MY_TARGET_CHANNEL = 'SixtyStore_loot' 
MY_BRAND_FOOTER = "\n\nJoin for more premium loots ❤️👇\nhttps://t.me/sixtystore_loot"

# 🎯 JIS CHANNEL KE POST PAR LOGO LAGANA HAI (Username bina @ ke daalein)
# Agar megadealv1 hi LootsVault ka source hai, toh isko aise hi rehne dein
LOGO_ONLY_SOURCE_CHANNEL = 'BhramsBots1' 

# 🧠 LOOP PROTECTION TRACKER
PROCESSED_MESSAGES = set()

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
        await client.forward_messages(CONVERTOR_BOT, event.message)
        print("✅ Converter bot ko safely forward ho gaya!\n")
    except Exception as e:
        print(f"❌ Forward karne mein error: {e}\n")

# ------------------------------------------
# 🎯 STEP 2: LOGO WATERMARKER & RE-POSTER (With Source Check)
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

    # CHECK KARO: Kya yeh post hamare target source channel (LootsVault/megadealv1) se aayi hai?
    is_target_source = False
    
    # Telegram forward header check karein
    if event.message.fwd_from and event.message.fwd_from.from_id:
        try:
            # Original channel ki details nikalna
            fwd_chat = await client.get_entity(event.message.fwd_from.from_id)
            if fwd_chat and getattr(fwd_chat, 'username', '').lower() == LOGO_ONLY_SOURCE_CHANNEL.lower():
                is_target_source = True
        except Exception as e:
            print(f"⚠️ Forward source check error: {e}")

    # 📝 CASE A: AGAR PURE TEXT HAI YA PHOTO KISI AUR CHANNEL KI HAI (Bina Logo Ke)
    if not event.message.media or not is_target_source:
        if not is_target_source and event.message.media:
            print("⏩ Kisi aur channel ki photo hai. Logo processing SKIP ki gayi.")
        try:
            updated_text = original_text + MY_BRAND_FOOTER
            await client.edit_message(event.chat_id, event.message.id, updated_text)
            print("📝 [SUCCESS] Post par normal footer link jod di gayi (No Logo)!\n")
        except Exception as e:
            print(f"❌ Normal edit error: {e}\n")
        return

    # 📸 CASE B: AGAR TARGET CHANNEL KI PHOTO HAI (Logo Edit + Re-post)
    print(f"🎯 MATCH FOUND! {LOGO_ONLY_SOURCE_CHANNEL} ki photo aayi hai. Double logo processing chalu...")
    try:
        photo_path = await event.message.download_media()
        base_img = Image.open(photo_path).convert("RGBA")
        img_w, img_h = base_img.size

        # Top-Left Logo placement
        if os.path.exists("logo.png"):
            logo_img = Image.open("logo.png").convert("RGBA")
            logo_img = logo_img.resize((110, 110)) 
            logo_position = (15, 15)
            base_img.paste(logo_img, logo_position, logo_img)
            print("🎨 Top-Left Logo successfully pasted!")

        # Bottom-Center Strip placement
        if os.path.exists("footer_strip.png"):
            strip_img = Image.open("footer_strip.png").convert("RGBA")
            strip_w, strip_h = 190, 45
            strip_img = strip_img.resize((strip_w, strip_h))
            
            strip_x = int((img_w - strip_w) / 2)
            strip_y = int(img_h - strip_h - 15)
            
            base_img.paste(strip_img, (strip_x, strip_y), strip_img)
            print("🎨 Bottom Footer Strip successfully pasted!")

        # Save edited image
        base_img = base_img.convert("RGB")
        base_img.save("edited_photo.jpg")
        photo_to_send = "edited_photo.jpg"

        # Purana bina logo wala post delete karo
        await client.delete_messages(event.chat_id, event.message.id)
        print("🗑️ Old post deleted.")

        # Naya branded post bhejdo
        final_text = original_text + MY_BRAND_FOOTER
        sent_msg = await client.send_file(MY_TARGET_CHANNEL, photo_to_send, caption=final_text)
        PROCESSED_MESSAGES.add(sent_msg.id)
        print("💥 [SUCCESS] Double watermarked post uploaded successfully!\n")

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
client.run_disconnected()