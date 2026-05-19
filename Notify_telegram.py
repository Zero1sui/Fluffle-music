import os
import sys

def main():
    token = os.environ.get("TELEGRAM_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    variant = os.environ.get("VARIANT", "unknown")
    status = os.environ.get("BUILD_STATUS", "unknown")

    print("\n======== LOCAL DIAGNOSTIC START ========")
    print(f"Checking Environment Variables...")
    
    if not token:
        print("❌ CRITICAL ERROR: TELEGRAM_TOKEN environment variable is missing or blank.")
    else:
        print(f"✅ TELEGRAM_TOKEN found! (Starts with: {token[:6]}...)")

    if not chat_id:
        print("❌ CRITICAL ERROR: TELEGRAM_CHAT_ID environment variable is missing or blank.")
    else:
        print(f"✅ TELEGRAM_CHAT_ID found! (Value: {chat_id})")

    if not token or not chat_id:
        print("Stopping execution due to missing credentials.")
        print("========================================\n")
        sys.exit(1) # Gracefully fail the step so you see it in the logs

    print(f"✅ Context verified. Build Variant: {variant} | Status: {status}")
    print("Attempting to format notification message...")
    
    # Your existing message formatting/sending logic goes here
    print("🚀 Script finished testing successfully!")
    print("========================================\n")

if __name__ == "__main__":
    main()
