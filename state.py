# state.py
def get_initial_state():
    return {
       "weak_topics": {"python": 0, "oop": 0, "basics": 0, "loops": 0, "functions": 0},
       "strong_topics": {"python": 0, "oop": 0, "basics": 0, "loops": 0, "functions": 0},
        "difficulty": "easy",
        "current_question": None,
        "current_topic": None,
        "pending_followup": None,
        "history": [],
        "score_history": [],
        "resume_skills": [],
        "resume_loaded": False
    }
