import json
import os
from datetime import date, timedelta

class AdolescentUser:
    def __init__(self, username):
        self.username = username
        self.skills = {
            "Critical Thinking": 0.5, "Creativity": 0.5, "Problem Solving": 0.5,
            "Negotiation": 0.5, "Decision Making": 0.5, "Cooperation": 0.5,
            "Self Management": 0.5, "Resilience": 0.5, "Communication": 0.5,
            "Empathy": 0.5, "Participation": 0.5, "Respect for Diversity": 0.5
        }
        self.current_quest_id = "prologue_01"
        self.xp = 0
        self.level = 1
        self.streak = 1
        self.last_login = str(date.today())
        self.completed_quests = []
        self.journal = []
        self.unlocked_achievements = []
        self.baseline_skills = {}

    def adjust_skill(self, skill, delta):
        if skill in self.skills:
            self.skills[skill] = round(max(0.0, min(1.0, self.skills[skill] + delta)), 2)

    def set_quest(self, quest_id):
        self.current_quest_id = quest_id

    def get_quest(self):
        return self.current_quest_id

    def add_xp(self, amount):
        self.xp += amount
        self.level = (self.xp // 100) + 1

    def update_streak(self):
        today = str(date.today())
        yesterday = str(date.today() - timedelta(days=1))
        if self.last_login == yesterday:
            self.streak += 1
        elif self.last_login != today:
            self.streak = 1
        self.last_login = today

    def log_quest(self, quest_id, skill, impact):
        self.completed_quests.append({
            "quest_id": quest_id,
            "skill": skill,
            "impact": impact
        })

    def add_journal_entry(self, text, skill_result):
        self.journal.append({
            "date": str(date.today()),
            "text": text,
            "skill": skill_result["skill"],
            "delta": skill_result["delta"]
        })

def save_user(user):
    data = {
        "username": user.username,
        "skills": user.skills,
        "current_quest_id": user.current_quest_id,
        "xp": user.xp,
        "level": user.level,
        "streak": user.streak,
        "last_login": user.last_login,
        "completed_quests": user.completed_quests,
        "journal": user.journal,
        "unlocked_achievements": user.unlocked_achievements,
        "baseline_skills": user.baseline_skills
    }
    with open(f"{user.username}_save.json", "w") as f:
        json.dump(data, f)

def load_user(username):
    filepath = f"{username}_save.json"
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            data = json.load(f)
        u = AdolescentUser(data["username"])
        u.skills = data["skills"]
        u.current_quest_id = data["current_quest_id"]
        u.xp = data.get("xp", 0)
        u.level = data.get("level", 1)
        u.streak = data.get("streak", 1)
        u.last_login = data.get("last_login", str(date.today()))
        u.completed_quests = data.get("completed_quests", [])
        u.journal = data.get("journal", [])
        u.unlocked_achievements = data.get("unlocked_achievements", [])
        u.baseline_skills = data.get("baseline_skills", {})
        return u
    return None