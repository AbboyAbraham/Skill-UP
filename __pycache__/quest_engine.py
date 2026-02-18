import json

def load_quests(filepath="quests.json"):
    with open(filepath, "r") as f:
        data = json.load(f)
    return {q["quest_id"]: q for q in data["quests"]}

def get_current_quest(quests, quest_id):
    return quests.get(quest_id, None)