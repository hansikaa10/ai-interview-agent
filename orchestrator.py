from questions import get_question
from evaluator import evaluate_answer
from state import state
import random


def pick_topic():
    weak = sorted(state["weak_topics"].items(), key=lambda x: x[1], reverse=True)

    if weak[0][1] > 0:
        return weak[0][0]

    return random.choice(list(state["weak_topics"].keys()))


def update_memory(topic, result):

    if result["score"] >= 3:
        state["strong_topics"][topic] += 1
    else:
        state["weak_topics"][topic] += 1


def update_difficulty(score):

    if score >= 4:
        state["difficulty"] = "hard" if state["difficulty"] == "medium" else "medium"
    elif score <= 1:
        state["difficulty"] = "easy" if state["difficulty"] == "medium" else "medium"


# 🔥 NEW: FOLLOW-UP LOGIC
def generate_followup(topic, result):

    if result["grade"] == "Weak":
        return f"Can you explain {topic} more simply?"

    if result["score"] >= 5:
        return f"Good. Now give a real-world example of {topic}."

    return None


def run_interview(answer=None):

    topic = pick_topic()
    question = get_question(topic, state["difficulty"])

    if answer is None:
        return question, topic

    result = evaluate_answer(question, answer)

    update_memory(topic, result)
    update_difficulty(result["score"])

    followup = generate_followup(topic, result)

    return {
        "question": question,
        "result": result,
        "followup": followup,
        "difficulty": state["difficulty"]
    }