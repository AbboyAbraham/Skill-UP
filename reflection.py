import random

DISTRESS_KEYWORDS = [
    "hurt myself", "end it", "suicide", "hopeless", "can't go on",
    "worthless", "no point", "self harm", "give up on life"
]

SKILLS = [
    "Critical Thinking", "Creativity", "Problem Solving", "Negotiation",
    "Decision Making", "Cooperation", "Self Management", "Resilience",
    "Communication", "Empathy", "Participation", "Respect for Diversity"
]

def check_for_distress(text):
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in DISTRESS_KEYWORDS)

def analyse_reflection(text):
    # Placeholder — returns a random skill boost until API is connected
    return {"skill": random.choice(SKILLS), "delta": 0.05}

def apply_reflection(user, text):
    result = analyse_reflection(text)
    user.adjust_skill(result["skill"], result["delta"])
    return result