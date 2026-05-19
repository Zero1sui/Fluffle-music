import os
import sys
import requests

def main():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    variant = os.environ.get("VARIANT", "unknown")
    status = os.environ.get("BUILD_STATUS", "unknown")

    if not token or not chat_id:
        print("❌ Missing credentials. Exiting script.")
        sys.exit(1)

    # 1. Handle the START message
    if status == "started":
        message = f"🚀 **Quick Test Build Started**\n\n• **Variant:** {variant}\n• **Status:** Compiling..."
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
        
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("✅ Start message sent to Telegram!")
        else:
            print(f"❌ Failed to send message: {response.text}")

    # 2. Handle the COMPLETED message (Sends the actual APK file)
    elif status == "completed":
        apk_dir = f"app/build/outputs/apk/{variant}"
        apk_file = None
        
        if os.path.exists(apk_dir):
            for file in os.listdir(apk_dir):
                if file.endswith(".apk"):
                    apk_file = os.path.join(apk_dir, file)
                    break

        if apk_file:
            print(f"📦 Found APK: {apk_file}. Uploading to Telegram...")
            url = f"https://api.telegram.org/bot{token}/sendDocument"
            caption = f"✅ **Quick Test Build Finished!**\n\n• **File:** {os.path.basename(apk_file)}"
            
            with open(apk_file, 'rb') as f:
                files = {'document': f}
                data = {'chat_id': chat_id, 'caption': caption, 'parse_mode': 'Markdown'}
                response = requests.post(url, data=data, files=files)
                
            if response.status_code == 200:
                print("✅ APK successfully sent to Telegram!")
            else:
                print(f"❌ Failed to send APK: {response.text}")
        else:
            print(f"❌ Error: No APK file found in path: {apk_dir}")

if __name__ == "__main__":
    main()
