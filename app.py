import streamlit as st
import tempfile
from orchestrator import run_interview
from state import state
from resume_parser import extract_resume_skills

st.title("🧠 AI Adaptive Interview Agent (Final Version)")

# 📄 Resume Upload
st.sidebar.header("Resume Upload")
file = st.sidebar.file_uploader("Upload PDF Resume", type=["pdf"])

if file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file.read())
        skills = extract_resume_skills(tmp.name)
        state["resume_skills"] = skills
        st.sidebar.success(f"Skills detected: {skills}")

# 🧠 Session init
if "question" not in st.session_state:
    q, topic = run_interview()
    st.session_state.question = q
    st.session_state.topic = topic

st.write("### 🧠 Question:")
st.write(st.session_state.question)

answer = st.text_area("Your Answer:")

if st.button("Submit Answer"):

    result, topic, difficulty = run_interview(answer)

    st.write("### 📊 Score:", result["score"])
    st.write("### 🧠 Grade:", result["grade"])

    st.write("### 💬 Feedback:")
    for f in result["feedback"]:
        st.write("-", f)

    st.write("### 📌 Topic:", topic)
    st.write("### 🎚 Difficulty:", difficulty)

    q, topic = run_interview()
    st.session_state.question = q
    st.session_state.topic = topic

st.sidebar.write("### 🧠 Weak Topics")
st.sidebar.write(state["weak_topics"])

st.sidebar.write("### 💪 Strong Topics")
st.sidebar.write(state["strong_topics"])

st.sidebar.write("### 📄 Resume Skills")
st.sidebar.write(state["resume_skills"])