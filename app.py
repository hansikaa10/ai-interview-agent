import streamlit as st
import tempfile

from orchestrator import run_interview
from state import state
from resume_parser import extract_resume_skills

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

# -----------------------------
# SHOW QUESTION
# -----------------------------
st.write("### 🧠 Question:")
st.write(st.session_state.question)

answer = st.text_area("Your Answer:")

# -----------------------------
# SUBMIT
# -----------------------------
if st.button("Submit Answer"):

    if not answer.strip():
        st.warning("Please write an answer")
        st.stop()

    output = run_interview(answer)

    result = output["result"]

    st.write("### 📊 Score:", result["score"])
    st.write("### 🧠 Grade:", result["grade"])

    if result.get("feedback"):
        st.write("### 💡 Feedback")
        for f in result["feedback"]:
            st.write("- ", f)

    # ALWAYS sync question from state (single source of truth)
    st.session_state.question = state["current_question"]

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.write("### Weak Topics")
st.sidebar.write(state["weak_topics"])

st.sidebar.write("### Strong Topics")
st.sidebar.write(state["strong_topics"])

st.sidebar.write("### Resume Skills")
st.sidebar.write(state["resume_skills"])