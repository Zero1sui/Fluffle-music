import os
import requests
import subprocess
import glob

def get_commit_details():
    try:
        # Get the commit title (subject line)
        title = subprocess.check_output(["git", "log", "-1", "--format=%s"]).decode("utf-8").strip()
        # Get the commit description (body paragraphs)
        body = subprocess.check_output(["git", "log", "-1", "--format=%b"]).decode("utf-8").strip()
    except Exception as e:
        print(f"Error reading git log: {e}")
        title = "New Commit"
        body = "No description provided."
    return title, body

def send_to_telegram():
    token = os.environ.get("TELEGRAM_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    variant = os.environ.get("VARIANT", "foss")
    status = os.environ.get("BUILD_STATUS", "completed")

    if not token or not chat_id:
        print("Error: TELEGRAM_TOKEN or TELEGRAM_CHAT_ID environment variables are missing.")
        return

    title, body = get_commit_details()

    # --- CASE 1: WORKFLOW JUST STARTED ---
    if status == "started":
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        message_text = (
            f"⏳ *Fluffle Build Started!* ({variant.upper()} Variant)\n\n"
            f"📌 *Commit:* {title}\n"
            f"⏱ _Compiling the project... This usually takes about 3 ~ 5 minutes. Hang tight!_"
        )
        payload = {
            "chat_id": chat_id,
            "text": message_text,
            "parse_mode": "Markdown"
        }
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print(f"Sent 'Started' alert for {variant} to Telegram.")
        return

    # --- CASE 2: WORKFLOW COMPLETED (SEND APK) ---
    search_path = f"app/build/outputs/apk/{variant}/debug/*.apk"
    apk_files = glob.glob(search_path)

    if not apk_files:
        print(f"Error: No APK file found matching path: {search_path}")
        return
    
    apk_path = apk_files[0]
    message_text = (
        f"🚀 *New Build Successful!* ({variant.upper()} Variant)\n\n"
        f"📌 *Commit:* {title}\n"
        f"📝 *Description:*\n{body if body else 'No description.'}\n\n"
        f"📦 _The debug APK is attached below._"
    )

    url = f"https://api.telegram.org/bot{token}/sendDocument"
    print(f"Uploading {variant.upper()} APK to Telegram...")
    
    with open(apk_path, "rb") as apk_file:
        payload = {
            "chat_id": chat_id,
            "caption": message_text,
            "parse_mode": "Markdown"
        }
        files = {"document": apk_file}
        response = requests.post(url, data=payload, files=files)
        
        if response.status_code == 200:
            print(f"Successfully sent {variant} APK to Telegram!")
        else:
            print(f"Failed to send. Status: {response.status_code}\n{response.text}")

if __name__ == "__main__":
    send_to_telegram()
