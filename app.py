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

# --- 1. MODERN MINIMALIST DARK THEME LAYOUT (CSS) ---
st.markdown("""
    <style>
    /* Global Background and Modern Typography */
    .stApp {
        background-color: #0f172a !important;
        color: #f1f5f9 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Clean Title & Header Typography Overrides */
    h1, h2, h3, h5, label, p, span {
        color: #ffffff !important;
        font-weight: 700 !important;
        letter-spacing: -0.025em;
    }
    .stCaption {
        color: #94a3b8 !important;
    }
    
    /* Premium Container for Question Prompt Card */
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
    
    /* Text Input Interface Styling Overrides */
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
    
    /* Flat Unified Sidebar Background Canvas */
    section[data-testid="stSidebar"] {
        background-color: #0b0f19 !important;
        border-right: 1px solid #1e293b !important;
    }
    
    /* Crimson Button Design Layout Override */
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
    
    /* Success Metrics Alert Strip Styling */
    div[data-testid="stSuccess"] {
        background-color: #064e3b !important;
        border: 1px solid #065f46 !important;
        color: #34d399 !important;
        border-radius: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. STATE PIPELINE SYSTEM INITIALIZATION ---
if "interview_state" not in st.session_state:
    st.session_state.interview_state = get_initial_state()

state = st.session_state.interview_state

# Initial application setup hook
if state["current_question"] is None:
    first_topic = pick_topic(state)
    state["current_topic"] = first_topic
    state["current_question"] = get_question(first_topic, state["difficulty"])

# --- 3. RE-DESIGNED LIVE ANALYTICS SIDEBAR ---
st.sidebar.title("📊 Assessment Metrics")

# Panel A: Resume Parsing Pipeline Interface
st.sidebar.markdown("##### **Upload PDF Resume**")
uploaded_file = st.sidebar.file_uploader("Upload Profile PDF", type=["pdf"], label_visibility="collapsed")
if uploaded_file and not state["resume_loaded"]:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        skills = extract_resume_skills(tmp.name)
        state["resume_skills"] = skills
        state["resume_loaded"] = True
        st.sidebar.success(f"🎯 Loaded Skills: {', '.join(skills)}")

# Panel B: Live Level Difficulty Banners
st.sidebar.markdown("---")
st.sidebar.markdown("##### **Live Calibration Metrics**")
diff_badge = {"easy": "🟢 Easy Track", "medium": "🟡 Medium Track", "hard": "🔴 Hard Track"}
st.sidebar.markdown(f"Current Difficulty Level: **{diff_badge.get(state['difficulty'], state['difficulty'].upper())}**")

# Panel C: Responsive Progress Meter Loops (Replaces old raw JSON text)
st.sidebar.markdown("---")
st.sidebar.markdown("##### **Topic Competency Matrix**")
all_topics = list(state["weak_topics"].keys())
for topic in all_topics:
    strong_count = state["strong_topics"].get(topic, 0)
    weak_count = state["weak_topics"].get(topic, 0)
    total = strong_count + weak_count
    
    score_ratio = (strong_count / total) if total > 0 else 0.0
    
    st.sidebar.markdown(f"`{topic.upper()}`")
    st.sidebar.progress(score_ratio)

# Panel D: Dynamic Metric Timeline Indicators
st.sidebar.markdown("---")
st.sidebar.markdown("##### **Recent Score Trajectory Trend**")
if state.get("score_history"):
    recent_scores = state["score_history"][-3:]
    cols = st.sidebar.columns(len(recent_scores))
    for idx, scr in enumerate(recent_scores):
        cols[idx].metric(label=f"Rd {len(state['score_history'])-len(recent_scores)+idx+1}", value=f"{scr}/5")
else:
    st.sidebar.caption("No historical run timelines recorded yet.")

# --- 4. EXECUTIVE WORKSPACE VIEWPORT ---
st.title("🤖 Adaptive Tech Interview Platform")
st.caption("⚡ Powered by Vector Semantic NLP (all-MiniLM-L6-v2) Evaluation Models.")
st.markdown("---")

main_container = st.container()
with main_container:
    st.markdown("##### Current Interview Question Prompt:")
    st.info(state["current_question"])
    st.write("") 
    
    user_answer = st.text_area("Your Answer:", height=150, placeholder="Type your answer layout solution guidelines here...")
    st.write("") 
    
    if st.button("Submit Answer", type="primary"):
        if not user_answer.strip():
            st.warning("The solution entry field cannot be submitted blank.")
        else:
            with st.spinner("Analyzing semantic coordinate vectors..."):
                eval_output = run_interview_turn(state, user_answer)
                st.rerun()

# --- 5. CHRONOLOGICAL EVALUATION METRICS REPORT ENGINE ---
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
