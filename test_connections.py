"""Test script to verify all connections are working"""

import os
from dotenv import load_dotenv
from integrations.notion_client import NotionClient
from tavily import TavilyClient
from langchain_openai import ChatOpenAI

load_dotenv()

def test_notion():
    """Test Notion connection"""
    print("\n🔍 Testing Notion connection...")
    try:
        notion = NotionClient()
        ideas = notion.get_all_pending_ideas()
        print(f"✅ Notion connected! Found {len(ideas)} pending ideas")

        if ideas:
            print(f"   First idea: {ideas[0]['topic']}")
        return True
    except Exception as e:
        print(f"❌ Notion error: {e}")
        return False


def test_tavily():
    """Test Tavily connection"""
    print("\n🔍 Testing Tavily connection...")
    try:
        tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        results = tavily.search(query="AI agents test", max_results=1)
        print(f"✅ Tavily connected! Found {len(results.get('results', []))} results")
        return True
    except Exception as e:
        print(f"❌ Tavily error: {e}")
        return False


def test_openrouter():
    """Test OpenRouter connection"""
    print("\n🔍 Testing OpenRouter (Claude) connection...")
    try:
        llm = ChatOpenAI(
            model="anthropic/claude-3.5-sonnet",
            openai_api_key=os.getenv("OPENROUTER_API_KEY"),
            openai_api_base="https://openrouter.ai/api/v1",
            temperature=0.3,
            max_tokens=100
        )
        response = llm.invoke("Say 'Connection successful' in exactly those words.")
        print(f"✅ OpenRouter connected!")
        print(f"   Response: {response.content[:100]}")
        return True
    except Exception as e:
        print(f"❌ OpenRouter error: {e}")
        return False


def test_change_detection():
    """Test timestamp tracking"""
    print("\n🔍 Testing change detection...")
    try:
        notion = NotionClient()

        # Check last processed time
        last_time = notion.get_last_processed_time()
        if last_time:
            print(f"✅ Last processed: {last_time[:19]}")
        else:
            print(f"ℹ️  No previous runs detected (first time)")

        # Test getting new ideas
        new_ideas = notion.get_new_ideas()
        print(f"✅ Change detection working! {len(new_ideas)} new ideas since last check")
        return True
    except Exception as e:
        print(f"❌ Change detection error: {e}")
        return False


def main():
    print("="*60)
    print("🧪 LinkedIn Agent Connection Test Suite")
    print("="*60)

    results = {
        "Notion": test_notion(),
        "Tavily": test_tavily(),
        "OpenRouter": test_openrouter(),
        "Change Detection": test_change_detection()
    }

    print("\n" + "="*60)
    print("📊 Test Results Summary")
    print("="*60)

    for name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")

    all_passed = all(results.values())

    print("\n" + "="*60)
    if all_passed:
        print("🎉 All tests passed! Your agent is ready to use.")
    else:
        print("⚠️  Some tests failed. Check your .env file and API keys.")
    print("="*60 + "\n")

    return all_passed


if __name__ == "__main__":
    main()
