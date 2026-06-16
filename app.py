import streamlit as st
import tempfile

from orchestrator import run_interview
from state import state
from resume_parser import extract_resume_skills

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="AI Interview Agent", layout="centered")

st.title("🧠 AI Adaptive Interview Agent")

# -----------------------------
# RESUME UPLOAD
# -----------------------------
st.sidebar.header("Resume Upload")

file = st.sidebar.file_uploader("Upload PDF Resume", type=["pdf"])

if file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file.read())
        skills = extract_resume_skills(tmp.name)
        state["resume_skills"] = skills
        st.sidebar.success(f"Skills detected: {skills}")

# -----------------------------
# INIT FIRST QUESTION
# -----------------------------
if "question" not in st.session_state:
    output = run_interview()

    st.session_state.question = output["question"]
    st.session_state.topic = output["topic"]

# -----------------------------
# DISPLAY CURRENT QUESTION
# -----------------------------
st.write("### 🧠 Question:")
st.write(st.session_state.question)

answer = st.text_area("Your Answer:")

# -----------------------------
# SUBMIT ANSWER FLOW
# -----------------------------
if st.button("Submit Answer"):

    if not answer.strip():
        st.warning("Please write an answer before submitting.")
        st.stop()

    output = run_interview(answer)

    result = output["result"]
    followup = output["followup"]

    # -------------------------
    # SHOW RESULTS
    # -------------------------
    st.write("### 📊 Score:", result["score"])
    st.write("### 🧠 Grade:", result["grade"])

    if result.get("feedback"):
        st.write("### 💡 Feedback")
        for f in result["feedback"]:
            st.write("- ", f)

    # -------------------------
    # IMPORTANT: SINGLE QUESTION FLOW
    # -------------------------
    if followup:
        # Follow-up replaces current question
        st.session_state.question = followup
        st.session_state.topic = "followup"
    else:
        # Move to next normal question
        new_q = run_interview()
        st.session_state.question = new_q["question"]
        st.session_state.topic = new_q["topic"]

# -----------------------------
# SIDEBAR ANALYTICS
# -----------------------------
st.sidebar.write("### 🧠 Weak Topics")
st.sidebar.write(state["weak_topics"])

st.sidebar.write("### 💪 Strong Topics")
st.sidebar.write(state["strong_topics"])

st.sidebar.write("### 📄 Resume Skills")
st.sidebar.write(state["resume_skills"])

# -----------------------------
# REPORT SECTION
# -----------------------------
st.sidebar.write("---")
st.sidebar.write("## 🧾 Final Report")

if st.button("Generate Report"):

    st.write("## 🧾 Interview Summary")

    scores = state.get("score_history", [])
    history = state.get("history", [])

    if scores:
        avg_score = sum(scores) / len(scores)
        st.write("### 📊 Average Score:", round(avg_score, 2))

    st.write("### 💪 Strong Topics")
    st.write(state["strong_topics"])

    st.write("### ⚠ Weak Topics")
    st.write(state["weak_topics"])

    st.write("### 🧠 Recent Activity")

    if history:
        for h in history[-10:]:
            st.write(h)
    else:
        st.write("No history recorded yet.")