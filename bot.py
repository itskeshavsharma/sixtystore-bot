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

SOURCE_CHANNELS = ['megadealv1', 'pocket_tv_mod_app'] 
CONVERTOR_BOT = 'ekconverter16bot' 
MY_TARGET_CHANNEL = 'SixtyStore_loot' 
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
        await client.forward_messages(CONVERTOR_BOT, event.message)
        print("✅ Converter bot ko safely forward ho gaya!\n")
    except Exception as e:
        print(f"❌ Forward karne mein error: {e}\n")

# ------------------------------------------
# 🎯 STEP 2: DOUBLE LOGO WATERMARKER & RE-POSTER
# ------------------------------------------
@client.on(events.NewMessage(chats=MY_TARGET_CHANNEL))
async def auto_logo_handler(event):
    if not event.message:
        return

    # Agar message mein photo nahi hai, toh sirf text edit karke chhod do
    if not event.message.media:
        if event.message.message and "https://t.me/sixtystore_loot" not in event.message.message:
            try:
                await client.edit_message(event.chat_id, event.message.id, event.message.message + MY_BRAND_FOOTER)
                print("📝 [TEXT ONLY] Footer link edit ho gayi.")
            except Exception as e:
                print(f"❌ Text edit error: {e}")
        return

    print("📸 Channel par photo wala post aaya! Double logo processing chalu...")
    original_text = event.message.message or ""
    
    # Loop protection tag
    if "[BRANDED]" in original_text:
        return

    try:
        # 1. Original photo download karo
        photo_path = await event.message.download_media()
        print("✅ Original photo downloaded.")

        # Main deal image ko open karo
        base_img = Image.open(photo_path).convert("RGBA")
        img_w, img_h = base_img.size  # Base image ka dynamic width aur height

        # ------------------------------------------
        # 🟢 PART A: TOP-LEFT LOGO PLACEMENT
        # ------------------------------------------
        if os.path.exists("logo.png"):
            logo_img = Image.open("logo.png").convert("RGBA")
            
            # 📐 Aapke logo ka size (Aapke screenshot ke hisab se perfect 110x110)
            logo_img = logo_img.resize((110, 110)) 
            
            # 📍 Coordinates: Unke logo ko cover karne ke liye bilkul top-left corner par
            logo_position = (15, 15)
            
            base_img.paste(logo_img, logo_position, logo_img)
            print("🎨 Top-Left Logo successfully pasted!")
        else:
            print("⚠️ logo.png nahi mili, step skip kiya.")

        # ------------------------------------------
        # 🟢 PART B: BOTTOM-CENTER STRIP PLACEMENT
        # ------------------------------------------
        if os.path.exists("footer_strip.png"):
            strip_img = Image.open("footer_strip.png").convert("RGBA")
            
            # 📐 Strip ka size (Width: 190, Height: 45) - Ise aavashyaktanusar chhota-bada kar sakte hain
            strip_w, strip_h = 190, 45
            strip_img = strip_img.resize((strip_w, strip_h))
            
            # 📍 Logic: Dynamic coordinates taaki strip hamesha niche center mein hi baithe
            strip_x = int((img_w - strip_w) / 2)
            strip_y = int(img_h - strip_h - 15)  # Niche se 15 pixels upar
            
            base_img.paste(strip_img, (strip_x, strip_y), strip_img)
            print("🎨 Bottom Footer Strip successfully pasted!")
        else:
            print("⚠️ footer_strip.png nahi mili, step skip kiya.")

        # Final conversion aur save
        base_img = base_img.convert("RGB")
        base_img.save("edited_photo.jpg")
        photo_to_send = "edited_photo.jpg"

        # 3. Purana unbranded message delete karo
        await client.delete_messages(event.chat_id, event.message.id)
        print("🗑️ Old post deleted.")

        # 4. Apna branded post upload karo
        final_text = original_text + MY_BRAND_FOOTER + "\n"
        await client.send_file(MY_TARGET_CHANNEL, photo_to_send, caption=final_text)
        print("💥 [SUCCESS] Double watermarked post successfully uploaded!\n")

        # Temporary files safai
        if os.path.exists(photo_path): os.remove(photo_path)
        if os.path.exists("edited_photo.jpg"): os.remove("edited_photo.jpg")

    except Exception as e:
        print(f"❌ Processing error: {e}\n")

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