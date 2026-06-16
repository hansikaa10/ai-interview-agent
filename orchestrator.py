import random
from questions import get_question
from evaluator import evaluate_answer
from state import state

LEVELS = ["easy", "medium", "hard"]


def pick_topic():
    weak = sorted(state["weak_topics"].items(), key=lambda x: x[1], reverse=True)
    if weak and weak[0][1] > 0:
        return weak[0][0]
    return random.choice(list(state["weak_topics"].keys()))


def update_memory(topic, result):
    state["score_history"].append(result["score"])

    state["history"].append({
        "question": state["current_question"],
        "topic": topic,
        "score": result["score"],
        "grade": result["grade"]
    })

    if result["score"] >= 3:
        state["strong_topics"][topic] += 1
    else:
        state["weak_topics"][topic] += 1


def update_difficulty(score):
    idx = LEVELS.index(state["difficulty"])

    if score >= 4 and idx < 2:
        state["difficulty"] = LEVELS[idx + 1]
    elif score <= 1 and idx > 0:
        state["difficulty"] = LEVELS[idx - 1]


def generate_followup(topic, result):
    if result["score"] <= 1:
        return f"Explain {topic} more simply"
    if result["score"] >= 5:
        return f"Give real example of {topic}"
    return None


def run_interview(answer=None):

    # ---------------- ASK MODE ----------------
    if answer is None:

        if state["pending_followup"]:
            q = state["pending_followup"]
            state["current_question"] = q
            state["current_topic"] = "followup"
            state["pending_followup"] = None

            return {
                "question": q,
                "topic": "followup",
                "result": None,
                "followup": None,
                "difficulty": state["difficulty"]
            }

        topic = pick_topic()
        q = get_question(topic, state["difficulty"])

        state["current_question"] = q
        state["current_topic"] = topic

        return {
            "question": q,
            "topic": topic,
            "result": None,
            "followup": None,
            "difficulty": state["difficulty"]
        }

    # ---------------- EVAL MODE ----------------
    result = evaluate_answer(state["current_question"], answer)

    topic = state["current_topic"]

    update_memory(topic, result)
    update_difficulty(result["score"])

    followup = generate_followup(topic, result)
    state["pending_followup"] = followup

    # ALWAYS GENERATE NEXT QUESTION HERE
    if followup:
        next_q = followup
    else:
        next_q = get_question(topic, state["difficulty"])

    state["current_question"] = next_q

    return {
        "question": next_q,
        "topic": topic,
        "result": result,
        "followup": followup,
        "difficulty": state["difficulty"]
    }