import streamlit as st
import tempfile
from orchestrator import run_interview
from state import state
from resume_parser import extract_resume_skills

st.set_page_config(page_title="AI Interview Agent", layout="centered")

st.title("🧠 AI Adaptive Interview Agent (Final Version)")

# -----------------------------
# 📄 Resume Upload Section
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
# 🧠 Initialize first question
# -----------------------------
if "question" not in st.session_state:
    output = run_interview()

    st.session_state.question = output["question"]
    st.session_state.topic = output.get("topic", "basics")
    st.session_state.difficulty = output.get("difficulty", "easy")

# -----------------------------
# Display question
# -----------------------------
st.write("### 🧠 Question:")
st.write(st.session_state.question)

answer = st.text_area("Your Answer:")

# -----------------------------
# Submit Answer
# -----------------------------
if st.button("Submit Answer"):

    output = run_interview(answer)

    result = output["result"]
    difficulty = output["difficulty"]
    followup = output["followup"]
    topic = output["topic"]

    st.write("### 📊 Score:", result["score"])
    st.write("### 🧠 Grade:", result["grade"])

    if result.get("feedback"):
        st.write("### 💡 Feedback")
        for f in result["feedback"]:
            st.write("- ", f)

    if followup:
        st.write("### 🔁 Follow-up Question")
        st.write(followup)

    st.write("### 🎯 Topic")
    st.write(topic)

    st.write("### ⚡ Difficulty")
    st.write(difficulty)

    # update UI question
    new_q = run_interview()
    st.session_state.question = new_q["question"]
    st.session_state.topic = new_q["topic"]

# -----------------------------
# 📊 Sidebar Analytics
# -----------------------------
st.sidebar.write("### 🧠 Weak Topics")
st.sidebar.write(state["weak_topics"])

st.sidebar.write("### 💪 Strong Topics")
st.sidebar.write(state["strong_topics"])

st.sidebar.write("### 📄 Resume Skills")
st.sidebar.write(state["resume_skills"])

# -----------------------------
# 📄 Final Report Section
# -----------------------------
st.sidebar.write("---")
st.sidebar.write("## 🧾 Final Report")

if st.button("Generate Report"):

    st.write("## 🧾 Interview Summary")

    history = state.get("history", [])
    scores = state.get("score_history", [])

    if scores:
        avg_score = sum(scores) / len(scores)
        st.write("### 📊 Average Score:", round(avg_score, 2))

    st.write("### 💪 Strong Topics")
    st.write(state["strong_topics"])

    st.write("### ⚠ Weak Topics")
    st.write(state["weak_topics"])

    st.write("### 🧠 Answer History")

    if history:
        for h in history[-10:]:
            st.write(h)
