# app.py
import streamlit as st
import tempfile
import json
from state import get_initial_state
from orchestrator import run_interview_turn, pick_topic
from questions import get_question
from resume_parser import extract_resume_skills
from report_generator import generate_pdf_transcript

st.set_page_config(page_title="AI Interview Agent", layout="wide")

# --- 1. SECURE STATE ENGINE INITIALIZATION ---
if "interview_state" not in st.session_state:
    st.session_state.interview_state = get_initial_state()

state = st.session_state.interview_state

if state["current_question"] is None:
    first_topic = pick_topic(state)

    question, reference = get_question(
        first_topic,
        state["difficulty"]
    )

    state["current_topic"] = first_topic
    state["current_question"] = question
    state["reference_answer"] = reference
# --- 2. NATIVE METRIC SIDEBAR ---
st.sidebar.title("📊 Assessment Metrics")

# Section A: Resume File Uploader
st.sidebar.subheader("Upload PDF Resume")
uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type=["pdf"], label_visibility="collapsed")
if uploaded_file and not state["resume_loaded"]:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        skills = extract_resume_skills(tmp.name)
        state["resume_skills"] = skills
        state["resume_loaded"] = True
        st.sidebar.success(f"🎯 Loaded Skills: {', '.join(skills)}")

# Section B: Live Track Calibration Gauges
st.sidebar.markdown("---")
st.sidebar.subheader("Live Calibration Metrics")
diff_badge = {"easy": "🟢 Easy Track", "medium": "🟡 Medium Track", "hard": "🔴 Hard Track"}
st.sidebar.write(f"Current Difficulty Level: **{diff_badge.get(state['difficulty'], state['difficulty'].upper())}**")

# Section C: Topic Progress Bars
st.sidebar.markdown("---")
st.sidebar.subheader("Topic Competency Matrix")

all_topics = list(state["weak_topics"].keys())
for topic in all_topics:
    strong_count = state["strong_topics"].get(topic, 0)
    weak_count = state["weak_topics"].get(topic, 0)
    total = strong_count + weak_count
    
    score_ratio = (strong_count / total) if total > 0 else 0.0
    
    st.sidebar.write(f"**{topic.upper()}**")
    st.sidebar.progress(score_ratio)

# Section D: History Scores Dashboard Card
st.sidebar.markdown("---")
st.sidebar.subheader("Recent Score Trajectory Trend")
if state.get("score_history"):
    recent_scores = state["score_history"][-3:]
    cols = st.sidebar.columns(len(recent_scores))
    for idx, scr in enumerate(recent_scores):
        cols[idx].metric(label=f"Rd {len(state['score_history'])-len(recent_scores)+idx+1}", value=f"{scr}/5")
else:
    st.sidebar.caption("No historical timelines logged yet.")

# --- 3. MAIN WORKSPACE DESIGN ---
st.title("🤖 Adaptive Tech Interview Platform")
st.caption("⚡ Powered by Vector Semantic NLP (all-MiniLM-L6-v2) Evaluation Models.")
st.markdown("---")

main_container = st.container()
with main_container:
    st.subheader("Current Interview Question:")
    st.info(state["current_question"])
    
    user_answer = st.text_area("Your Answer:", height=150, placeholder="Type your answer layout solution guidelines here...")
    
    if st.button("Submit Answer", type="primary"):
        if not user_answer.strip():
            st.warning("The answer entry field cannot be submitted blank.")
        else:
            with st.spinner("Analyzing semantic vectors..."):
                eval_output = run_interview_turn(state, user_answer)
                st.rerun()

# --- 4. CHRONOLOGICAL EVALUATION METRICS REPORT ENGINE ---
if state["history"]:
    latest_run = state["history"][-1]
    st.markdown("---")
    st.subheader("🏁 Performance Review & Report Panel")
    
    # Real-Time Visual Feedback Output Cards
    col_g1, col_g2 = st.columns(2)
    col_g1.metric(label="Assigned Performance Rating", value=latest_run["grade"])
    col_g2.metric(label="Calculated Evaluation Score", value=f"{latest_run['score']} / 5")
    
    st.write("")
    
    # PDF Compilation Stream Processing Trigger
    try:
        pdf_data = generate_pdf_transcript(state)
        st.success("PDF Transcript successfully compiled and calibrated!")
        st.download_button(
            label="📥 Download PDF Assessment Report",
            data=bytes(pdf_data),
            file_name="interview_performance_report.pdf",
            mime="application/pdf"
        )
    except Exception as e:
        st.error(f"Failed to generate layout matrix report tracking streams: {str(e)}")
