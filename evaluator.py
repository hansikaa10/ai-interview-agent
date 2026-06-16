def evaluate_answer(question, answer):
    answer = answer.strip().lower()
    question = question.lower()

    score = 0
    feedback = []

    word_count = len(answer.split())

    # 1. Length intelligence
    if word_count < 5:
        score -= 2
        feedback.append("Too short — interviewer expects explanation.")
    elif word_count > 25:
        score += 2
        feedback.append("Good depth of explanation.")
    else:
        score += 1

    # 2. Confidence detection
    low_confidence = ["idk", "not sure", "maybe", "i think"]
    if any(w in answer for w in low_confidence):
        score -= 2
        feedback.append("Low confidence in answer.")

    # 3. Reasoning signals
    reasoning_words = ["because", "therefore", "for example", "means", "so"]
    if any(w in answer for w in reasoning_words):
        score += 2
        feedback.append("Good reasoning shown.")

    # 4. Topic alignment check
    topic_map = {
        "loop": ["for", "while", "iteration"],
        "function": ["return", "def", "parameter"],
        "oop": ["class", "object", "inheritance"]
    }

    matched = None

    for t, keywords in topic_map.items():
        if t in question:
            matched = t
            if any(k in answer for k in keywords):
                score += 2
                feedback.append(f"Correct concept coverage: {t}")
            else:
                score -= 2
                feedback.append(f"Missing core concept of {t}")

    # 5. Final grade
    if score >= 5:
        grade = "Strong"
    elif score >= 2:
        grade = "Average"
    else:
        grade = "Weak"

    return {
        "score": score,
        "grade": grade,
        "feedback": feedback,
        "matched_topic": matched
    }