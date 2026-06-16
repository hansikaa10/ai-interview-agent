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

    q = normalize(question)
    a = normalize(answer)

    score = 0
    feedback = []

    # find topic category
    topic_keywords = KEY_CONCEPTS["oop"] if "object" in q or "class" in q else KEY_CONCEPTS["basics"]

    matched = 0
    total = len(topic_keywords)

    for concept, keywords in topic_keywords.items():

        if any(k in a for k in keywords):
            matched += 1

    score = (matched / total) * 5

    # feedback logic
    if score >= 4:
        grade = "Strong"
        feedback.append("Good conceptual understanding.")
    elif score >= 2:
        grade = "Average"
        feedback.append(f"Partially correct. Matched {matched}/{total} concepts.")
    else:
        grade = "Weak"
        feedback.append(f"Needs improvement. Matched {matched}/{total} concepts.")

    return {
        "score": round(score, 2),
        "grade": grade,
        "feedback": feedback
    }