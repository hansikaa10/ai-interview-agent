import streamlit as st
import tempfile
from orchestrator import run_interview
from state import state
from resume_parser import extract_resume_skills

st.set_page_config(page_title="AI Interview Agent", layout="centered")

st.title("AI Interview Agent")

# ---------------- RESUME ----------------
file = st.sidebar.file_uploader("Upload PDF Resume", type=["pdf"])

if file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file.read())
        skills = extract_resume_skills(tmp.name)
        state["resume_skills"] = skills
        st.sidebar.write(skills)

# ---------------- INIT ----------------
if state["current_question"] is None:
    q = run_interview()
    state["current_question"] = q["question"]

# ---------------- DISPLAY QUESTION ----------------
st.write("### Question")
st.write(state["current_question"])

answer = st.text_area("Your Answer")

# ---------------- SUBMIT ----------------
if st.button("Submit Answer"):

    if not answer.strip():
        st.warning("Enter answer first")
        st.stop()

    output = run_interview(answer)

    result = output["result"]

    # show score ONLY if available
    if result:
        st.write("### Score:", result["score"])
        st.write("### Grade:", result["grade"])

        if result.get("feedback"):
            st.write("### Feedback")
            for f in result["feedback"]:
                st.write("-", f)

    # MOVE TO NEXT QUESTION (IMPORTANT FIX)
    next_q = run_interview()
    state["current_question"] = next_q["question"]

    st.rerun()

# ---------------- REPORT (RESTORED) ----------------
st.sidebar.write("---")
st.sidebar.write("## Generate Report")

if st.sidebar.button("Generate Report"):

    st.write("## Interview Report")

    if state["score_history"]:
        avg = sum(state["score_history"]) / len(state["score_history"])
        st.write("### Average Score:", round(avg, 2))

    st.write("### Weak Topics")
    st.write(state["weak_topics"])

    st.write("### Strong Topics")
    st.write(state["strong_topics"])

    st.write("### Resume Skills")
    st.write(state["resume_skills"])

    st.write("### History")
    st.write(state["history"])