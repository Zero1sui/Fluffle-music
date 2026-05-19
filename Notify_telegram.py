import os
import requests
import subprocess
import glob

def get_commit_details():
    try:
        title = subprocess.check_output(["git", "log", "-1", "--format=%s"]).decode("utf-8").strip()
        body = subprocess.check_output(["git", "log", "-1", "--format=%b"]).decode("utf-8").strip()
    except Exception as e:
        print(f"Error reading git log: {e}")
        title = "New Commit"
        body = "No description provided."
    return title, body

def send_apk_to_telegram():
    token = os.environ.get("TELEGRAM_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    variant = os.environ.get("VARIANT", "foss")  # Defaults to foss if not provided

    if not token or not chat_id:
        print("Error: TELEGRAM_TOKEN or TELEGRAM_CHAT_ID environment variables are missing.")
        return

    # Metro's exact output directory structure based on the matrix variant
    search_path = f"app/build/outputs/apk/{variant}/debug/*.apk"
    apk_files = glob.glob(search_path)

    if not apk_files:
        print(f"Error: No APK file found matching path: {search_path}")
        return
    
    apk_path = apk_files[0] # Pick the generated APK
    title, body = get_commit_details()

    # Formatted message with Markdown
    message_text = (
        f"🚀 *New Build Successful!* ({variant.upper()} Variant)\n\n"
        f"📌 *Commit:* {title}\n"
        f"📝 *Description:*\n{body if body else 'No description.'}\n\n"
        f"📦 _The debug APK is attached below._"
    )

    url = f"https://api.telegram.org/bot{token}/sendDocument"
    print(f"Uploading {variant.upper()} APK and sending notification to Telegram...")
    
    with open(apk_path, "rb") as apk_file:
        payload = {
            "chat_id": chat_id,
            "caption": message_text,
            "parse_mode": "Markdown"
        }
        files = {
            "document": apk_file
        }
        
        response = requests.post(url, data=payload, files=files)
        
        if response.status_code == 200:
            print(f"Successfully sent {variant} build to Telegram!")
        else:
            print(f"Failed to send. Server responded with: {response.status_code}")
            print(response.text)

if __name__ == "__main__":
    send_apk_to_telegram()
