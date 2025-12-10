"""Research Agent - Uses Tavily for web research and Claude for synthesis"""

from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from tavily import TavilyClient
import os
import json
import re


class ResearchAgent:
    """Agent responsible for researching topics and synthesizing insights"""

    def __init__(self):
        self.tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        self.llm = ChatOpenAI(
            model="anthropic/claude-3.5-sonnet",
            openai_api_key=os.getenv("OPENROUTER_API_KEY"),
            openai_api_base="https://openrouter.ai/api/v1",
            temperature=0.3,
            max_tokens=2000
        )

        self.synthesis_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a LinkedIn research assistant. Your job is to gather high-quality, relevant information for LinkedIn content.

## Context Handling (IMPORTANT)

**If user provides context with:**
- **Links/URLs**: Prioritize these as primary sources. Extract key insights from them first, then supplement with web search.
- **Rough notes/ideas**: Use these to guide research direction (e.g., "mention 83% stat", "target PMs", "contrarian angle").
- **Specific requirements**: Follow them precisely (e.g., "lead with X", "include quote from Y").

**If NO context provided:**
- Proceed with standard research using topic and goal type
- Conduct thorough web research to find best sources
- Follow the research logic below

## Research Logic by Goal Type

**Thought Leadership**: Establish authority through contrarian or data-backed insights
- Find 2-3 recent controversies or debates
- Search for academic papers or industry reports (ArXiv, Gartner)
- Identify contrarian viewpoints
- Extract 1-2 surprising statistics (prioritize last 6 months)
- Look for "everyone is wrong about X" angles

**Product**: Highlight pain points your product solves
- Search for competitor feature gaps and user complaints
- Find pain points from review sites (G2, Capterra)
- Monitor Reddit/Twitter for frustration posts
- Identify trending feature requests

**Educational**: Teach something actionable in 90 seconds
- Find authoritative step-by-step guides
- Identify common mistakes or misconceptions
- Search for case studies or real-world examples
- Look for visual frameworks or models

**Personal Brand**: Build relatability through vulnerability
- Find relatable stories or anecdotes
- Search for vulnerable/authentic takes
- Identify trending personal experiences
- Look for "lessons learned" or "what I wish I knew" posts

**Interactive**: Spark debate or engagement
- Find polarizing questions or debates
- Search for "hot takes" or controversial opinions
- Identify common dilemmas (X vs Y)

**Inspirational**: Motivate through success stories
- Find underdog success stories
- Search for quotes from respected figures
- Identify milestone achievements or breakthroughs

## Source Quality Hierarchy
**Tier 1 (Highest Priority):**
- Academic papers (ArXiv, Google Scholar)
- Industry reports (Gartner, Forrester, McKinsey)
- Government data (Census, BLS)
- Direct user feedback (Reddit, G2, Twitter)

**Tier 2:**
- Reputable news outlets (WSJ, NYT, Bloomberg)
- Industry blogs (a16z, First Round Review)

**Avoid:**
- Content farms, unverified claims, outdated data (>2 years)

## Output Requirements

Return structured research as JSON:
{{
  "key_insights": ["3-5 specific, actionable insights with stats/sources"],
  "statistics": [{{"stat": "X% of Y do Z", "source": "URL", "date": "YYYY-MM"}}],
  "quotes": [{{"quote": "...", "author": "Name & Title", "source": "URL", "context": "Why this matters"}}],
  "contrarian_angles": ["Angles that challenge conventional wisdom, backed by data"],
  "user_pain_points": ["Specific pain points (for Product goal only)"],
  "recommended_focus": "1-2 sentence suggestion on strongest angle based on research quality"
}}

## Quality Standards
- At least 2 high-quality sources (Tier 1 or 2)
- All statistics MUST include source URLs and dates
- Insights must be specific (avoid generic "AI is growing fast")
- Contrarian angles must be backed by data, not just opinion
- Prioritize recency (last 6 months preferred)
- Never invent statistics

## CRITICAL: URL Usage Rules
- ONLY use URLs that appear in the "Key Sources" section below
- DO NOT invent, guess, or create any URLs
- If a source doesn't have a URL, don't include it in citations
- Copy the exact URL as provided - do not modify or shorten
- If you reference a statistic, it MUST have a corresponding URL from the sources"""),
            ("user", """Topic: {topic}
Goal: {goal}
Context/Notes: {context}

Search Results:
{search_results}

**Instructions:**
1. If context contains URLs/links: Extract and summarize key points from those sources FIRST
2. If context has rough notes (e.g., "mention X stat", "target Y audience"): Use these as research priorities
3. If context is minimal or empty: Conduct standard research based on topic and goal
4. Supplement with search results to create comprehensive brief

Analyze and provide a structured research brief following the JSON format. Focus on the research logic for the "{goal}" goal type. Include specific URLs and dates for all statistics.""")
        ])

    def research(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute research workflow: search -> synthesize"""

        topic = state["topic"]
        goal = state["goal"]
        context = state.get("context", "")

        print(f"🔍 Researching: {topic}")

        # Step 1: Tavily search
        query = f"{topic} {goal} 2024"
        search_results = self.tavily.search(
            query=query,
            search_depth="advanced",
            max_results=5,
            include_answer=True
        )

        # Format search results with explicit URLs
        formatted_results = f"Summary: {search_results.get('answer', 'No summary available')}\n\n"
        formatted_results += "Key Sources (USE ONLY THESE URLs):\n"

        # Extract URLs for validation
        valid_urls = []
        for idx, result in enumerate(search_results.get('results', []), 1):
            url = result.get('url', '')
            title = result.get('title', 'No title')
            content = result.get('content', '')[:300]

            formatted_results += f"\n[Source {idx}]\n"
            formatted_results += f"Title: {title}\n"
            formatted_results += f"URL: {url}\n"
            formatted_results += f"Content: {content}...\n"

            if url:
                valid_urls.append(url)

        print(f"📊 Found {len(search_results.get('results', []))} sources with {len(valid_urls)} valid URLs")

        # Step 2: Claude synthesis
        chain = self.synthesis_prompt | self.llm
        response = chain.invoke({
            "topic": topic,
            "goal": goal,
            "context": context,
            "search_results": formatted_results
        })

        research_brief = response.content

        # Validate URLs in research brief (optional warning)
        self._validate_urls_in_brief(research_brief, valid_urls)

        print(f"✅ Research complete ({len(research_brief)} chars)")

        # Update state
        return {
            **state,
            "research_brief": research_brief,
            "search_results": formatted_results,
            "status": "researching"
        }

    def _validate_urls_in_brief(self, brief: str, valid_urls: list) -> None:
        """Check if research brief contains only valid URLs from Tavily"""
        # Extract all URLs from the brief
        url_pattern = r'https?://[^\s\"\'\}\],]+'
        found_urls = re.findall(url_pattern, brief)

        if not found_urls:
            print("⚠️  Warning: No URLs found in research brief")
            return

        # Check for invalid URLs
        invalid_urls = []
        for url in found_urls:
            # Clean URL (remove trailing punctuation)
            clean_url = url.rstrip('.,;:)')
            if clean_url not in valid_urls:
                invalid_urls.append(clean_url)

        if invalid_urls:
            print(f"⚠️  Warning: Found {len(invalid_urls)} potentially hallucinated URL(s):")
            for url in invalid_urls[:3]:  # Show first 3
                print(f"   - {url}")
        else:
            print(f"✅ All {len(found_urls)} URLs validated from Tavily sources")
