import streamlit as st
import tempfile
from orchestrator import run_interview
from state import state
from resume_parser import extract_resume_skills

st.set_page_config(page_title="AI Interview Agent", layout="centered")

st.title("AI Interview Agent")

# ---------------- RESUME ----------------
if "resume_loaded" not in st.session_state:
    st.session_state.resume_loaded = False

file = st.sidebar.file_uploader("Upload Resume", type=["pdf"])

if file and not st.session_state.resume_loaded:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file.read())
        skills = extract_resume_skills(tmp.name)

        state["resume_skills"] = skills
        st.session_state.resume_loaded = True

        st.sidebar.write("Skills:", skills)

# ---------------- INIT ----------------
if state["current_question"] is None:
    first = run_interview()
    state["current_question"] = first["question"]

# ---------------- DISPLAY ----------------
st.write("### Question")
st.write(state["current_question"])

answer = st.text_area("Your Answer")

# ---------------- SUBMIT ----------------
if st.button("Submit Answer"):

    if not answer.strip():
        st.warning("Write something first")
        st.stop()

    output = run_interview(answer)
    result = output["result"]

    st.write("### Score:", result["score"])
    st.write("### Grade:", result["grade"])

    for f in result["feedback"]:
        st.write("-", f)

    st.session_state.question = state["current_question"]

    st.rerun()

# ---------------- REPORT ----------------
st.sidebar.write("## Report")

if st.sidebar.button("Generate Report"):

    st.write("## Final Report")

    if state["score_history"]:
        avg = sum(state["score_history"]) / len(state["score_history"])
        st.write("Average Score:", round(avg, 2))

    st.write("Weak Topics:", state["weak_topics"])
    st.write("Strong Topics:", state["strong_topics"])
    st.write("History:", state["history"])