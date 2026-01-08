# Quality Issues Analysis & Fixes

## Reported Issues

1. **Posts are getting smaller** - Not meeting 800-1300 character target
2. **Hooks are very repetitive** - All 3 hooks sound similar
3. **Hooks are out of context** - Not relevant to the actual topic

## Root Causes

### Issue 1: Shorter Posts
- Editor Agent minimum thresholds may be too low for some goal types
- Current minimums: 200-800 chars depending on goal
- Should be: 800-1300 for most types (except Interactive)

### Issue 2: Repetitive Hooks
- **CRITICAL**: Editor Agent checks for 3 hooks but doesn't validate they use different formulas
- Writer prompt specifies 3 types (Controversial, Question, Story) but enforcement is missing
- No automated check for hook diversity

### Issue 3: Out of Context Hooks
- Research brief may not be reaching Writer Agent properly
- Research brief is truncated to 1500 chars (line 367 in writer_agent.py)
- May lose important context/insights

## Proposed Fixes

### Fix 1: Strengthen Minimum Character Counts

Update `QUALITY_THRESHOLDS` in `editor_agent.py`:

```python
QUALITY_THRESHOLDS = {
    "Thought Leadership": {
        "min_chars": 1000,  # Was 800
        "max_chars": 1500,
        "min_line_breaks": 4,
        "min_quality_score": 75
    },
    "Product": {
        "min_chars": 800,  # Was 500
        "max_chars": 1300,
        "min_line_breaks": 3,
        "min_quality_score": 70
    },
    "Educational": {
        "min_chars": 800,  # Was 400
        "max_chars": 1300,
        "min_line_breaks": 3,
        "min_quality_score": 75
    },
    # ... etc
}
```

### Fix 2: Add Hook Diversity Validation

Add to `_automated_quality_check()` in `editor_agent.py`:

```python
# Check hook diversity
def _check_hook_diversity(self, hooks: list) -> tuple[bool, str]:
    """Check if hooks use different formulas"""
    if len(hooks) < 3:
        return False, "Need 3 hooks"

    # Check for formula patterns
    controversial_pattern = r"unpopular opinion|hot take|controversial"
    question_pattern = r"what if|why do|why does|how many"
    story_pattern = r"I \w+|Last \w+|Yesterday|A few \w+ ago"

    has_controversial = any(re.search(controversial_pattern, hook, re.I) for hook in hooks)
    has_question = any(re.search(question_pattern, hook, re.I) for hook in hooks)
    has_story = any(re.search(story_pattern, hook, re.I) for hook in hooks)

    diversity_count = sum([has_controversial, has_question, has_story])

    if diversity_count < 3:
        return False, f"Hooks use only {diversity_count}/3 formula types. Need: Controversial, Question, Story"

    return True, "Hook diversity OK"
```

Then in `_automated_quality_check()`:

```python
# Check 3: Hook Diversity
is_diverse, diversity_msg = self._check_hook_diversity(hooks)
if not is_diverse:
    score -= 20
    feedback.append(diversity_msg)
```

### Fix 3: Increase Research Brief Limit

In `writer_agent.py` line 367:

```python
# Change from:
"research_brief": research_brief[:1500]

# To:
"research_brief": research_brief[:3000]  # Double the context
```

### Fix 4: Add Explicit Hook Instructions to Writer Revision

When Editor sends feedback for revision, explicitly remind about hook formulas:

```python
if "hook" in feedback_context.lower() or "repetitive" in feedback_context.lower():
    feedback_context += "\n\nREMINDER: Generate 3 DIFFERENT hook types:\n"
    feedback_context += "1. Controversial: 'Unpopular opinion: [bold claim]'\n"
    feedback_context += "2. Question: 'What if [provocative hypothetical]?'\n"
    feedback_context += "3. Story: 'I [mistake/discovery] that [outcome]'\n"
```

## Implementation Priority

1. **HIGH**: Fix 2 (Hook Diversity Validation) - Addresses repetitive hooks
2. **HIGH**: Fix 3 (Research Brief Limit) - Addresses context relevance
3. **MEDIUM**: Fix 1 (Character Counts) - Addresses post length
4. **LOW**: Fix 4 (Explicit Reminders) - Nice to have

## Testing Plan

After implementing fixes, test with:

1. Same topic, run 3 times - verify hooks are different each time
2. Complex topic with stats - verify research brief data is used
3. Various goal types - verify minimum character counts are met
4. Check editor feedback - verify it catches hook issues

## Additional Recommendations

1. Add logging to see actual research brief length being passed
2. Monitor revision cycles - if >2 revisions common, prompts need work
3. Consider adding example hooks for each formula type in Writer prompt
4. Add telemetry to track average post length by goal type
