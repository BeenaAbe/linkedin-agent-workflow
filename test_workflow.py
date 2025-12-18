"""End-to-end workflow test"""

import os
from dotenv import load_dotenv
from workflow import EnhancedLinkedInWorkflow

load_dotenv()


def test_full_workflow():
    """Test complete workflow with sample input"""
    print("\n" + "="*60)
    print("🧪 Testing Full Workflow (Research + Writing)")
    print("="*60 + "\n")

    # Sample input
    test_input = {
        "page_id": "test-123",
        "topic": "Why most AI agents are just fancy chatbots",
        "goal": "Thought Leadership",
        "context": "Lead with the 83% statistic. Target product managers."
    }

    print(f"📝 Topic: {test_input['topic']}")
    print(f"🎯 Goal: {test_input['goal']}")
    print(f"📋 Context: {test_input['context']}\n")

    try:
        # Run workflow
        workflow = EnhancedLinkedInWorkflow()
        result = workflow.run(test_input)

        # Validate output
        print("\n" + "="*60)
        print("✅ Workflow completed! Validating output...")
        print("="*60 + "\n")

        checks = []

        # Check 1: Research brief exists
        research_length = len(result.get("research_brief", ""))
        if research_length > 0:
            print(f"✅ Research brief generated ({research_length} chars)")
            checks.append(True)
        else:
            print(f"❌ No research brief")
            checks.append(False)

        # Check 2: 3 hooks
        hooks = result.get("hooks", [])
        if len(hooks) == 3:
            print(f"✅ All 3 hooks generated")
            for i, hook in enumerate(hooks, 1):
                print(f"   {i}. {hook[:60]}...")
            checks.append(True)
        else:
            print(f"❌ Only {len(hooks)} hooks (expected 3)")
            checks.append(False)

        # Check 3: Post body
        post_body = result.get("post_body", "")
        char_count = len(post_body)
        if 200 <= char_count <= 1500:
            print(f"✅ Post body valid ({char_count} chars)")
            checks.append(True)
        else:
            print(f"⚠️  Post body length: {char_count} chars (optimal: 800-1300)")
            checks.append(char_count > 0)

        # Check 4: Line breaks
        line_breaks = post_body.count('\n\n')
        if line_breaks >= 3:
            print(f"✅ Good formatting ({line_breaks} line breaks)")
            checks.append(True)
        else:
            print(f"⚠️  Only {line_breaks} line breaks (aim for 4+)")
            checks.append(True)  # Warning, not failure

        # Check 5: CTA
        cta = result.get("cta", "")
        if cta:
            print(f"✅ CTA: {cta}")
            checks.append(True)
        else:
            print(f"❌ No CTA")
            checks.append(False)

        # Check 6: Hashtags
        hashtags = result.get("hashtags", [])
        if 3 <= len(hashtags) <= 5:
            print(f"✅ Hashtags: {' '.join(hashtags)}")
            checks.append(True)
        else:
            print(f"⚠️  {len(hashtags)} hashtags (optimal: 3-5)")
            checks.append(len(hashtags) > 0)

        # Check 7: Visual suggestion
        visual = result.get("visual_format", "")
        if visual:
            print(f"✅ Visual format: {visual}")
            checks.append(True)
        else:
            print(f"❌ No visual suggestion")
            checks.append(False)

        # Check 8: Quality score
        quality_score = result.get("quality_score", 0)
        if quality_score >= 70:
            print(f"✅ Quality score: {quality_score}/100")
            checks.append(True)
        else:
            print(f"⚠️  Quality score: {quality_score}/100 (target: 70+)")
            checks.append(quality_score > 0)

        # Check 9: Content strategy
        strategy = result.get("content_strategy", {})
        if strategy and strategy.get("chosen_angle"):
            print(f"✅ Strategy: {strategy.get('chosen_angle', '')[:50]}...")
            checks.append(True)
        else:
            print(f"❌ No content strategy")
            checks.append(False)

        # Check 10: Workflow metadata
        workflow_id = result.get("workflow_id", "")
        duration = result.get("duration_minutes", 0)
        if workflow_id and duration > 0:
            print(f"✅ Workflow ID: {workflow_id}, Duration: {duration}min")
            checks.append(True)
        else:
            print(f"⚠️  Missing workflow metadata")
            checks.append(False)

        # Final score
        print("\n" + "="*60)
        passed = sum(checks)
        total = len(checks)
        percentage = (passed / total) * 100

        print(f"📊 Quality Score: {passed}/{total} checks passed ({percentage:.0f}%)")

        if percentage >= 85:
            print("🎉 Excellent! Workflow is working perfectly.")
        elif percentage >= 70:
            print("✅ Good! Minor improvements possible.")
        else:
            print("⚠️  Some issues detected. Review output above.")

        print("="*60 + "\n")

        # Show sample output
        print("📄 Sample Output:")
        print("-" * 60)
        print(f"\nHook 1: {hooks[0] if hooks else 'N/A'}")
        print(f"\nPost (first 200 chars):\n{post_body[:200]}...")
        print(f"\nCTA: {cta}")
        print(f"\nHashtags: {' '.join(hashtags)}")
        print("-" * 60)

        return percentage >= 70

    except Exception as e:
        print(f"\n❌ Workflow failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_full_workflow()
    exit(0 if success else 1)
