import os
import requests
import subprocess

def get_commit_details():
    try:
        # Get the commit title (subject)
        title = subprocess.check_output(["git", "log", "-1", "--format=%s"]).decode("utf-8").strip()
        # Get the commit description (body)
        body = subprocess.check_output(["git", "log", "-1", "--format=%b"]).decode("utf-8").strip()
    except Exception as e:
        print(f"Error reading git log: {e}")
        title = "New Commit"
        body = "No description provided."
    return title, body

def send_apk_to_telegram():
    token = os.environ.get("TELEGRAM_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    apk_path = "app/build/outputs/apk/debug/app-debug.apk"

    if not token or not chat_id:
        print("Error: TELEGRAM_TOKEN or TELEGRAM_CHAT_ID environment variables are missing.")
        return

    title, body = get_commit_details()

    # Format the message using Markdown
    message_text = (
        f"🚀 *New Build Successful!*\n\n"
        f"📌 *Commit:* {title}\n"
        f"📝 *Description:*\n{body if body else 'No description.'}\n\n"
        f"📦 _The debug APK is attached below._"
    )

    url = f"https://api.telegram.org/bot{token}/sendDocument"
    
    # Check if the APK actually exists before trying to send it
    if not os.path.exists(apk_path):
        print(f"Error: APK file not found at {apk_path}")
        return

    print("Uploading APK and sending notification to Telegram...")
    
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
            print("Successfully sent to Telegram!")
        else:
            print(f"Failed to send. Server responded with: {response.status_code}")
            print(response.text)

if __name__ == "__main__":
    send_apk_to_telegram()
