import re

def normalize(text):
    return re.sub(r"\s+", " ", text.lower().strip())


KEY_CONCEPTS = {
    "basics": {
        "object": ["instance", "class", "object", "blueprint"],
        "variable": ["store", "value", "memory", "data"],
        "function": ["reuse", "block", "code", "task", "return"]
    },
    "oop": {
        "object": ["instance", "class", "object"],
        "class": ["blueprint", "object", "template"],
        "inheritance": ["parent", "child", "reuse", "extend"],
        "polymorphism": ["many", "forms", "override", "same name"]
    }
}

def evaluate_answer(question, answer):

    if not answer:
        return {
            "score": 0,
            "grade": "Weak",
            "feedback": ["No answer provided"],
            "matched_topic": "unknown"
        }

    keywords = question.lower().split()

    match_count = sum(1 for k in keywords if k in answer.lower())

    score = min(5, max(0, match_count))

    if score >= 4:
        grade = "Strong"
    elif score >= 2:
        grade = "Average"
    else:
        grade = "Weak"

    feedback = []
    if score < 2:
        feedback.append("Answer is too vague")
    elif score < 4:
        feedback.append("Good but missing depth")
    else:
        feedback.append("Excellent explanation")

    return {
        "score": score,
        "grade": grade,
        "feedback": feedback,
        "matched_topic": "general"
    }