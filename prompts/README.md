# Prompt Engineering Guide

This directory contains the detailed prompt engineering documentation for the LinkedIn Content Engine agents.

## Agent Prompts

### 1. Research Agent ([research_agent.py](../agents/research_agent.py))

**Purpose**: Gather high-quality, relevant research for LinkedIn content

**Key Features**:
- Goal-specific research strategies (6 types)
- Source quality hierarchy (Tier 1-3)
- Structured JSON output with citations
- Contrarian angle detection
- Statistics validation (must include URLs + dates)

**Output**: Structured research brief with:
- Key insights (3-5)
- Statistics with sources
- Quotes with attribution
- Contrarian angles
- Pain points (for Product goal)
- Recommended focus

**Customization**: Edit lines 22-93 in `research_agent.py`

---

### 2. Writer Agent ([writer_agent.py](../agents/writer_agent.py))

**Purpose**: Generate high-performing LinkedIn posts from research

**Key Features**:
- 3 hook formulas (Controversial, Question, Story)
- Goal-specific CTAs
- Visual asset recommendations by goal type
- LinkedIn best practices enforcement
- Character limits and formatting rules
- Hashtag strategy (3-5 tags)

**Output**: Complete post package with:
- 3 hook options
- Post body (<1,500 chars)
- Call-to-action
- Hashtags (3-5)
- Visual asset suggestion
- Character count & read time

**Customization**: Edit lines 20-146 in `writer_agent.py`

---

## Prompt Customization Examples

### Example 1: Change Writing Style

To make posts more casual/conversational:

```python
# In writer_agent.py, add to system prompt:
**Writing Style:**
- Use contractions ("don't" not "do not")
- Ask rhetorical questions
- Use "..." for pauses
- Include "tbh", "honestly", "real talk" sparingly
```

### Example 2: Add Industry-Specific Research

To focus on B2B SaaS:

```python
# In research_agent.py, modify Thought Leadership section:
**Thought Leadership (B2B SaaS)**:
- Search for "SaaS metrics benchmarks" (ARR, CAC, LTV)
- Find pricing strategy debates (usage-based vs seat-based)
- Monitor SaaStr, ChartMogul, OpenView blogs
- Look for "SaaS [topic] 2024" trends
```

### Example 3: Adjust Hook Formulas

To add a "Data Hook" type:

```python
# In writer_agent.py, add 4th hook type:
**4. Data Hook:**
"X% of [audience] are doing [surprising behavior]. Here's why."
Example: "73% of product teams skip user research. Here's what they're missing."
```

### Example 4: Change Visual Preferences

To always suggest carousels:

```python
# In writer_agent.py, modify Visual Asset Logic:
## Visual Asset Logic (All Goals)

Default to **Carousel** unless specified:
- 5-10 slides
- 1:1 aspect ratio
- Title + Key Points + CTA slide
```

---

## Goal-Specific Customization

### Thought Leadership

**Current behavior**: Contrarian angles, data-driven, carousel visual

**To customize for "Hot Takes"**:
```python
# Research agent: Add this to Thought Leadership section
- Prioritize Reddit threads with 500+ upvotes
- Find Twitter debates with 1k+ replies
- Look for "[topic] is overrated" posts
```

### Product

**Current behavior**: Pain point focus, demo video/screenshot

**To customize for "Feature Launches"**:
```python
# Writer agent: Modify Product CTA
- **Product (Launch)**: "DM me for early access" OR "Waitlist link in bio"

# Add to visual section:
**Product Launch** → **Before/After Video**
- Show old painful workflow (10s)
- Show new feature solving it (20s)
- End with results/metrics (5s)
```

### Educational

**Current behavior**: Step-by-step guides, carousel

**To customize for "Mistake Roundups"**:
```python
# Research agent: Add to Educational section
- Search "[topic] mistakes" OR "things I wish I knew"
- Find "anti-patterns" in engineering blogs
- Look for "don't do this" posts

# Writer agent: Modify hook
**Mistake Hook (Educational):**
"I made [number] mistakes in [timeframe]. Here's what not to do."
```

---

## Temperature & Token Settings

### Current Settings

**Research Agent** ([research_agent.py:15-18](../agents/research_agent.py#L15-L18))
```python
temperature=0.3,  # Lower = more factual/consistent
max_tokens=2000   # Enough for detailed research
```

**Writer Agent** ([writer_agent.py:13-16](../agents/writer_agent.py#L13-L16))
```python
temperature=0.7,  # Higher = more creative/varied
max_tokens=3000   # Enough for long-form posts
```

### Recommended Adjustments

**For more creative/unpredictable content**:
```python
# Writer agent
temperature=0.9,  # More variety in hooks
```

**For highly consistent brand voice**:
```python
# Writer agent
temperature=0.4,  # Less variation
```

**For shorter posts**:
```python
# Writer agent
max_tokens=1500,  # Forces brevity
```

---

## Adding Few-Shot Examples

To improve output consistency, add examples to prompts:

### Example: Add Hook Examples

```python
# In writer_agent.py, add after Hook Formulas section:
## Example Hooks by Industry

**B2B SaaS:**
- "Hot take: Your free tier is why you can't raise a Series A."
- "Why do founders obsess over features when pricing is broken?"
- "I analyzed 500 SaaS landing pages. 90% make this mistake."

**AI/ML:**
- "Unpopular opinion: Most 'AI' is just if/else statements with extra steps."
- "What if your model's accuracy is hiding massive bias?"
- "I spent 6 months on an AI project that humans could do in 10 minutes."
```

### Example: Add Research Examples

```python
# In research_agent.py, add after Output Requirements section:
## Example Research Output

**Input**: Topic: "Product-led growth", Goal: "Thought Leadership"

**Output**:
{
  "key_insights": [
    "87% of PLG companies have a <$1k ACV, making enterprise sales difficult (OpenView 2024)",
    "Self-serve revenue hit a plateau at 60% for most PLG companies (ProfitWell)",
    "PLG products with usage-based pricing grow 38% faster than seat-based (ChartMogul)"
  ],
  "statistics": [
    {
      "stat": "PLG companies have 30% lower CAC than traditional SaaS",
      "source": "https://openviewpartners.com/plg-benchmarks-2024",
      "date": "2024-08"
    }
  ],
  "recommended_focus": "Lead with the '60% plateau' stat to challenge PLG hype, then show how hybrid models solve it."
}
```

---

## Testing Prompt Changes

### 1. Single Run Test

```bash
python main.py single
```

Check output quality in Notion "Draft Body" field.

### 2. A/B Test Hooks

Generate 2 posts with different prompts, post both, compare engagement after 48 hours.

### 3. Iterate on Temperature

Try 3 runs with different temperatures:
```python
# Run 1: temperature=0.5
# Run 2: temperature=0.7
# Run 3: temperature=0.9
```

Pick the temperature that produces the best mix of creativity + consistency.

---

## Prompt Debugging

### Issue: Research is too generic

**Fix**: Add specificity requirements
```python
# In research_agent.py quality standards:
- Insights must include specific numbers, not ranges ("42%" not "40-50%")
- Avoid phrases like "growing fast", "increasing popularity"
- Every claim must cite a Tier 1 or 2 source
```

### Issue: Posts are too long

**Fix**: Enforce stricter limits
```python
# In writer_agent.py constraints:
- Character limit: <1,000 characters (stricter)
- Maximum 3 bullet points (down from 5)
- Post body: 200-800 characters only
```

### Issue: Hooks are too similar

**Fix**: Add explicit differentiation
```python
# In writer_agent.py, modify Hook Formulas:
You MUST generate 3 DIFFERENT hooks:
1. Hook 1: Controversial (challenge a belief)
2. Hook 2: Question (ask "what if" or "why")
3. Hook 3: Story (personal anecdote with "I")

**DO NOT**:
- Reuse the same structure across hooks
- Start all 3 hooks with "Unpopular opinion"
- Use similar sentence patterns
```

### Issue: CTAs don't match goal

**Fix**: Add validation step
```python
# In writer_agent.py, add to Quality Checklist:
- [ ] CTA explicitly matches Goal:
  - Thought Leadership → Ask for opinions/debate
  - Product → Drive to link in comments
  - Educational → Ask which tip to try
```

---

## Advanced: Multi-Model Strategy

Use different models for different tasks:

```python
# Research Agent (accuracy matters)
from langchain_anthropic import ChatAnthropic
self.llm = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",  # Best reasoning
    temperature=0.2
)

# Writer Agent (creativity matters)
self.llm = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",  # Best writing
    temperature=0.8
)

# Alternative: Use Haiku for speed (research only)
self.llm = ChatAnthropic(
    model="claude-3-haiku-20240307",  # 10x cheaper
    temperature=0.3
)
```

**Cost comparison**:
- Sonnet: $3 per post (research + writing)
- Haiku (research) + Sonnet (writing): $1.50 per post

---

## Version Control for Prompts

Track prompt changes in git:

```bash
git log --oneline agents/research_agent.py
git diff HEAD~1 agents/writer_agent.py
```

Tag major prompt versions:
```bash
git tag -a prompt-v1.0 -m "Initial production prompts"
git tag -a prompt-v1.1 -m "Added B2B SaaS examples"
```

---

## Resources

- [Anthropic Prompt Engineering Guide](https://docs.anthropic.com/claude/docs/prompt-engineering)
- [LangChain Prompt Templates](https://python.langchain.com/docs/modules/model_io/prompts/)
- [LinkedIn Algorithm Best Practices](https://www.linkedin.com/business/marketing/blog/content-marketing/linkedin-algorithm)

---

## Need Help?

If you're unsure how to customize prompts:

1. **Check the original prompt files** in the root directory:
   - [system-prompt-researcher.md](../../system-prompt-researcher.md)
   - [system-prompt-writer.md](../../system-prompt-writer.md)

2. **Test incrementally**: Change one section at a time and run `python main.py single`

3. **Compare outputs**: Keep a log of prompt changes and their effect on quality
