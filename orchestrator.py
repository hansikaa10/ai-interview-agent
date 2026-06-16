from questions import get_question
from evaluator import evaluate_answer
from state import state
import random


LEVELS = ["easy", "medium", "hard"]

SKILL_TOPIC_MAP = {
    "python": "basics",
    "oop": "oop",
    "loops": "loops",
    "function": "functions",
    "flask": "functions",
    "django": "functions",
}


def pick_topic():

    skills = state.get("resume_skills", [])

    mapped_topics = []

    for skill in skills:
        if skill in SKILL_TOPIC_MAP:
            mapped_topics.append(SKILL_TOPIC_MAP[skill])

    # If resume has skills → prioritize them
    if mapped_topics:
        return random.choice(mapped_topics)

    # fallback → weak topics
    weak = sorted(
        state["weak_topics"].items(),
        key=lambda x: x[1],
        reverse=True
    )

    if weak and weak[0][1] > 0:
        return random.choice(weak[:2])[0]

    return random.choice(list(state["weak_topics"].keys()))


def update_memory(topic, result):

    if result["score"] >= 3:
        state["strong_topics"][topic] += 1
    else:
        state["weak_topics"][topic] += 1


def update_difficulty(score):

    current = LEVELS.index(
        state["difficulty"]
    )

    if score >= 4 and current < 2:
        state["difficulty"] = LEVELS[current + 1]

    elif score <= 1 and current > 0:
        state["difficulty"] = LEVELS[current - 1]


def generate_followup(topic, result):

    if result["score"] <= 1:
        return f"Can you explain {topic} more clearly?"

    if result["score"] >= 5:
        return f"Give a real-world example of {topic}."

    return None


def run_interview(answer=None):

    if state["pending_followup"] and answer is None:
        followup_question = state["pending_followup"]
        state["pending_followup"] = None
        return {
            "question": followup_question,
            "topic": "followup",
            "result": None,
            "followup": None,
            "difficulty": state["difficulty"],
            "weak_topics": state["weak_topics"],
            "strong_topics": state["strong_topics"]
        }

    topic = pick_topic()

    question = get_question(topic, state["difficulty"])

    if answer is None:
        return {
            "question": question,
            "topic": topic,
            "difficulty": state["difficulty"]
        }

    result = evaluate_answer(question, answer)

    update_memory(topic, result)
    update_difficulty(result["score"])

    followup = generate_followup(topic, result)

    state["pending_followup"] = followup

    # 🔥 NEW: history tracking
    state["history"].append({
        "question": question,
        "answer": answer,
        "topic": topic,
        "score": result["score"]
    })

    state["score_history"].append(result["score"])

    return {
        "question": question,
        "topic": topic,
        "result": result,
        "followup": followup,
        "difficulty": state["difficulty"],
        "weak_topics": state["weak_topics"],
        "strong_topics": state["strong_topics"]
    }