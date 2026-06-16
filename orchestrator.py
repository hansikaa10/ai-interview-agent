import random
from questions import get_question
from evaluator import evaluate_answer
from state import state

LEVELS = ["easy", "medium", "hard"]


def pick_topic():

    weak = sorted(
        state["weak_topics"].items(),
        key=lambda x: x[1],
        reverse=True
    )

    if weak and weak[0][1] > 0:
        return weak[0][0]

    return random.choice(list(state["weak_topics"].keys()))


def update_memory(topic, result):

    state["score_history"].append(result["score"])
    state["history"].append({
        "topic": topic,
        "question": state["current_question"],
        "score": result["score"],
        "grade": result["grade"]
    })

    if result["score"] >= 3:
        state["strong_topics"][topic] += 1
    else:
        state["weak_topics"][topic] += 1


def update_difficulty(score):

    current = LEVELS.index(state["difficulty"])

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


# =========================
# MAIN ENGINE (FIXED)
# =========================
def run_interview(answer=None):

    # -------------------------
    # ASK MODE
    # -------------------------
    if answer is None:

        topic = pick_topic()
        question = get_question(topic, state["difficulty"])

        state["current_question"] = question
        state["current_topic"] = topic

        return {
            "question": question,
            "topic": topic,
            "result": None,
            "followup": None,
            "difficulty": state["difficulty"]
        }

    # -------------------------
    # EVALUATION MODE
    # -------------------------
    question = state["current_question"]
    topic = state["current_topic"]

    result = evaluate_answer(question, answer)

    update_memory(topic, result)
    update_difficulty(result["score"])

    followup = generate_followup(topic, result)

    # IMPORTANT: next question becomes follow-up if exists
    if followup:
        state["current_question"] = followup
        state["current_topic"] = topic
    else:
        new_topic = pick_topic()
        new_q = get_question(new_topic, state["difficulty"])

        state["current_question"] = new_q
        state["current_topic"] = new_topic

    return {
        "question": question,
        "topic": topic,
        "result": result,
        "followup": followup,
        "difficulty": state["difficulty"]
    }