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
    /* 1. Cyberpunk Dark Base with Digital Grid Texture */
    .stApp {
        background-color: #030712 !important;
        color: #e2e8f0 !important;
        font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace !important;
        background-image: 
            linear-gradient(rgba(59, 130, 246, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(59, 130, 246, 0.03) 1px, transparent 1px);
        background-size: 20px 20px;
    }
    
    /* 2. Glowing Neon Futuristic Titles */
    h1 {
        color: #ffffff !important;
        font-weight: 800 !important;
        text-shadow: 0 0 10px rgba(59, 130, 246, 0.5), 0 0 20px rgba(59, 130, 246, 0.2);
        letter-spacing: -1px;
    }
    h2, h3, h5, label {
        color: #38bdf8 !important; /* Cyber Cyan Headers */
        font-family: 'JetBrains Mono', monospace !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stCaption {
        color: #a855f7 !important; /* Matrix Purple Subtext */
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* 3. Glassmorphic Sci-Fi Prompt Container */
    div[data-testid="stInfo"] {
        background: rgba(15, 23, 42, 0.6) !important;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(56, 189, 248, 0.2) !important;
        border-left: 6px solid #06b6d4 !important; /* Electric Cyan accent */
        border-radius: 10px !important;
        padding: 1.5rem !important;
        box-shadow: 0 0 15px rgba(6, 182, 212, 0.15);
    }
    div[data-testid="stInfo"] div {
        color: #38bdf8 !important;
    }
    
    /* 4. Terminal-Style Text Entry Windows */
    textarea {
        background-color: #020617 !important;
        border: 1px solid #1e293b !important;
        border-radius: 8px !important;
        color: #4ade80 !important; /* Classic Matrix Terminal Green Output Text */
        font-family: 'Fira Code', 'Courier New', monospace !important;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.6);
    }
    textarea:focus {
        border-color: #a855f7 !important; /* Glows neon purple on selection focus */
        box-shadow: 0 0 12px rgba(168, 85, 247, 0.3) !important;
    }
    
    /* 5. Deep Void Command Sidebar Panel */
    section[data-testid="stSidebar"] {
        background-color: #020617 !important;
        border-right: 1px solid rgba(56, 189, 248, 0.1) !important;
    }
    
    /* 6. High-Visibility Custom Matrix Sidebar Progress Bars */
    div[data-testid="stSidebar"] div[role="progressbar"] {
        background-color: #1e293b !important;
        border-radius: 4px;
        height: 8px !important;
    }
    div[data-testid="stSidebar"] div[role="progressbar"] > div {
        background: linear-gradient(90deg, #3b82f6, #06b6d4) !important; /* Cyber color gradient shift */
        box-shadow: 0 0 8px #06b6d4;
    }
    div[data-testid="stSidebar"] p {
        color: #e2e8f0 !important;
        font-size: 0.8rem !important;
        margin-top: 10px !important;
    }
    
    /* 7. Pulse-Glowing Primary Action Button */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #ef4444, #b91c1c) !important;
        color: #ffffff !important;
        font-family: 'JetBrains Mono', monospace !important;
        text-transform: uppercase;
        font-weight: 700 !important;
        border-radius: 6px !important;
        border: 1px solid #f87171 !important;
        padding: 0.6rem 2.2rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 0 10px rgba(239, 68, 68, 0.3);
    }
    div.stButton > button:first-child:hover {
        transform: scale(1.02) translateY(-1px);
        box-shadow: 0 0 20px rgba(239, 68, 68, 0.6);
        border-color: #ffffff !important;
    }
    
    /* 8. Download Panel Button Override Style */
    div[data-testid="stVerticalBlock"] div.stButton > button:first-child {
        background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
        border: 1px solid #60a5fa !important;
        box-shadow: 0 0 10px rgba(37, 99, 235, 0.3) !important;
    }
    div[data-testid="stVerticalBlock"] div.stButton > button:first-child:hover {
        box-shadow: 0 0 20px rgba(37, 99, 235, 0.6) !important;
    }
    
    /* 9. Holographic Green Success Confirmation Banners */
    div[data-testid="stSuccess"] {
        background-color: rgba(6, 78, 59, 0.4) !important;
        backdrop-filter: blur(8px);
        border: 1px solid #10b981 !important;
        color: #34d399 !important;
        text-shadow: 0 0 5px rgba(52, 211, 153, 0.5);
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
