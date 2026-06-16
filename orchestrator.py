# orchestrator.py
import random
from questions import get_question
from evaluator import evaluate_answer

LEVELS = ["easy", "medium", "hard"]

def pick_topic(state):
    # 1. Gather all active topic categories
    all_topics = list(state["weak_topics"].keys())
    
    # 2. Check what areas the candidate is struggling with the most
    max_weak_value = max(state["weak_topics"].values())
    
    # If there are actual weak points flagged (> 0), pick randomly among the weakest areas
    if max_weak_value > 0:
        candidates = [topic for topic, count in state["weak_topics"].items() if count == max_weak_value]
        return random.choice(candidates)
        
    # 3. If there are no mistakes yet, prioritize resume skills but shuffle them to ensure variety
    if state.get("resume_skills"):
        valid_skills = [skill for skill in state["resume_skills"] if skill in state["weak_topics"]]
        if valid_skills:
            return random.choice(valid_skills) # Shuffles choices instead of locking the first one
            
    # 4. Ultimate fallback: pick any category randomly
    return random.choice(all_topics)



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
