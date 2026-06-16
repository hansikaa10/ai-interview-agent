import re

# 🧠 Concept-based answer evaluation (SMART upgrade)

CONCEPTS = {
    "functions": [
        "reusable",
        "reuse",
        "call",
        "parameters",
        "arguments",
        "return",
        "code block",
        "specific task"
    ],
    "loops": [
        "iteration",
        "repeat",
        "for",
        "while",
        "condition",
        "sequence",
        "multiple times"
    ],
    "oop": [
        "class",
        "object",
        "inheritance",
        "polymorphism",
        "encapsulation",
        "method"
    ],
    "basics": [
        "variable",
        "data type",
        "store",
        "value",
        "memory"
    ]
}


def evaluate_answer(question, answer):

    answer = answer.lower().strip()

    score = 0
    feedback = []

    # --- 1. Length check (still useful) ---
    word_count = len(answer.split())

    if word_count < 5:
        score -= 2
        feedback.append("Answer is too short.")
    elif word_count > 25:
        score += 2
        feedback.append("Good detailed explanation.")
    else:
        score += 1
        feedback.append("Decent length.")

    # --- 2. Detect topic ---
    question_lower = question.lower()

    topic_found = "basics"
    for t in CONCEPTS.keys():
        if t in question_lower:
            topic_found = t
            break

    # --- 3. Concept matching ---
    matched = 0
    expected = CONCEPTS[topic_found]

    for concept in expected:
        if re.search(r"\b" + re.escape(concept) + r"\b", answer):
            matched += 1

    concept_score = (matched / len(expected)) * 5

    score += concept_score

    feedback.append(
        f"Matched {matched}/{len(expected)} key concepts for {topic_found}."
    )

    # --- 4. Weak answer detection ---
    weak_phrases = ["idk", "i don't know", "no idea", "not sure"]

    if any(p in answer for p in weak_phrases):
        score -= 3
        feedback.append("Shows lack of clarity.")

    # --- 5. Final grading ---
    if score >= 6:
        grade = "Excellent"
    elif score >= 4:
        grade = "Good"
    elif score >= 2:
        grade = "Average"
    else:
        grade = "Weak"

    return {
        "score": round(score, 2),
        "grade": grade,
        "feedback": feedback,
        "matched_topic": topic_found
    }


# 🧾 Pretty formatter (optional use in Streamlit)
def format_feedback(result):

    return f"""
📊 Evaluation Result
--------------------
Score: {result['score']}
Grade: {result['grade']}

🧠 Feedback:
- """ + "\n- ".join(result["feedback"])