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

    output = run_interview(answer)
    st.write("DEBUG OUTPUT:", output)

    result = output["result"]
    difficulty = output["difficulty"]
    followup = output["followup"]
    topic = output["topic"]

    st.write("### 📊 Score:", result["score"])
    st.write("### 🧠 Grade:", result["grade"])

    if followup:
        st.write("### 🔁 Follow-up")
        st.write(followup)

    st.write("### 🎯 Current Topic")
    st.write(topic)

    st.write("### ⚡ Difficulty")
    st.write(difficulty)

    q, topic = run_interview()
    st.session_state.question = q
    st.session_state.topic = topic

st.sidebar.write("### 🧠 Weak Topics")
st.sidebar.write(state["weak_topics"])

st.sidebar.write("### 💪 Strong Topics")
st.sidebar.write(state["strong_topics"])

st.sidebar.write("### 📄 Resume Skills")
st.sidebar.write(state["resume_skills"])
