# feedback.py
def generate_feedback(result, question, answer, topic):
    score = result["score"]
    grade = result["grade"]
    feedback_list = result["feedback"]
    
    response = []
    response.append(f"### 📊 Question Focus: **{topic.upper()}**")
    
    if grade == "Strong":
        response.append("🟢 **Strong Answer:** You clearly understand the concept.")
    elif grade == "Average":
        response.append("🟡 **Decent Attempt:** But there are gaps in your explanation.")
    else:
        response.append("🔴 **Needs Improvement:** The core concept is missing or unclear.")
        
    response.append(f"💡 *Feedback:* {' '.join(feedback_list)}")
    
    if score >= 4:
        response.append("🎯 *Interviewer note:* This is a strong hire-level answer.")
    elif score >= 2:
        response.append("⚠️ *Interviewer note:* Borderline answer – needs refinement.")
    else:
        response.append("❌ *Interviewer note:* Below interview standard – revisit basics.")
        
    return "\n\n".join(response)
