"""Quick test script for Slack webhook"""
import os
from dotenv import load_dotenv
import requests

load_dotenv()

webhook_url = os.getenv("SLACK_WEBHOOK_URL")
print(f"Webhook URL: {webhook_url}")

if not webhook_url:
    print("❌ SLACK_WEBHOOK_URL not found in environment")
    exit(1)

# Send test message
message = {
    "text": "🧪 Test notification from LinkedIn Agent Workflow"
}

try:
    response = requests.post(
        webhook_url,
        json=message,
        headers={"Content-Type": "application/json"}
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

    if response.status_code == 200:
        print("✅ Slack webhook is working!")
    else:
        print(f"❌ Slack webhook failed: {response.text}")

except Exception as e:
    print(f"❌ Error: {e}")
