"""Strategist Agent - Creates content strategy and outline from research"""

from typing import Dict, Any
import json
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os


class StrategistAgent:
    """Agent responsible for analyzing research and creating content strategy"""

    def __init__(self):
        self.llm = ChatOpenAI(
            model="anthropic/claude-3.5-sonnet",
            openai_api_key=os.getenv("OPENROUTER_API_KEY"),
            openai_api_base="https://openrouter.ai/api/v1",
            temperature=0.4,  # Slightly lower for more focused strategy
            max_tokens=2000
        )

        self.strategy_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert LinkedIn content strategist. Your job is to analyze research and create a winning content strategy.

## Your Responsibilities

1. **Analyze Research Quality**
   - Identify strongest insights, statistics, and angles
   - Assess credibility of sources
   - Find gaps or weak points

2. **Select Best Angle**
   - Choose the most compelling angle based on goal type
   - Prioritize data-backed or contrarian perspectives
   - Consider target audience appeal

3. **Create Content Outline**
   - Structure: Hook → Problem/Context → Solution/Insight → CTA
   - Adapt structure to content type
   - Identify key points for each section

4. **Recommend Structure Type**
   - Story arc (personal narrative)
   - Framework (numbered steps, bullet points)
   - Contrarian argument (thesis + supporting points)
   - Case study (problem → solution → results)

## Strategy Logic by Goal Type

**Thought Leadership:**
- Angle: Contrarian or data-backed unique perspective
- Structure: Hook → Current Belief → Contrarian Thesis → 3 Supporting Points → CTA
- Length: 1500+ characters (deep dive)
- Focus: Establish authority, spark debate

**Product:**
- Angle: ONE clear value proposition (save time, increase revenue, reduce friction)
- Structure: Hook → Problem → Feature Name → Benefit (bullets) → Social Proof → CTA
- Length: 800-1300 characters
- Focus: Benefits over features

**Educational:**
- Angle: Solve a small, specific problem in 3-5 steps
- Structure: Hook (promise result) → Numbered Steps → Brief "Why" for each → CTA
- Length: 600-1200 characters
- Focus: Actionable, scannable

**Personal Brand:**
- Angle: Vulnerable story with professional takeaway
- Structure: Hook (in media res) → Struggle → Turning Point → Resolution → Lesson → CTA
- Length: 600-1000 characters
- Focus: Emotional connection, relatability

**Interactive:**
- Angle: Polarizing or highly relatable topic
- Structure: Hook → Brief Setup → Open-Ended Question → CTA (comment below)
- Length: 300-600 characters
- Focus: Maximize comments, easy to answer

**Inspirational:**
- Angle: Breakthrough moment or profound lesson
- Structure: Hook (pain point) → Turning Point → Resolution → Lesson → Reflective CTA
- Length: 600-1000 characters
- Focus: Motivation, hope, values

## Output Format (JSON)

Return ONLY valid JSON in this structure:

{{
  "chosen_angle": "One-sentence description of the unique angle",
  "outline": [
    "Hook concept (attention-grabbing opener)",
    "Section 1: Problem/Context",
    "Section 2: Solution/Insight",
    "Section 3: Supporting Point (if applicable)",
    "CTA concept"
  ],
  "structure_type": "story|framework|argument|case_study",
  "key_points": [
    "Point 1: Specific insight with data",
    "Point 2: Another key insight",
    "Point 3: Final supporting point"
  ],
  "supporting_data": [
    {{"stat": "83% of AI agents are chatbots", "source": "URL", "usage": "Lead with this in hook"}},
    {{"quote": "...", "author": "Name", "usage": "Use in section 2"}}
  ],
  "recommended_focus": "1-2 sentence suggestion on what to emphasize",
  "target_length": "600-1000 characters",
  "hook_approach": "controversial|question|story"
}}

## Quality Standards

- Angle must be specific and defensible
- Outline must match goal type structure
- Key points must be backed by research data
- Supporting data must include actual sources from research
- No invented statistics or sources"""),
            ("user", """Topic: {topic}
Goal: {goal}
Context: {context}

Research Brief:
{research_brief}

Analyze the research and create a comprehensive content strategy for this {goal} post. Focus on selecting the strongest angle and creating a clear outline that will result in a high-performing LinkedIn post.""")
        ])

    def create_strategy(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate content strategy from research"""

        topic = state["topic"]
        goal = state["goal"]
        context = state.get("context", "")
        research_brief = state.get("research_brief", "")

        print(f"🎯 Strategist: Analyzing research for {goal} post...")

        if not research_brief:
            print("⚠️  Strategist: No research brief available, creating basic strategy")
            return self._create_fallback_strategy(state)

        # Generate strategy
        chain = self.strategy_prompt | self.llm
        response = chain.invoke({
            "topic": topic,
            "goal": goal,
            "context": context,
            "research_brief": research_brief[:2000]  # Limit to avoid token overflow
        })

        # Parse JSON response
        content = response.content.strip()
        # Remove markdown code blocks if present
        content = content.replace("```json\n", "").replace("```json", "").replace("\n```", "").replace("```", "")

        try:
            strategy = json.loads(content)
        except json.JSONDecodeError as e:
            print(f"⚠️  Strategist: JSON parse error: {e}")
            print(f"⚠️  Raw response: {content[:200]}...")
            return self._create_fallback_strategy(state)

        # Validate strategy
        required_keys = ["chosen_angle", "outline", "key_points"]
        if not all(k in strategy for k in required_keys):
            print(f"⚠️  Strategist: Missing required keys in strategy")
            return self._create_fallback_strategy(state)

        print(f"✅ Strategist: Strategy created")
        print(f"   Angle: {strategy['chosen_angle'][:60]}...")
        print(f"   Outline: {len(strategy['outline'])} sections")
        print(f"   Key Points: {len(strategy['key_points'])}")

        # Update state
        return {
            **state,
            "content_strategy": strategy,
            "outline": strategy.get("outline", []),
            "status": "strategizing"
        }

    def _create_fallback_strategy(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Create basic strategy when LLM fails or no research available"""

        goal = state["goal"]
        topic = state["topic"]

        # Basic outline templates
        outlines = {
            "Thought Leadership": [
                "Hook: Controversial statement about " + topic,
                "Current belief/problem",
                "Contrarian thesis",
                "3 supporting points",
                "CTA: What's your take?"
            ],
            "Product": [
                "Hook: Pain point related to " + topic,
                "Problem description",
                "Feature introduction",
                "Benefit bullets",
                "CTA: Try it now"
            ],
            "Educational": [
                "Hook: Promise result",
                "Step 1",
                "Step 2",
                "Step 3",
                "CTA: Try and report back"
            ],
            "Personal Brand": [
                "Hook: In media res",
                "Struggle/challenge",
                "Turning point",
                "Resolution/lesson",
                "CTA: Share your story"
            ],
            "Interactive": [
                "Hook: Question setup",
                "Brief context",
                "Open-ended question",
                "CTA: Comment below"
            ],
            "Inspirational": [
                "Hook: Painful moment",
                "Turning point",
                "Lesson learned",
                "CTA: Tag someone"
            ]
        }

        fallback_strategy = {
            "chosen_angle": f"Compelling perspective on {topic}",
            "outline": outlines.get(goal, outlines["Educational"]),
            "structure_type": "framework",
            "key_points": [
                "Point about " + topic,
                "Supporting insight",
                "Actionable takeaway"
            ],
            "supporting_data": [],
            "recommended_focus": f"Focus on delivering value for {goal} audience",
            "target_length": "800-1300 characters",
            "hook_approach": "question"
        }

        print(f"✅ Strategist: Fallback strategy created")

        return {
            **state,
            "content_strategy": fallback_strategy,
            "outline": fallback_strategy["outline"],
            "status": "strategizing"
        }
