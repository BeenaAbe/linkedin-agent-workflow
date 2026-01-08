"""Slack notification client"""

import os
import requests
from typing import Dict, Any


class SlackNotifier:
    """Send notifications to Slack"""

    def __init__(self):
        self.webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    def send_draft_notification(self, draft_data: Dict[str, Any]):
        """Send notification when draft is ready"""

        print(f"🔔 Attempting to send Slack notification...")
        print(f"   Webhook URL configured: {bool(self.webhook_url)}")

        if not self.webhook_url:
            print("⚠️  Slack webhook URL not configured, skipping notification")
            return

        # Build Slack message with blocks
        message = {
            "text": "✨ New LinkedIn Draft Ready!",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "✨ New LinkedIn Draft Ready"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Topic:* {draft_data['topic']}\n*Goal:* {draft_data['goal']}"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Hook Options:*\n1. {draft_data['hooks'][0][:100]}...\n2. {draft_data['hooks'][1][:100]}..."
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Draft Preview:*\n{draft_data['post_body'][:200]}..."
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Review in Notion"
                            },
                            "url": f"https://notion.so/{draft_data['page_id'].replace('-', '')}"
                        }
                    ]
                }
            ]
        }

        try:
            print(f"   Sending POST request to Slack...")
            response = requests.post(
                self.webhook_url,
                json=message,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            print(f"   Response status: {response.status_code}")
            print(f"   Response body: {response.text}")
            response.raise_for_status()
            print("✅ Slack notification sent successfully!")

        except Exception as e:
            print(f"❌ Error sending Slack notification: {e}")
            import traceback
            traceback.print_exc()

    def send_error_notification(self, error_message: str, topic: str):
        """Send error notification"""

        if not self.webhook_url:
            return

        message = {
            "text": f"❌ LinkedIn workflow failed for: {topic}",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"❌ *Workflow Error*\n\n*Topic:* {topic}\n*Error:* {error_message}"
                    }
                }
            ]
        }

        try:
            requests.post(self.webhook_url, json=message)
        except Exception as e:
            print(f"❌ Error sending error notification: {e}")
