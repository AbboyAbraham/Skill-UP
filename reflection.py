import anthropic
import os
import json

client = anthropic.Anthropic()  # automatically finds ANTHROPIC_API_KEY

SKILLS = [
    "Critical Thinking", "Creativity", "Problem Solving", "Negotiation",
    "Decision Making", "Cooperation", "Self Management", "Resilience",
    "Communication", "Empathy", "Participation", "Respect for Diversity"
]

DISTRESS_KEYWORDS = [
    "hurt myself", "end it", "suicide", "hopeless", "can't go on",
    "worthless", "no point", "self harm", "give up on life"
]

def check_for_distress(text):
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in DISTRESS_KEYWORDS)

def analyse_reflection(text):
    prompt = f"""
    You are a skill analyser. A user wrote this reflection about their day:
    "{text}"

    From this list of skills: {SKILLS}

    Return ONLY a JSON object like this, no explanation, no extra text:
    {{"skill": "Resilience", "delta": 0.05}}

    Rules:
    - Pick only ONE skill most relevant to the reflection
    - delta must be between -0.1 and 0.1
    - Positive if they handled it well, negative if they struggled
    - Return ONLY the JSON, nothing else
    """
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=100,
        messages=[{"role": "user", "content": prompt}]
    )
    cleaned = message.content[0].text.strip().replace("```json", "").replace("```", "")
    return json.loads(cleaned)

def apply_reflection(user, text):
    result = analyse_reflection(text)
    user.adjust_skill(result["skill"], result["delta"])
    return result