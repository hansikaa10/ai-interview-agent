def generate_feedback(result, question, answer, topic):

    score = result["score"]
    grade = result["grade"]
    feedback_list = result["feedback"]

    response = []

    # 🧠 HEADER (human interviewer tone)
    if grade == "Strong":
        response.append("🟢 Strong answer — you clearly understand the concept.")
    elif grade == "Average":
        response.append("🟡 Decent attempt, but there are gaps in understanding.")
    else:
        response.append("🔴 Needs improvement — core concept is not clear.")

    # 🎯 Question-specific feedback
    response.append(f"\n📌 Question Focus: {topic}")

    # 🧠 Personalized correction
    if "Missing core concept" in " ".join(feedback_list):
        response.append("👉 You missed key concepts — revise fundamentals of this topic.")

    if "Too short" in " ".join(feedback_list):
        response.append("👉 Try explaining in steps instead of short definitions.")

    if "Good reasoning" in " ".join(feedback_list):
        response.append("👉 Good logical thinking — keep structuring your answers like this.")

    # 📊 Score interpretation
    if score >= 5:
        response.append("🔥 Interviewer would consider this a strong hire-level answer.")
    elif score >= 2:
        response.append("⚠️ Borderline answer — needs refinement for interviews.")
    else:
        response.append("❌ Below interview standard — revisit basics.")

    return "\n".join(response)
