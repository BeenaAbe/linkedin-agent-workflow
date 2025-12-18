"""Editor Agent - Quality checks, style enforcement, and revision logic"""

from typing import Dict, Any
import re
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os


class EditorAgent:
    """Agent responsible for reviewing draft quality and enforcing style rules"""

    # Forbidden corporate jargon
    FORBIDDEN_JARGON = [
        "synergy", "leverage", "circle back", "alignment", "bandwidth",
        "touch base", "move the needle", "low-hanging fruit", "paradigm shift",
        "thinking outside the box", "win-win", "game changer", "best of breed"
    ]

    # Passive voice indicators
    PASSIVE_VOICE_PATTERNS = [
        r'\bis\s+\w+ed\b',  # is created, is managed
        r'\bwas\s+\w+ed\b',  # was designed
        r'\bare\s+\w+ed\b',  # are implemented
        r'\bwere\s+\w+ed\b',  # were developed
        r'\bbeen\s+\w+ed\b'  # has been launched
    ]

    # Quality thresholds by content type
    QUALITY_THRESHOLDS = {
        "Thought Leadership": {
            "min_chars": 800,
            "max_chars": 1500,
            "min_line_breaks": 4,
            "min_quality_score": 75
        },
        "Product": {
            "min_chars": 500,
            "max_chars": 1300,
            "min_line_breaks": 3,
            "min_quality_score": 70
        },
        "Educational": {
            "min_chars": 400,
            "max_chars": 1200,
            "min_line_breaks": 3,
            "min_quality_score": 75
        },
        "Personal Brand": {
            "min_chars": 400,
            "max_chars": 1000,
            "min_line_breaks": 4,
            "min_quality_score": 70
        },
        "Interactive": {
            "min_chars": 200,
            "max_chars": 600,
            "min_line_breaks": 2,
            "min_quality_score": 65
        },
        "Inspirational": {
            "min_chars": 400,
            "max_chars": 1000,
            "min_line_breaks": 4,
            "min_quality_score": 70
        }
    }

    def __init__(self):
        self.llm = ChatOpenAI(
            model="anthropic/claude-3.5-sonnet",
            openai_api_key=os.getenv("OPENROUTER_API_KEY"),
            openai_api_base="https://openrouter.ai/api/v1",
            temperature=0.2,  # Low temperature for consistent editing
            max_tokens=1500
        )

        self.review_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert LinkedIn content editor. Your job is to review drafts for quality, style, and effectiveness.

## Review Criteria

**Content Quality:**
- Hook strength: Is the opening compelling enough to stop scrolling?
- Clarity: Is the message clear and easy to understand?
- Value: Does it provide genuine insight or actionable advice?
- Flow: Does the post have logical progression?

**Style & Voice:**
- Active voice (avoid passive constructions)
- No corporate jargon ("synergy," "leverage," "circle back")
- Conversational tone (not stiff or formal)
- Short, punchy sentences mixed with longer explanations

**LinkedIn Best Practices:**
- Line breaks every 2-3 sentences for mobile readability
- No walls of text
- CTA is clear and matches content goal
- Statistics are specific (not vague)

**Goal-Specific Checks:**

Thought Leadership: Contrarian or data-backed? Establishes authority?
Product: Clear value proposition? Benefits over features?
Educational: Actionable steps? Easy to scan?
Personal Brand: Vulnerable yet professional? Relatable story?
Interactive: Provocative question? Easy to answer?
Inspirational: Emotional arc? Hopeful tone?

## Review Output

Provide a brief assessment (2-3 sentences) covering:
1. What works well
2. What needs improvement (if anything)
3. Recommendation: APPROVE or REVISE (with specific fix)

Be constructive but honest. If the draft is strong, approve it. If it has issues, suggest ONE specific improvement."""),
            ("user", """Goal: {goal}
Topic: {topic}

Draft Post:
{post_body}

Hooks:
{hooks}

CTA: {cta}

Please review this draft and provide your assessment.""")
        ])

    def review(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Review and potentially edit draft"""

        goal = state["goal"]
        post_body = state.get("post_body", "")
        hooks = state.get("hooks", [])
        cta = state.get("cta", "")
        topic = state.get("topic", "")

        print(f"📝 Editor: Reviewing {goal} draft...")

        # Run automated quality checks
        auto_score, auto_feedback = self._automated_quality_check(state)

        print(f"   Automated score: {auto_score}/100")

        # Get LLM review
        llm_feedback = self._llm_review(goal, topic, post_body, hooks, cta)

        # Combine scores
        quality_score = auto_score

        # Determine if revisions needed
        revision_count = state.get("revision_count", 0)
        threshold = self.QUALITY_THRESHOLDS.get(goal, {}).get("min_quality_score", 70)

        # Decision logic
        if quality_score >= threshold:
            decision = "approve"
            print(f"✅ Editor: Draft approved (score: {quality_score})")
        elif revision_count >= 2:
            decision = "approve"  # Max revisions reached, accept anyway
            print(f"⚠️  Editor: Max revisions reached, approving (score: {quality_score})")
        else:
            decision = "revise"
            print(f"⚠️  Editor: Requesting revision (score: {quality_score})")

        # Compile feedback
        editor_feedback = self._compile_feedback(auto_feedback, llm_feedback)

        # Update state
        return {
            **state,
            "quality_score": quality_score,
            "editor_feedback": editor_feedback,
            "editor_decision": decision,
            "revision_count": revision_count + (1 if decision == "revise" else 0),
            "status": "editing"
        }

    def _automated_quality_check(self, state: Dict[str, Any]) -> tuple[int, list]:
        """Run rule-based quality checks"""

        goal = state["goal"]
        post_body = state.get("post_body", "")
        hooks = state.get("hooks", [])
        cta = state.get("cta", "")
        hashtags = state.get("hashtags", [])

        feedback = []
        score = 100  # Start at 100, deduct for issues

        thresholds = self.QUALITY_THRESHOLDS.get(goal, self.QUALITY_THRESHOLDS["Educational"])

        # Check 1: Character count
        char_count = len(post_body)
        if char_count < thresholds["min_chars"]:
            score -= 15
            feedback.append(f"Post too short ({char_count} chars, need {thresholds['min_chars']}+)")
        elif char_count > thresholds["max_chars"]:
            score -= 10
            feedback.append(f"Post too long ({char_count} chars, max {thresholds['max_chars']})")

        # Check 2: Line breaks
        line_breaks = post_body.count('\n\n')
        if line_breaks < thresholds["min_line_breaks"]:
            score -= 10
            feedback.append(f"Insufficient line breaks ({line_breaks}, need {thresholds['min_line_breaks']}+)")

        # Check 3: Hooks
        if len(hooks) < 3:
            score -= 15
            feedback.append(f"Missing hooks (found {len(hooks)}, need 3)")

        # Check 4: CTA
        if not cta or len(cta) < 10:
            score -= 10
            feedback.append("Missing or weak CTA")

        # Check 5: Hashtags
        hashtag_count = len(hashtags)
        if hashtag_count < 3 or hashtag_count > 5:
            score -= 5
            feedback.append(f"Hashtag count off (found {hashtag_count}, need 3-5)")

        # Check 6: Jargon detection
        jargon_found = self._detect_jargon(post_body)
        if jargon_found:
            score -= 10
            feedback.append(f"Corporate jargon detected: {', '.join(jargon_found[:3])}")

        # Check 7: Passive voice
        passive_count = self._count_passive_voice(post_body)
        if passive_count > 2:
            score -= 8
            feedback.append(f"Excessive passive voice ({passive_count} instances)")

        # Check 8: Paragraph length
        long_paragraphs = self._check_paragraph_length(post_body)
        if long_paragraphs > 0:
            score -= 7
            feedback.append(f"Walls of text detected ({long_paragraphs} long paragraphs)")

        # Check 9: Statistics verification
        if not self._has_statistics(post_body) and goal == "Thought Leadership":
            score -= 5
            feedback.append("Missing data/statistics for Thought Leadership post")

        # Ensure score doesn't go below 0
        score = max(0, score)

        return score, feedback

    def _llm_review(self, goal: str, topic: str, post_body: str, hooks: list, cta: str) -> str:
        """Get LLM-based qualitative review"""

        try:
            chain = self.review_prompt | self.llm
            response = chain.invoke({
                "goal": goal,
                "topic": topic,
                "post_body": post_body,
                "hooks": "\n".join(hooks) if hooks else "No hooks provided",
                "cta": cta
            })

            return response.content.strip()

        except Exception as e:
            print(f"⚠️  Editor: LLM review failed: {e}")
            return "LLM review unavailable"

    def _detect_jargon(self, text: str) -> list:
        """Detect forbidden corporate jargon"""

        text_lower = text.lower()
        found = []

        for jargon in self.FORBIDDEN_JARGON:
            if jargon in text_lower:
                found.append(jargon)

        return found

    def _count_passive_voice(self, text: str) -> int:
        """Count passive voice instances"""

        count = 0
        for pattern in self.PASSIVE_VOICE_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            count += len(matches)

        return count

    def _check_paragraph_length(self, text: str) -> int:
        """Check for overly long paragraphs"""

        paragraphs = text.split('\n\n')
        long_count = 0

        for para in paragraphs:
            sentences = para.count('.') + para.count('!') + para.count('?')
            # More than 3 sentences in a paragraph = wall of text
            if sentences > 3:
                long_count += 1

        return long_count

    def _has_statistics(self, text: str) -> bool:
        """Check if post contains statistics"""

        # Look for patterns like "83%", "5x", "$1M", "2,000"
        stat_patterns = [
            r'\d+%',  # Percentages
            r'\d+x',  # Multipliers
            r'\$\d+',  # Money
            r'\d{1,3}(,\d{3})+',  # Large numbers with commas
        ]

        for pattern in stat_patterns:
            if re.search(pattern, text):
                return True

        return False

    def _compile_feedback(self, auto_feedback: list, llm_feedback: str) -> str:
        """Compile all feedback into single message"""

        feedback_parts = []

        if auto_feedback:
            feedback_parts.append("Automated checks:")
            for item in auto_feedback:
                feedback_parts.append(f"  - {item}")

        if llm_feedback and llm_feedback != "LLM review unavailable":
            feedback_parts.append(f"\nEditorial review:\n{llm_feedback}")

        return "\n".join(feedback_parts) if feedback_parts else "No issues found"
