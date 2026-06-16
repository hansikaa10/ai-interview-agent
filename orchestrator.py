# orchestrator.py
import random
from questions import get_question
from evaluator import evaluate_answer

LEVELS = ["easy", "medium", "hard"]

def pick_topic(state):
    all_topics = list(state["weak_topics"].keys())
    
    # 1. Get the topic that was just asked in the previous round
    last_topic = state.get("current_topic")
    
    # 2. Force variety: filter it out so we choose a different topic next turn
    if last_topic in all_topics and len(all_topics) > 1:
        available_topics = [t for t in all_topics if t != last_topic]
    else:
        available_topics = all_topics
        
    # 3. Look for weak spots ONLY among the newly filtered available topics
    weak_counts = {t: state["weak_topics"].get(t, 0) for t in available_topics}
    max_weak_value = max(weak_counts.values()) if weak_counts else 0
    
    if max_weak_value > 0:
        candidates = [topic for topic, count in weak_counts.items() if count == max_weak_value]
        return random.choice(candidates)
        
    # 4. If no clear weak areas exist, check for resume skills
    if state.get("resume_skills"):
        valid_skills = [skill for skill in state["resume_skills"] if skill in available_topics]
        if valid_skills:
            return random.choice(valid_skills)
            
    # 5. Fallback selection
    return random.choice(available_topics)




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
    # Process the evaluation of the user's current answer
    result = evaluate_answer(state["current_question"], answer)
    topic = state["current_topic"]
    
    update_memory(state, topic, result)
    update_difficulty(state, result["score"])
    
    # 1. Check if the question just answered was ALREADY a follow-up
    was_already_followup = state.get("pending_followup") is not None
    
    # 2. Only generate a new follow-up if we aren't already inside one
    if not was_already_followup:
        followup = generate_followup(topic, result)
    else:
        followup = None # Force transition to a new question
        
    state["pending_followup"] = followup
    
    # 3. Stage the next question
    if followup:
        state["current_question"] = followup
    else:
        next_topic = pick_topic(state)
        state["current_topic"] = next_topic
        state["current_question"] = get_question(next_topic, state["difficulty"])
        
    return result
