# orchestrator.py
import random
from questions import get_question
from evaluator import evaluate_answer

LEVELS = ["easy", "medium", "hard"]

def pick_topic(state):
    # If resume skills exist, prioritize those topics first
    if state.get("resume_skills"):
        for skill in state["resume_skills"]:
            if skill in state["weak_topics"]:
                return skill
                
    # Sort topics by highest error weight/count
    weak = sorted(state["weak_topics"].items(), key=lambda x: x[1], reverse=True)
    if weak and weak[0][1] > 0:
        return weak[0][0]
        
    return random.choice(list(state["weak_topics"].keys()))


def update_memory(state, topic, result):
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

def update_difficulty(state, score):
    try:
        idx = LEVELS.index(state["difficulty"])
        if score >= 4 and idx < 2:
            state["difficulty"] = LEVELS[idx + 1]
        elif score <= 1 and idx > 0:
            state["difficulty"] = LEVELS[idx - 1]
    except ValueError:
        state["difficulty"] = "easy"

def generate_followup(topic, result):
    if result["score"] <= 1:
        return f"Explain {topic} simply with a basic code structure."
    if result["score"] >= 5:
        return f"Give a production real-world scenario where you implement {topic}."
    return None

def run_interview_turn(state, answer):
    # Process the evaluation of the user's answer
    result = evaluate_answer(state["current_question"], answer)
    topic = state["current_topic"]
    
    update_memory(state, topic, result)
    update_difficulty(state, result["score"])
    
    # Track follow-up state
    followup = generate_followup(topic, result)
    state["pending_followup"] = followup
    
    # Stage the next question immediately
    if followup:
        state["current_question"] = followup
    else:
        next_topic = pick_topic(state)
        state["current_topic"] = next_topic
        state["current_question"] = get_question(next_topic, state["difficulty"])
        
    return result
