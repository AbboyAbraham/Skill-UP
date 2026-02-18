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

    def adjust_skill(self, skill, delta):
        if skill in self.skills:
            self.skills[skill] = round(max(0.0, min(1.0, self.skills[skill] + delta)), 2)

    def set_quest(self, quest_id):
        self.current_quest_id = quest_id

    def get_quest(self):
        return self.current_quest_id