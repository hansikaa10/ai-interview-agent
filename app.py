import streamlit as st
from orchestrator import run_interview
from state import state

st.set_page_config(page_title="AI Interview Agent")

st.title("AI Interview Agent")

# ---------------- INIT ----------------
if state["current_question"] is None:
    q = run_interview()
    state["current_question"] = q["question"]

# ---------------- DISPLAY ----------------
st.write("### Question")
st.write(state["current_question"])

answer = st.text_area("Your Answer")

# ---------------- SUBMIT ----------------
if st.button("Submit Answer"):

    if not answer.strip():
        st.warning("Please write an answer")
        st.stop()

    output = run_interview(answer)

    result = output["result"]

    st.write("### Score:", result["score"])
    st.write("### Grade:", result["grade"])

    st.write("### Feedback")
    for f in result["feedback"]:
        st.write("-", f)

    # UPDATE UI
    st.session_state.question = state["current_question"]

    st.rerun()

# ---------------- REPORT ----------------
st.sidebar.write("## Generate Report")

if st.sidebar.button("Generate Report"):

    st.write("## Final Report")

    if state["score_history"]:
        avg = sum(state["score_history"]) / len(state["score_history"])
        st.write("Average Score:", round(avg, 2))

    st.write("Weak Topics:", state["weak_topics"])
    st.write("Strong Topics:", state["strong_topics"])
    st.write("History:", state["history"])