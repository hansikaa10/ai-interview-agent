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

st.markdown("""
    <style>
    /* 1. Premium Minimalist Dark Slate Foundation Base */
    .stApp {
        background-color: #090d16 !important;
        color: #f8fafc !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
    }
    
    /* 2. Premium Sans-Serif Typography Layouts */
    h1, h2, h3, h5, label, p, span, textarea {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        letter-spacing: -0.02em !important;
    }
    h1 {
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 2.25rem !important;
    }
    h2, h3, h5, label {
        color: #f1f5f9 !important;
        font-weight: 600 !important;
    }
    .stCaption {
        color: #64748b !important;
        font-size: 0.9rem !important;
    }
    
    /* 3. Minimalist Bordered Question Prompt Container Card */
    div[data-testid="stInfo"] {
        background-color: #111726 !important;
        border: 1px solid #1e293b !important;
        border-left: 5px solid #3b82f6 !important; /* Premium Clean Blue Accent */
        border-radius: 10px !important;
        padding: 1.5rem !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    div[data-testid="stInfo"] div {
        color: #e2e8f0 !important;
        font-weight: 500 !important;
    }
    
    /* 4. Elegant Minimalist Input Field Windows */
    textarea {
        background-color: #111726 !important;
        border: 1px solid #1e293b !important;
        border-radius: 8px !important;
        color: #ffffff !important;
        font-size: 1rem !important;
        padding: 1rem !important;
    }
    textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15) !important;
    }
    
    /* 5. Flat Solid Charcoal Sidebar Navigation Background */
    section[data-testid="stSidebar"] {
        background-color: #05070f !important;
        border-right: 1px solid #121824 !important;
    }
    
    /* 6. High-Contrast Progress Indicator Bars */
    div[data-testid="stSidebar"] div[role="progressbar"] {
        background-color: #121824 !important;
        border-radius: 6px;
        height: 8px !important;
    }
    div[data-testid="stSidebar"] div[role="progressbar"] > div {
        background-color: #3b82f6 !important; /* Vivid Blue Status Fill */
    }
    div[data-testid="stSidebar"] p {
        color: #94a3b8 !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        margin-top: 8px !important;
    }
    
    /* 7. Targeted Primary Action Button (Main Workspace Only) */
    div[data-testid="stMain"] div.stButton > button:first-child {
        background-color: #2563eb !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 0.6rem 2.2rem !important;
        transition: background-color 0.2s ease;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.15);
    }
    div[data-testid="stMain"] div.stButton > button:first-child:hover {
        background-color: #1d4ed8 !important;
    }
    
    /* 8. Download Panel Button Minimal Layout Match */
    div[data-testid="stVerticalBlock"] div.stButton > button:first-child {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        box-shadow: none !important;
        padding: 0.5rem 1.5rem !important;
    }
    div[data-testid="stVerticalBlock"] div.stButton > button:first-child:hover {
        background-color: #334155 !important;
    }
    
    /* 9. Safety Guard: Protect File Uploader Styles from Button Conflicts */
    div[data-testid="stFileUploader"] button {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 1px solid #334155 !important;
        box-shadow: none !important;
        transform: none !important;
    }
    div[data-testid="stFileUploader"] button:hover {
        background-color: #334155 !important;
    }
    
    /* 10. Subdued Forest Green Success Notification Strips */
    div[data-testid="stSuccess"] {
        background-color: #022c22 !important;
        border: 1px solid #064e3b !important;
        color: #34d399 !important;
        border-radius: 8px !important;
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
