def evaluate_answer(question, answer):

    if not answer or len(answer.strip()) < 5:
        return {
            "score": 0,
            "grade": "Weak",
            "feedback": ["Answer too short or empty"],
            "matched_topic": "unknown"
        }

    question_words = set(question.lower().split())
    answer_words = set(answer.lower().split())

    overlap = len(question_words.intersection(answer_words))

    # SAFE SCORING (0–5)
    if overlap >= 5:
        score = 5
        grade = "Strong"
        feedback = ["Excellent explanation"]
    elif overlap >= 3:
        score = 3
        grade = "Average"
        feedback = ["Good but missing depth"]
    elif overlap >= 1:
        score = 1
        grade = "Weak"
        feedback = ["Too vague"]
    else:
        score = 0
        grade = "Weak"
        feedback = ["No relevant concepts found"]

    return {
        "score": score,
        "grade": grade,
        "feedback": feedback,
        "matched_topic": "general"
    }