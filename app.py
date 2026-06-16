# app.py
import streamlit as st
import tempfile
import json
from state import get_initial_state
from orchestrator import run_interview_turn, pick_topic
from questions import get_question
from resume_parser import extract_resume_skills
from feedback import generate_feedback

st.set_page_config(page_title="AI Interview Agent", layout="wide")

# 1. Secure State Engine Hook
if "interview_state" not in st.session_state:
    st.session_state.interview_state = get_initial_state()

state = st.session_state.interview_state

# Initial question boot routine
if state["current_question"] is None:
    first_topic = pick_topic(state)
    state["current_topic"] = first_topic
    state["current_question"] = get_question(first_topic, state["difficulty"])

# 2. Sidebar Componentry
st.sidebar.title("🧠 Candidate Assessment Context")

# Resume Skill Processor
uploaded_file = st.sidebar.file_uploader("Upload PDF Resume", type=["pdf"])
if uploaded_file and not state["resume_loaded"]:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        skills = extract_resume_skills(tmp.name)
        state["resume_skills"] = skills
        state["resume_loaded"] = True
        st.sidebar.success(f"Loaded Skills: {', '.join(skills)}")

# Metrics Dashboard
st.sidebar.markdown("---")
st.sidebar.subheader("🎯 Live Calibration Metrics")
st.sidebar.info(f"Target Track Level: **{state['difficulty'].upper()}**")

st.sidebar.markdown("**Demonstrated Proficiencies**")
st.sidebar.json(state["strong_topics"])

st.sidebar.markdown("**Flagged Areas for Improvement**")
st.sidebar.json(state["weak_topics"])

# 3. Main Workspace Routine
st.title("🤖 Adaptive Tech Interview Platform")
st.caption("Dynamic problem sets scaling with runtime user input analytics.")

st.subheader("Current Interview Question:")
st.info(state["current_question"])

# Clean text input area using unique session identification keys
user_answer = st.text_area("Your Answer:", key="input_text_area", height=150)

if st.button("Submit Answer", type="primary"):
    if not user_answer.strip():
        st.warning("Text entry block cannot be submitted empty.")
    else:
        with st.spinner("Analyzing semantics via AI Evaluation Matrix..."):
            # Execute state machine cycle updates
            eval_output = run_interview_turn(state, user_answer)
            
            # Extract historical references for printing logs
            latest_topic = state["current_topic"]
            
            # Format and display real-time feedback
            feedback_md = generate_feedback(
                eval_output, 
                state["current_question"], 
                user_answer, 
                latest_topic
            )
            st.session_state["last_feedback"] = feedback_md
            st.rerun()

# Keep feedback visible across session refreshes
if "last_feedback" in st.session_state:
    st.markdown("---")
    st.markdown(st.session_state["last_feedback"])

# 4. Final Transcript Report Generator Engine
if len(state["history"]) > 0:
    st.markdown("---")
    st.subheader("🏁 Conclude & Export Interview")
    
    if st.button("Generate Performance Transcript"):
        report_data = {
            "candidate_skills": state["resume_skills"],
            "final_standing": {
                "difficulty_achieved": state["difficulty"],
                "strong_areas": state["strong_topics"],
                "weak_areas": state["weak_topics"]
            },
            "detailed_timeline": state["history"]
        }
        
        json_report = json.dumps(report_data, indent=4)
        st.success("Report successfully generated!")
        st.download_button(
            label="📥 Download JSON Assessment Report",
            data=json_report,
            file_name="interview_performance_report.json",
            mime="application/json"
        )
