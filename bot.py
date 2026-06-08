# import os
# import threading
# from http.server import BaseHTTPRequestHandler, HTTPServer
# from telethon import TelegramClient, events
# from PIL import Image

# # ==========================================
# # ⚙️ SETTINGS (Keys Render Dashboard se uthayega)
# # ==========================================
# API_ID = int(os.environ.get("API_ID", 1234567))  
# API_HASH = os.environ.get("API_HASH", "placeholder_hash")

# SOURCE_CHANNELS = ['megadealv1', 'pocket_tv_mod_app'] 
# CONVERTOR_BOT = 'ekconverter16bot' 
# MY_TARGET_CHANNEL = 'SixtyStore_loot' 
# MY_BRAND_FOOTER = "\n\nJoin for more premium loots ❤️👇\nhttps://t.me/sixtystore_loot"

# # 🧠 LOOP PROTECTION TRACKER
# PROCESSED_MESSAGES = set()

# # ==========================================
# # 🤖 BOT INITIALIZATION
# # ==========================================
# client = TelegramClient('forwarder_session', API_ID, API_HASH)

# # ------------------------------------------
# # 🔄 STEP 1: AUTO-FORWARDER (Source -> Converter Bot)
# # ------------------------------------------
# @client.on(events.NewMessage(chats=SOURCE_CHANNELS))
# async def instant_forward_handler(event):
#     if not event.message:
#         return
#     print("📥 Source channel par naya post aaya! Converter bot ko forward kar raha hoon...")
#     try:
#         await client.forward_messages(CONVERTOR_BOT, event.message)
#         print("✅ Converter bot ko safely forward ho gaya!\n")
#     except Exception as e:
#         print(f"❌ Forward karne mein error: {e}\n")

# # ------------------------------------------
# # 🎯 STEP 2: OPEN PHOTO WATERMARKER & RE-POSTER (No Filters)
# # ------------------------------------------
# @client.on(events.NewMessage(chats=MY_TARGET_CHANNEL))
# async def auto_logo_handler(event):
#     if not event.message:
#         return

#     # 🛑 1. ID CHECK: Loop protection
#     if event.message.id in PROCESSED_MESSAGES:
#         return

#     original_text = event.message.message or ""
    
#     # 🛑 2. TEXT CHECK: Duplicate protection
#     if "https://t.me/sixtystore_loot" in original_text:
#         return

#     PROCESSED_MESSAGES.add(event.message.id)

#     # 📝 CASE A: AGAR PURE TEXT HAI (Bina Photo Ke)
#     if not event.message.media:
#         try:
#             updated_text = original_text + MY_BRAND_FOOTER
#             await client.edit_message(event.chat_id, event.message.id, updated_text)
#             print("📝 [SUCCESS] Pure text post par footer link jod di gayi!\n")
#         except Exception as e:
#             print(f"❌ Text edit karne mein error: {e}\n")
#         return

#     # 📸 CASE B: AGAR PHOTO WALA MESSAGE HAI (Ab har photo process hogi!)
#     print("📸 Channel par photo wala post aaya! Triple logo processing chalu...")
#     try:
#         # Photo download karo
#         photo_path = await event.message.download_media()
#         base_img = Image.open(photo_path).convert("RGBA")
#         img_w, img_h = base_img.size

#         # 1️⃣ Top-Left Logo placement
#         if os.path.exists("logo.png"):
#             logo_img = Image.open("logo.png").convert("RGBA")
#             logo_img = logo_img.resize((110, 110)) 
#             logo_position = (15, 15)
#             base_img.paste(logo_img, logo_position, logo_img)
#             print("🎨 Top-Left Logo successfully pasted!")

#         # 2️⃣ Bottom-Center Strip placement
#         if os.path.exists("footer_strip.png"):
#             strip_img = Image.open("footer_strip.png").convert("RGBA")
#             strip_w, strip_h = 190, 45
#             strip_img = strip_img.resize((strip_w, strip_h))
            
#             strip_x = int((img_w - strip_w) / 2)
#             strip_y = int(img_h - strip_h - 15)
            
#             base_img.paste(strip_img, (strip_x, strip_y), strip_img)
#             print("🎨 Bottom Footer Strip successfully pasted!")

#         # 3️⃣ Center Solid White + Black Logo placement
#         if os.path.exists("center_watermark.png"):
#             center_w_img = Image.open("center_watermark.png").convert("RGBA")
            
#             # Photo ke size ke hisab se center watermark ka size (width ka 45%)
#             wm_size = int(img_w * 0.45)
#             center_w_img = center_w_img.resize((wm_size, wm_size))
            
#             wm_x = int((img_w - wm_size) / 2)
#             wm_y = int((img_h - wm_size) / 2)
            
#             base_img.paste(center_w_img, (wm_x, wm_y), center_w_img)
#             print("🎨 Center White-Black Watermark successfully pasted!")

#         # Save final image
#         base_img = base_img.convert("RGB")
#         base_img.save("edited_photo.jpg")
#         photo_to_send = "edited_photo.jpg"

#         # Purana bina logo wala post delete karo
#         await client.delete_messages(event.chat_id, event.message.id)
#         print("🗑️ Old post deleted.")

#         # Naya customized post bhejdo (Footer link ke sath)
#         final_text = original_text + MY_BRAND_FOOTER
        
#         sent_msg = await client.send_file(MY_TARGET_CHANNEL, photo_to_send, caption=final_text)
#         PROCESSED_MESSAGES.add(sent_msg.id)
#         print("💥 [SUCCESS] Triple watermarked post successfully uploaded!\n")

#         # Safai
#         if os.path.exists(photo_path): os.remove(photo_path)
#         if os.path.exists("edited_photo.jpg"): os.remove("edited_photo.jpg")

#     except Exception as e:
#         print(f"❌ Photo processing error: {e}\n")

# # ==========================================
# # 🌍 DUMMY SERVER WITH TINY RESPONSE FOR CRON-JOB
# # ==========================================
# class TinyRequestHandler(BaseHTTPRequestHandler):
#     def do_GET(self):
#         self.send_response(200)
#         self.send_header("Content-type", "text/plain")
#         self.end_headers()
#         self.wfile.write(b"Bot is awake!")
#     def do_HEAD(self):
#         self.send_response(200)
#         self.end_headers()

# def run_dummy_server():
#     port = int(os.environ.get("PORT", 8000))
#     server = HTTPServer(('0.0.0.0', port), TinyRequestHandler)
#     server.serve_forever()

# threading.Thread(target=run_dummy_server, daemon=True).start()

# client.start()
# client.run_until_disconnected()


import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from telethon import TelegramClient, events
from PIL import Image
import cv2
import numpy as np

# ==========================================
# ⚙️ SETTINGS (Keys Render Dashboard se uthayega)
# ==========================================
API_ID = int(os.environ.get("API_ID", 1234567))  
API_HASH = os.environ.get("API_HASH", "placeholder_hash")

SOURCE_CHANNELS = ['BhramsBots1', 'megadealv1', 'pocket_tv_mod_app'] 
CONVERTOR_BOT = 'ekconverter16bot' 
MY_TARGET_CHANNEL = 'SixtyStore_loot' 
MY_BRAND_FOOTER = "\n\nJoin for more premium loots ❤️👇\nhttps://t.me/sixtystore_loot"

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
# 🎯 STEP 2: SMART VISION WATERMARKER (Sirf 2 Logos)
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

    # 📝 CASE A: AGAR PURE TEXT HAI (Bina Photo Ke)
    if not event.message.media:
        try:
            updated_text = original_text + MY_BRAND_FOOTER
            await client.edit_message(event.chat_id, event.message.id, updated_text)
            print("📝 [SUCCESS] Pure text post par footer link jod di gayi!\n")
        except Exception as e:
            print(f"❌ Text edit karne mein error: {e}\n")
        return

    # 📸 CASE B: AGAR PHOTO WALA MESSAGE HAI
    print("📸 Channel par photo wala post aaya! Smart image analysis chalu...")
    try:
        # Photo download karo
        photo_path = await event.message.download_media()
        
        # 🧠 COMPUTER VISION: Check karo kya unka logo image mein hai?
        has_logo = False
        if os.path.exists("target_watermark.png"):
            main_img_cv = cv2.imread(photo_path, cv2.IMREAD_GRAYSCALE)
            template_cv = cv2.imread("target_watermark.png", cv2.IMREAD_GRAYSCALE)
            
            if main_img_cv is not None and template_cv is not None:
                result = cv2.matchTemplate(main_img_cv, template_cv, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, _ = cv2.minMaxLoc(result)
                
                print(f"🔍 Image Match Score: {max_val:.2f} (Humein kam se kam 0.60 chahiye)")
                # Threshold thoda kam kar diya hai taaki match aasani se pakad sake
                if max_val >= 0.60:
                    has_logo = True
        else:
            print("⚠️ target_watermark.png file nahi mili! Matching skip ho gayi.")

        # 🚫 LOGO NAHI MILA: Toh photo ko bina chhede sirf link edit karke chod do!
        if not has_logo:
            print("⏩ Target logo nahi mila. Photo edit SKIP ki ja rahi hai.")
            try:
                updated_text = original_text + MY_BRAND_FOOTER
                await client.edit_message(event.chat_id, event.message.id, updated_text)
                print("📝 [SUCCESS] Bina logo wali post par sirf text link add ho gayi!\n")
            except Exception as e:
                print(f"❌ Just link edit error: {e}")
            if os.path.exists(photo_path): os.remove(photo_path)
            return

        # 🎯 LOGO MIL GAYA: Toh sirf 2 logo lagao aur re-post karo!
        print("🎯 MATCH FOUND! Logo detected. Sirf 2 logo lagaye ja rahe hain...")
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

        # Save and send (Center wala sab hata diya hai)
        base_img = base_img.convert("RGB")
        base_img.save("edited_photo.jpg")
        
        await client.delete_messages(event.chat_id, event.message.id)
        final_text = original_text + MY_BRAND_FOOTER
        sent_msg = await client.send_file(MY_TARGET_CHANNEL, "edited_photo.jpg", caption=final_text)
        PROCESSED_MESSAGES.add(sent_msg.id)
        print("💥 [SUCCESS] 2-Logo watermarked post uploaded successfully!\n")

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