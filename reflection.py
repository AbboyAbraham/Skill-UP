import random
import re

DISTRESS_KEYWORDS = [
    "hurt myself", "end it", "suicide", "hopeless", "can't go on",
    "worthless", "no point", "self harm", "give up on life"
]

SKILLS = [
    "Critical Thinking", "Creativity", "Problem Solving", "Negotiation",
    "Decision Making", "Cooperation", "Self Management", "Resilience",
    "Communication", "Empathy", "Participation", "Respect for Diversity"
]

BANNED_PHRASES = [
    "ignore previous", "system prompt", "jailbreak",
    "forget instructions", "act as", "you are now"
]

def sanitize_text(text):
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    # Limit length
    return text.strip()[:500]

def check_for_distress(text):
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in DISTRESS_KEYWORDS)

def check_for_injection(text):
    text_lower = text.lower()
    return any(phrase in text_lower for phrase in BANNED_PHRASES)

def analyse_reflection(text):
    text = sanitize_text(text)

    # Block injection attempts
    if check_for_injection(text):
        return {"skill": "Self Management", "delta": 0.0}

    # Distress check before processing
    if check_for_distress(text):
        return {"skill": "Resilience", "delta": 0.0}

    # Placeholder — returns a random skill boost until API is connected
    return {"skill": random.choice(SKILLS), "delta": 0.05}

def apply_reflection(user, text):
    result = analyse_reflection(text)
    user.adjust_skill(result["skill"], result["delta"])
    return result
