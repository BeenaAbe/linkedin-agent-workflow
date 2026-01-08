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
        """Create detailed AI image generation prompt for DALL-E/Midjourney/Stable Diffusion

        This generates a comprehensive prompt that includes:
        - Visual style and composition
        - Color palette and mood
        - Typography and design elements
        - Technical specifications
        - Quality modifiers for better AI output
        """

        topic = state.get("topic", "business topic")
        hooks = state.get("hooks", [""])
        hook_preview = hooks[0][:100] if hooks else ""

        prompts = {
            "Thought Leadership": (
                f"Create a professional LinkedIn carousel cover slide about '{topic}'. "
                f"VISUAL STYLE: Clean, modern, minimalist corporate design. "
                f"LAYOUT: Centered composition with clear hierarchy. Large, bold sans-serif heading text at top third. "
                f"Subtle geometric patterns or abstract shapes in background (lines, gradients, or soft shapes). "
                f"COLOR PALETTE: Professional blues (#0077B5 LinkedIn blue, #00A0DC light blue) with white/off-white (#F3F6F8) background. "
                f"Accent colors: Navy blue (#004182) for depth, light gray (#E1E9EE) for subtle elements. "
                f"TYPOGRAPHY: Modern sans-serif font (Helvetica, Inter, or similar). Title in 72-96pt bold, subtitle in 36-48pt regular. "
                f"ELEMENTS: Minimal iconography related to {topic} - max 1-2 simple line icons. Thin divider lines or subtle frames. "
                f"MOOD: Authoritative, trustworthy, professional, forward-thinking. "
                f"TECHNICAL: 1080x1080px, 1:1 aspect ratio, high contrast for mobile readability, 20% margin on all sides. "
                f"STYLE KEYWORDS: Corporate, B2B, executive, thought leader, professional photography aesthetic, clean UI design, "
                f"Behance quality, dribbble inspiration. "
                f"AVOID: Cheesy stock photos, cluttered layouts, too many colors, Comic Sans or decorative fonts."
            ),

            "Product": (
                f"Create a professional product showcase image for '{topic}'. "
                f"VISUAL STYLE: Modern SaaS interface design, clean product demo aesthetic. "
                f"LAYOUT: Center the main product interface/feature. Use 3D perspective or subtle shadow for depth. "
                f"Include annotation arrows or callout boxes highlighting key features (max 2-3 annotations). "
                f"COLOR PALETTE: Bright, vibrant interface colors - primary brand color (suggest #667EEA purple or #48BB78 green), "
                f"white background (#FFFFFF), subtle gray UI elements (#F7FAFC, #E2E8F0). Use high contrast for CTAs. "
                f"TYPOGRAPHY: Modern product UI font (SF Pro, Roboto, Inter). Labels in 24-32pt, annotations in 18-24pt. "
                f"ELEMENTS: Product screenshot or mockup, UI elements (buttons, inputs, cards), subtle drop shadows, "
                f"glowing highlights on key features, cursor hover states, smooth rounded corners (8-16px radius). "
                f"MOOD: Exciting, innovative, user-friendly, 'aha moment' feeling. "
                f"TECHNICAL: 1080x1350px (4:5 ratio) or 1080x1080px (1:1), crisp rendering, high DPI (2x resolution), "
                f"clear visual hierarchy. "
                f"STYLE KEYWORDS: Product Hunt featured, ProductLed aesthetic, B2B SaaS, modern web app, "
                f"iOS/Material Design inspired, glass morphism effects, micro-interactions suggested. "
                f"AVOID: Outdated UI patterns, low contrast text, overly complex interfaces, generic stock photos."
            ),

            "Personal Brand": (
                f"Create an authentic, professional photo related to '{topic}'. "
                f"VISUAL STYLE: Candid documentary photography, natural and approachable, behind-the-scenes authenticity. "
                f"COMPOSITION: Rule of thirds, subject in natural environment (office, coffee shop, workspace, outdoor professional setting). "
                f"Environmental context that tells a story about {topic}. Shallow depth of field (f/2.8-f/4) with subject in focus. "
                f"LIGHTING: Natural window light or soft golden hour lighting. Avoid harsh shadows. "
                f"Warm, inviting tone with slight backlight for dimension. "
                f"COLOR PALETTE: Natural, warm tones - golden hour warmth, earth tones, authentic environment colors. "
                f"Slightly desaturated for professional feel but not black & white. "
                f"SUBJECT: Professional but casual attire, genuine expression (thoughtful, engaged, or mid-action), "
                f"authentic moment not posed headshot. "
                f"MOOD: Approachable, authentic, relatable, human, trustworthy, inspirational without being cheesy. "
                f"TECHNICAL: 1080x1350px (4:5 portrait ratio), high quality portrait photography, slight film grain for authenticity. "
                f"STYLE KEYWORDS: Brandon Stanton humans of style, documentary photography, environmental portrait, "
                f"Gary Vee authenticity, lifestyle business photography, Forbes contributor aesthetic. "
                f"AVOID: Corporate headshot, overly posed, fake office stock photos, cheesy hand gestures, clipart style."
            ),

            "Educational": (
                f"Create an educational infographic about '{topic}'. "
                f"VISUAL STYLE: Clear, scannable, step-by-step visual guide with strong information hierarchy. "
                f"LAYOUT: Vertical or grid layout with numbered sections (3-5 steps max). Each section has icon + title + brief text. "
                f"Left-aligned or centered alignment for easy reading. Clear visual flow with arrows or connecting elements. "
                f"COLOR PALETTE: Educational and approachable - primary color (suggest #3182CE blue or #38B2AC teal), "
                f"secondary accent (#F6AD55 orange), neutral background (#FAFAFA light gray), dark text (#2D3748). "
                f"Use color coding for different sections/categories. "
                f"TYPOGRAPHY: Highly legible sans-serif (Open Sans, Lato, Nunito). Headers 48-64pt bold, body text 24-32pt regular. "
                f"Number badges in 36-48pt. Consistent spacing and alignment. "
                f"ELEMENTS: Simple line icons (Feather, Heroicons style) for each step, numbered badges or circles, "
                f"subtle divider lines, small charts or progress indicators, checkmarks or bullets for sub-points. "
                f"MOOD: Friendly, accessible, confidence-building, 'you can do this' energy. "
                f"TECHNICAL: 1080x1080px (1:1 square), high contrast for mobile, sufficient whitespace (40px+ margins), "
                f"scalable text sizes. "
                f"STYLE KEYWORDS: Venngage style, Canva educational template, Skillshare aesthetic, course material design, "
                f"how-to guide, process visualization, explainer graphics. "
                f"AVOID: Wall of text, too many elements, low contrast, decorative fonts, childish clipart."
            ),

            "Interactive": (
                f"Create a bold, contrarian quote card for '{topic}'. "
                f"CONTENT: Feature an engaging question or controversial statement related to '{topic}'. "
                f"{'Use this hook: ' + hook_preview if hook_preview else 'Create a thought-provoking question that challenges common assumptions.'} "
                f"VISUAL STYLE: Bold, conversation-starting, pattern interrupt design that stops the scroll. "
                f"LAYOUT: Text-dominant design with question/statement taking 60-70% of space. Large, impactful typography. "
                f"Quote marks optional. Author attribution minimal or absent. "
                f"COLOR PALETTE: High contrast and bold - dark background (#1A202C charcoal or #2D3748 gray) with bright text, "
                f"OR vibrant gradient background (suggest purple-pink, blue-green, or orange-red gradients). "
                f"Accent color for emphasis (#F6E05E yellow, #FC8181 coral). "
                f"TYPOGRAPHY: Extra bold, statement-making font (Montserrat Black, Bebas Neue, Poppins Bold). "
                f"Main text 64-96pt, very thick weight (800-900). High contrast with background. "
                f"TEXTURE: Subtle textured background (grainy, concrete, watercolor, or gradient noise), "
                f"geometric patterns, or abstract shapes for visual interest. "
                f"MOOD: Provocative, discussion-worthy, makes you stop and think, slightly edgy or contrarian. "
                f"TECHNICAL: 1080x1080px (1:1 square), extremely high contrast for visibility, optimized for quick comprehension. "
                f"STYLE KEYWORDS: Gary Vee quote card, controversial take, pattern interrupt, scroll-stopper, "
                f"debate starter, LinkedIn poll aesthetic, discussion prompt. "
                f"AVOID: Safe/bland statements, low contrast, too much text, decorative fonts, generic motivational vibes."
            ),

            "Inspirational": (
                f"Create an inspiring quote card or motivational image for '{topic}'. "
                f"VISUAL STYLE: Uplifting, aspirational, emotionally resonant with professional polish. "
                f"LAYOUT: Centered quote text with elegant framing. Optional subtle imagery in background (nature, skyline, abstract). "
                f"Text should be primary focus with background enhancing not competing. "
                f"COLOR PALETTE: Warm and hopeful - sunrise oranges/golds (#F6AD55, #ED8936), calming blues (#4299E1), "
                f"soft purples (#9F7AEA), or earthy greens (#48BB78). White or light overlay for text legibility. "
                f"Gradient skies or soft bokeh effects. "
                f"TYPOGRAPHY: Elegant serif for quotes (Playfair Display, Merriweather) or strong sans-serif (Montserrat, Raleway). "
                f"Quote text 48-72pt, author attribution 24-32pt. Letter spacing for elegance. "
                f"IMAGERY: If using background - mountain peaks, ocean horizons, city skylines, workspace victory moments, "
                f"sunrise/sunset, abstract light rays, or textured overlays (watercolor, brush strokes). "
                f"MOOD: Hopeful, empowering, growth-minded, vulnerable yet strong, inspiring without toxic positivity. "
                f"TECHNICAL: 1080x1080px (1:1 square), text overlay with sufficient contrast (use dark overlay on bright images), "
                f"high emotional impact. "
                f"STYLE KEYWORDS: Brené Brown aesthetic, Simon Sinek inspiration, TED talk vibes, personal growth content, "
                f"leadership development, authentic motivation, Jay Shetty visual style. "
                f"AVOID: Cheesy sunset clichés, overused quotes, toxic positivity, generic corporate motivation, Comic Sans."
            )
        }

        base_prompt = prompts.get(goal, prompts["Educational"])

        # Add quality enhancement suffix for all prompts
        quality_suffix = (
            " HIGH QUALITY RENDERING: Professional design, award-winning composition, trending on Dribbble/Behance, "
            "print-ready resolution, polished and publication-ready, modern 2024-2025 design trends, "
            "optimized for LinkedIn mobile and desktop feed."
        )

        return base_prompt + quality_suffix

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
