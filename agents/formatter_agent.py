"""Formatter Agent - Final polish, hashtags, and visual specifications"""

from typing import Dict, Any, List
import re


class FormatterAgent:
    """Agent responsible for final formatting and export-ready preparation"""

    # Hashtag strategy by content type
    HASHTAG_TEMPLATES = {
        "Thought Leadership": {
            "broad": ["#Leadership", "#Innovation", "#FutureOfWork"],
            "niche": ["#ProductThinking", "#ThoughtLeadership", "#StrategicThinking"]
        },
        "Product": {
            "broad": ["#SaaS", "#ProductivityTools", "#Technology"],
            "niche": ["#PLG", "#ProductLaunch", "#ProductManagement"]
        },
        "Personal Brand": {
            "broad": ["#Leadership", "#CareerAdvice", "#PersonalGrowth"],
            "niche": ["#CareerDevelopment", "#ProfessionalGrowth", "#WorkLifeBalance"]
        },
        "Educational": {
            "broad": ["#Marketing", "#Productivity", "#BusinessTips"],
            "niche": ["#MarketingTips", "#GrowthHacking", "#SkillDevelopment"]
        },
        "Interactive": {
            "broad": ["#LinkedInPoll", "#Discussion", "#TechIndustry"],
            "niche": ["#Debate", "#CommunityInput", "#IndustryInsights"]
        },
        "Inspirational": {
            "broad": ["#Motivation", "#Inspiration", "#Success"],
            "niche": ["#GrowthMindset", "#LeadershipDevelopment", "#Vulnerability"]
        }
    }

    # Visual format recommendations by goal type
    VISUAL_FORMATS = {
        "Thought Leadership": {
            "format": "carousel",
            "aspect_ratio": "1:1",
            "slides": "5-15",
            "suggestion": "Multi-slide carousel (PDF) with unique frameworks, trend breakdowns, or proprietary charts"
        },
        "Product": {
            "format": "video",
            "aspect_ratio": "1:1 or 4:5",
            "duration": "30-90 seconds",
            "suggestion": "Native video with subtitles showing 'Aha!' moment OR high-resolution screenshot/GIF with annotations"
        },
        "Personal Brand": {
            "format": "photo",
            "aspect_ratio": "1:1 or 4:5",
            "suggestion": "Candid, authentic photo related to story (behind-the-scenes, not corporate headshot)"
        },
        "Educational": {
            "format": "carousel",
            "aspect_ratio": "1:1",
            "slides": "3-7",
            "suggestion": "Step-by-step guide carousel or simple infographic summarizing tips"
        },
        "Interactive": {
            "format": "text-only",
            "suggestion": "Text-only post for immediate commenting OR contrarian quote card (1:1 aspect ratio)"
        },
        "Inspirational": {
            "format": "quote-card",
            "aspect_ratio": "1:1",
            "suggestion": "Quote card highlighting profound lesson on textured background OR behind-the-scenes photo"
        }
    }

    def finalize(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Apply final formatting and polish"""

        goal = state["goal"]
        post_body = state.get("post_body", "")
        topic = state.get("topic", "")

        print(f"✨ Formatter: Finalizing {goal} post...")

        # Generate hashtags
        hashtags = self._generate_hashtags(goal, topic, post_body)

        # Create visual asset specifications
        visual_specs = self._create_visual_specs(goal, state)

        # Calculate metrics
        character_count = len(post_body)
        word_count = len(post_body.split())
        estimated_read_time = self._estimate_read_time(word_count)

        # Generate first comment (if external links needed)
        first_comment = self._generate_first_comment(state)

        # Final formatting touches
        formatted_post = self._apply_formatting(post_body)

        print(f"✅ Formatter: Finalization complete")
        print(f"   Characters: {character_count}")
        print(f"   Read Time: {estimated_read_time}")
        print(f"   Hashtags: {len(hashtags)}")
        print(f"   Visual Format: {visual_specs.get('format', 'N/A')}")

        # Update state
        return {
            **state,
            "post_body": formatted_post,
            "hashtags": hashtags,
            "visual_specs": visual_specs,
            "visual_format": visual_specs.get("format", "text"),
            "visual_suggestion": visual_specs.get("suggestion", ""),
            "character_count": character_count,
            "word_count": word_count,
            "estimated_read_time": estimated_read_time,
            "first_comment": first_comment,
            "status": "formatting"
        }

    def _generate_hashtags(self, goal: str, topic: str, post_body: str) -> List[str]:
        """Generate 3-5 hashtags mixing broad and niche tags"""

        templates = self.HASHTAG_TEMPLATES.get(goal, self.HASHTAG_TEMPLATES["Educational"])

        # Start with template tags
        broad_tags = templates["broad"][:2]  # Take 2 broad tags
        niche_tags = templates["niche"][:2]  # Take 2 niche tags

        hashtags = broad_tags + niche_tags

        # Try to extract topic-specific hashtag
        topic_tag = self._create_topic_hashtag(topic)
        if topic_tag and topic_tag not in hashtags:
            hashtags.append(topic_tag)

        # Limit to 3-5 tags
        hashtags = hashtags[:5]

        # Ensure minimum 3 tags
        if len(hashtags) < 3:
            hashtags.extend(["#LinkedIn", "#Business", "#Professional"][:3 - len(hashtags)])

        return hashtags[:5]

    def _create_topic_hashtag(self, topic: str) -> str:
        """Create hashtag from topic"""

        # Remove common words
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}

        # Extract meaningful words
        words = re.findall(r'\w+', topic.lower())
        meaningful = [w.capitalize() for w in words if w not in stop_words and len(w) > 3]

        if not meaningful:
            return ""

        # Create hashtag (max 2-3 words)
        tag = "".join(meaningful[:3])

        # Limit length
        if len(tag) > 20:
            tag = "".join(meaningful[:2])

        return f"#{tag}" if tag else ""

    def _create_visual_specs(self, goal: str, state: Dict[str, Any]) -> Dict[str, Any]:
        """Create visual asset specifications"""

        template = self.VISUAL_FORMATS.get(goal, self.VISUAL_FORMATS["Educational"])

        visual_specs = {
            "format": template["format"],
            "aspect_ratio": template.get("aspect_ratio", "1:1"),
            "suggestion": template["suggestion"]
        }

        # Add format-specific details
        if template["format"] == "carousel":
            visual_specs["slides"] = template.get("slides", "5-10")
            visual_specs["carousel_outline"] = self._create_carousel_outline(state)

        elif template["format"] == "video":
            visual_specs["duration"] = template.get("duration", "30-60 seconds")
            visual_specs["video_script"] = self._create_video_script_outline(state)
            visual_specs["requires_subtitles"] = True

        elif template["format"] == "photo":
            visual_specs["style"] = "authentic, candid, behind-the-scenes"

        elif template["format"] == "quote-card":
            visual_specs["quote_text"] = self._extract_key_quote(state)

        # Add generation prompt for AI image tools
        visual_specs["generation_prompt"] = self._create_generation_prompt(goal, state)

        return visual_specs

    def _create_carousel_outline(self, state: Dict[str, Any]) -> List[str]:
        """Create carousel slide outline"""

        outline = state.get("outline", [])

        if not outline:
            return [
                "Cover: Post title",
                "Slide 2: Problem statement",
                "Slide 3: Key insight",
                "Slide 4: Supporting data",
                "Slide 5: Call to action"
            ]

        # Convert outline to slides
        slides = ["Cover: " + outline[0] if outline else "Cover"]
        slides.extend([f"Slide {i+2}: {section}" for i, section in enumerate(outline[1:6])])

        return slides

    def _create_video_script_outline(self, state: Dict[str, Any]) -> str:
        """Create basic video script outline"""

        hooks = state.get("hooks", [])
        key_points = state.get("content_strategy", {}).get("key_points", [])

        script = "Video Script Outline:\n\n"
        script += f"0-5s: {hooks[0] if hooks else 'Attention-grabbing opener'}\n"
        script += f"5-20s: Show the problem/pain point\n"
        script += f"20-45s: Demonstrate solution/feature\n"
        script += f"45-60s: Show result/outcome (Aha! moment)\n"
        script += f"60-90s: CTA and next steps\n"

        return script

    def _extract_key_quote(self, state: Dict[str, Any]) -> str:
        """Extract most impactful quote for quote card"""

        # Try to get from strategy
        supporting_data = state.get("content_strategy", {}).get("supporting_data", [])

        for item in supporting_data:
            if "quote" in item:
                return item["quote"]

        # Fallback: use chosen angle
        angle = state.get("content_strategy", {}).get("chosen_angle", "")
        if angle:
            return angle

        # Last resort: use topic
        return state.get("topic", "Your key insight here")

    def _create_generation_prompt(self, goal: str, state: Dict[str, Any]) -> str:
        """Create DALL-E/Midjourney prompt for visual generation"""

        topic = state.get("topic", "business topic")

        prompts = {
            "Thought Leadership": f"Professional, minimalist design for '{topic}' carousel. Clean typography, corporate blue and white color scheme, modern iconography, 1:1 aspect ratio",
            "Product": f"Clean product screenshot or demo for '{topic}'. Modern UI, bright interface, clear annotations, professional lighting, 1:1 or 4:5 aspect ratio",
            "Personal Brand": f"Candid, authentic photo related to '{topic}'. Natural lighting, behind-the-scenes feel, professional but approachable, 4:5 aspect ratio",
            "Educational": f"Infographic style for '{topic}'. Step-by-step visual guide, numbered sections, clean icons, easy to scan, 1:1 aspect ratio",
            "Interactive": f"Bold quote card for '{topic}'. Large text, contrarian statement, textured background, eye-catching typography, 1:1 aspect ratio",
            "Inspirational": f"Motivational quote card for '{topic}'. Inspiring imagery, elegant typography, warm colors, hopeful tone, 1:1 aspect ratio"
        }

        return prompts.get(goal, prompts["Educational"])

    def _generate_first_comment(self, state: Dict[str, Any]) -> str:
        """Generate first comment (for external links)"""

        # Check if context has URLs
        context = state.get("context", "")

        # Look for URLs in context
        url_pattern = r'https?://[^\s]+'
        urls = re.findall(url_pattern, context)

        if not urls:
            return ""

        # Create first comment with links
        comment = "🔗 Resources mentioned:\n\n"
        for i, url in enumerate(urls[:3], 1):  # Max 3 links
            comment += f"{i}. {url}\n"

        comment += "\nWhat questions do you have? Comment below!"

        return comment

    def _estimate_read_time(self, word_count: int) -> str:
        """Estimate read time based on word count"""

        # Average reading speed: 200-250 words per minute
        # LinkedIn skimming: ~150 words per minute
        reading_speed = 150

        minutes = word_count / reading_speed

        if minutes < 1:
            seconds = int(minutes * 60)
            return f"{seconds} seconds"
        else:
            return f"{int(minutes)} minute{'s' if minutes > 1 else ''}"

    def _apply_formatting(self, post_body: str) -> str:
        """Apply final formatting touches"""

        # Ensure consistent line breaks
        # Replace single newlines with double (except in lists)
        lines = post_body.split('\n')

        formatted_lines = []
        for i, line in enumerate(lines):
            formatted_lines.append(line)

            # Add double line break after non-empty lines (if not already there)
            if line.strip() and i < len(lines) - 1:
                next_line = lines[i + 1] if i + 1 < len(lines) else ""
                if next_line.strip():  # Next line is not empty
                    # Don't add extra break if it's a list item
                    if not (line.strip().startswith(('•', '-', '*', '1.', '2.', '3.'))):
                        formatted_lines.append("")

        return '\n'.join(formatted_lines)
