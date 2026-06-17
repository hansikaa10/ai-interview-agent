# app.py
import streamlit as st
import tempfile
import json
from state import get_initial_state
from orchestrator import run_interview_turn, pick_topic
from questions import get_question
from resume_parser import extract_resume_skills
from feedback import generate_feedback
from report_generator import generate_pdf_transcript

st.set_page_config(page_title="AI Interview Agent", layout="wide")
st.markdown("""
    <style>
    /* 1. Universal Dark Theme Foundation */
    .stApp {
        background-color: #0f172a !important;
        color: #f1f5f9 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* 2. Title & Secondary Caption Header Typography */
    h1, h2, h3, h5, label {
        color: #ffffff !important;
        font-weight: 700 !important;
        letter-spacing: -0.025em;
    }
    .stCaption {
        color: #94a3b8 !important;
    }
    
    /* 3. Sleek Premium Card Container for Question Prompt */
    div[data-testid="stInfo"] {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        border-left: 6px solid #3b82f6 !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    div[data-testid="stInfo"] div {
        color: #e2e8f0 !important;
    }
    
    /* 4. Text Input Block Overrides */
    textarea {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        color: #ffffff !important;
        font-size: 1rem !important;
    }
    textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.25) !important;
    }
    
    /* 5. Flat Minimalist Sidebar Background */
    section[data-testid="stSidebar"] {
        background-color: #0b0f19 !important;
        border-right: 1px solid #1e293b !important;
    }
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] label {
        color: #ffffff !important;
    }
    
    /* 6. Crimson/Coral Primary Submit Button */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #ef4444, #dc2626) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 0.6rem 2.2rem !important;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 4px 10px rgba(239, 68, 68, 0.25);
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 15px rgba(239, 68, 68, 0.4);
    }
    
    /* 7. Clean Success Notification Styling */
    div[data-testid="stSuccess"] {
        background-color: #064e3b !important;
        border: 1px solid #065f46 !important;
        color: #34d399 !important;
        border-radius: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

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
# Locate your sidebar section in app.py and update it to this:

# 2. Sidebar Componentry
st.sidebar.title("🧠 Assessment Metrics")

# Resume Skill Processor (Keep your existing upload code intact)
uploaded_file = st.sidebar.file_uploader("Upload PDF Resume", type=["pdf"])
if uploaded_file and not state["resume_loaded"]:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        skills = extract_resume_skills(tmp.name)
        state["resume_skills"] = skills
        state["resume_loaded"] = True
        st.sidebar.success(f"Loaded Skills: {', '.join(skills)}")

st.sidebar.markdown("---")
st.sidebar.subheader("🎯 Live Calibration Metrics")

# Visual Element 1: Clean Level Indicator Gauge
difficulty_colors = {"easy": "🟢 Easy Track", "medium": "🟡 Medium Track", "hard": "🔴 Hard Track"}
current_lev = state.get('difficulty', 'easy')
st.sidebar.markdown(f"Current Difficulty Level: **{difficulty_colors.get(current_lev, current_lev.upper())}**")

# Visual Element 2: Real-time Interactive Strength vs. Weakness Chart
st.sidebar.markdown("##### **Topic Competency Matrix**")

# Prepare data payload safely for the UI rendering framework
chart_data = {}
all_topics = set(list(state["strong_topics"].keys()) + list(state["weak_topics"].keys()))

for topic in all_topics:
    strong_count = state["strong_topics"].get(topic, 0)
    weak_count = state["weak_topics"].get(topic, 0)
    # Calculate a net baseline proficiency metric index score
    total_attempts = strong_count + weak_count
    if total_attempts > 0:
        chart_data[topic.upper()] = round((strong_count / total_attempts) * 100, 1)
    else:
        chart_data[topic.upper()] = 0.0

# Render native graphical container instantly down the sidebar channel
if any(v > 0 for v in chart_data.values()):
    st.sidebar.bar_chart(chart_data)
else:
    st.sidebar.caption("Complete your first interview question to populate the analytics dashboard chart grid matrix.")

# Visual Element 3: Clean Metric Progress Cards
st.sidebar.markdown("##### **Recent Score Trajectory Trend**")
if state.get("score_history"):
    recent_scores = state["score_history"][-3:] # Capture the last 3 turns
    cols = st.sidebar.columns(len(recent_scores))
    for idx, scr in enumerate(recent_scores):
        cols[idx].metric(label=f"Round {len(state['score_history'])-len(recent_scores)+idx+1}", value=f"{scr}/5")
else:
    st.sidebar.caption("No historical run timelines recorded yet.")


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
    
    try:
        # Generate the PDF binary array snapshot string data stream 
        pdf_data = generate_pdf_transcript(state)
        
        st.success("PDF Transcript successfully compiled and calibrated!")
        st.download_button(
            label="📥 Download PDF Assessment Report",
            data=bytes(pdf_data), # Convert string output buffer safely into browser byte format
            file_name="interview_performance_report.pdf",
            mime="application/pdf"
        )
    except Exception as e:
        st.error(f"Failed to generate document matrix layout: {str(e)}")