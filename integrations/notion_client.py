"""Notion API client for reading and updating content pipeline"""

import os
import json
from datetime import datetime
from pathlib import Path
from notion_client import Client
from typing import Optional, Dict, Any, List


class NotionClient:
    """Handle all Notion API interactions"""

    def __init__(self):
        self.client = Client(auth=os.getenv("NOTION_TOKEN"))
        self.database_id = os.getenv("NOTION_DATABASE_ID")
        self.state_file = Path(".last_processed")

    def get_next_idea(self) -> Optional[Dict[str, Any]]:
        """Query Notion for the next idea with Status = 'Idea'"""

        try:
            response = self.client.databases.query(
                database_id=self.database_id,
                filter={
                    "property": "Status",
                    "status": {
                        "equals": "Idea"
                    }
                },
                page_size=1
            )

            results = response.get("results", [])
            if not results:
                return None

            page = results[0]
            props = page["properties"]

            # Parse properties
            return {
                "page_id": page["id"],
                "topic": self._get_title(props.get("Name")),
                "goal": self._get_select(props.get("Goal")),
                "context": self._get_rich_text(props.get("Context/Notes", {}))
            }

        except Exception as e:
            print(f"❌ Error querying Notion: {e}")
            return None

    def update_status(self, page_id: str, status: str):
        """Update the status of a Notion page"""

        try:
            self.client.pages.update(
                page_id=page_id,
                properties={
                    "Status": {
                        "status": {
                            "name": status
                        }
                    }
                }
            )
            print(f"✅ Updated status to: {status}")

        except Exception as e:
            print(f"❌ Error updating status: {e}")

    def update_with_research(self, page_id: str, research_brief: str):
        """Update page with research results and set status to Drafting"""

        try:
            self.client.pages.update(
                page_id=page_id,
                properties={
                    "Status": {
                        "status": {"name": "Drafting"}
                    },
                    "Research Brief": {
                        "rich_text": [
                            {
                                "text": {
                                    "content": research_brief[:2000]  # Notion limit
                                }
                            }
                        ]
                    }
                }
            )
            print(f"✅ Updated with research brief")

        except Exception as e:
            print(f"❌ Error updating research: {e}")

    def update_with_draft(self, page_id: str, draft_data: Dict[str, Any]):
        """Update page with final draft and set status to Ready"""

        try:
            properties = {
                "Status": {
                    "status": {"name": "Ready"}
                },
                "Hook Option 1": {
                    "rich_text": [{"text": {"content": draft_data["hooks"][0][:2000]}}]
                },
                "Hook Option 2": {
                    "rich_text": [{"text": {"content": draft_data["hooks"][1][:2000]}}]
                },
                "Hook Option 3": {
                    "rich_text": [{"text": {"content": draft_data["hooks"][2][:2000]}}]
                },
                "Draft Body": {
                    "rich_text": [{"text": {"content": draft_data["post_body"][:2000]}}]
                },
                "CTA": {
                    "rich_text": [{"text": {"content": draft_data["cta"][:2000]}}]
                },
                "Hashtags": {
                    "rich_text": [{"text": {"content": " ".join(draft_data["hashtags"])}}]
                },
                "Image Suggestion": {
                    "rich_text": [{"text": {"content": draft_data["visual_suggestion"][:2000]}}]
                },
                "Format Type": {
                    "select": {"name": draft_data["visual_format"]}
                }
            }

            self.client.pages.update(
                page_id=page_id,
                properties=properties
            )
            print(f"✅ Updated with complete draft")

        except Exception as e:
            print(f"❌ Error updating draft: {e}")

    # Helper methods
    def _get_title(self, prop) -> str:
        """Extract title from property"""
        if not prop or not prop.get("title"):
            return ""
        return prop["title"][0]["plain_text"] if prop["title"] else ""

    def _get_rich_text(self, prop) -> str:
        """Extract rich text from property"""
        if not prop or not prop.get("rich_text"):
            return ""
        return prop["rich_text"][0]["plain_text"] if prop["rich_text"] else ""

    def _get_select(self, prop) -> str:
        """Extract select value from property"""
        if not prop or not prop.get("select"):
            return ""
        return prop["select"]["name"] if prop["select"] else ""

    # Timestamp tracking methods
    def get_last_processed_time(self) -> Optional[str]:
        """Get the timestamp of the last processed item"""
        if not self.state_file.exists():
            return None

        try:
            with open(self.state_file, 'r') as f:
                data = json.load(f)
                return data.get('last_processed')
        except (json.JSONDecodeError, IOError):
            return None

    def update_last_processed_time(self, timestamp: str = None):
        """Update the last processed timestamp"""
        if timestamp is None:
            timestamp = datetime.utcnow().isoformat() + "Z"

        try:
            with open(self.state_file, 'w') as f:
                json.dump({'last_processed': timestamp}, f)
        except IOError as e:
            print(f"⚠️  Warning: Could not save timestamp: {e}")

    def get_all_pending_ideas(self) -> List[Dict[str, Any]]:
        """Get all ideas with Status = 'Idea' (for batch processing)"""
        try:
            response = self.client.databases.query(
                database_id=self.database_id,
                filter={
                    "property": "Status",
                    "status": {
                        "equals": "Idea"
                    }
                },
                sorts=[
                    {
                        "timestamp": "created_time",
                        "direction": "ascending"
                    }
                ]
            )

            results = response.get("results", [])
            ideas = []

            for page in results:
                props = page["properties"]
                ideas.append({
                    "page_id": page["id"],
                    "topic": self._get_title(props.get("Name")),
                    "goal": self._get_select(props.get("Goal")),
                    "context": self._get_rich_text(props.get("Context/Notes", {})),
                    "created_time": page.get("created_time")
                })

            return ideas

        except Exception as e:
            print(f"❌ Error querying Notion for all ideas: {e}")
            return []

    def get_new_ideas(self, since_timestamp: str = None) -> List[Dict[str, Any]]:
        """Get ideas created after the specified timestamp"""
        if since_timestamp is None:
            since_timestamp = self.get_last_processed_time()

        # If no timestamp, fall back to get_all_pending_ideas
        if since_timestamp is None:
            return self.get_all_pending_ideas()

        try:
            # Build filter with both status and timestamp
            filter_conditions = {
                "and": [
                    {
                        "property": "Status",
                        "status": {
                            "equals": "Idea"
                        }
                    },
                    {
                        "timestamp": "created_time",
                        "created_time": {
                            "after": since_timestamp
                        }
                    }
                ]
            }

            response = self.client.databases.query(
                database_id=self.database_id,
                filter=filter_conditions,
                sorts=[
                    {
                        "timestamp": "created_time",
                        "direction": "ascending"
                    }
                ]
            )

            results = response.get("results", [])
            ideas = []

            for page in results:
                props = page["properties"]
                ideas.append({
                    "page_id": page["id"],
                    "topic": self._get_title(props.get("Name")),
                    "goal": self._get_select(props.get("Goal")),
                    "context": self._get_rich_text(props.get("Context/Notes", {})),
                    "created_time": page.get("created_time")
                })

            return ideas

        except Exception as e:
            print(f"❌ Error querying Notion for new ideas: {e}")
            return []
