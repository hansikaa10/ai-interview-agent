import re

CONCEPTS = {
    "functions": [
        "reuse", "reusable", "call", "return", "parameter",
        "argument", "task", "specific"
    ],
    "loops": [
        "iterate", "repeat", "for", "while", "multiple", "times"
    ],
    "oop": [
        "class", "object", "instance", "state",
        "behavior", "attribute", "method", "encapsulation"
    ],
    "basics": [
        "variable", "data", "value", "store", "type"
    ]
}


def evaluate_answer(question, answer):

    answer = answer.lower().strip()

    score = 0
    feedback = []

    # -----------------------
    # LENGTH CHECK
    # -----------------------
    words = len(answer.split())

    if words < 5:
        score -= 1
        feedback.append("Answer is too short.")
    elif words > 15:
        score += 1
        feedback.append("Good explanation length.")

    # -----------------------
    # DETECT TOPIC
    # -----------------------
    topic = "basics"
    q = question.lower()

    for t in CONCEPTS:
        if t in q:
            topic = t
            break

    # -----------------------
    # CONCEPT MATCHING (FAIR SCORING)
    # -----------------------
    matched = 0
    for concept in CONCEPTS[topic]:
        if concept in answer:
            matched += 1

    # normalize score (IMPORTANT FIX)
    concept_score = (matched / len(CONCEPTS[topic])) * 5
    score += concept_score

    feedback.append(
        f"Matched {matched}/{len(CONCEPTS[topic])} key concepts for {topic}."
    )

    # -----------------------
    # FINAL GRADING
    # -----------------------
    if score >= 4.5:
        grade = "Excellent"
    elif score >= 3:
        grade = "Good"
    elif score >= 1.5:
        grade = "Average"
    else:
        grade = "Weak"

    return {
        "score": round(score, 2),
        "grade": grade,
        "feedback": feedback,
        "matched_topic": topic
    }