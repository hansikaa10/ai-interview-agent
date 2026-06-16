# 🧠 Adaptive AI Interview Agent

Welcome! This is a dynamic, state-preserving technical interview simulator built with Python and Streamlit. The application evaluates a candidate's conceptual understanding of programming topics in real-time, shifts questioning difficulty based on performance trends, extracts tech skills directly from uploaded PDF resumes, and exports a polished, presentation-ready PDF report of the session.

I built this project to dive deep into **state machine design**, **data extraction pipelines**, **real-time analytical dashboards**, and **Semantic Natural Language Processing (NLP)**.

---

## 🚀 Key Architectural Highlights

*   **Semantic NLP Evaluation Engine:** Replaced primitive keyword matching with an advanced, open-source Sentence Transformer (`all-MiniLM-L6-v2`) and Cosine Similarity mapping. The application computes high-dimensional vector embeddings to grade answers based on contextual, conceptual meaning rather than exact word spelling.
*   **Atomic State Management:** Streamlit naturally executes code from top to bottom on every single button press, which normally wipes out active variables. I engineered a centralized memory engine inside `st.session_state` to prevent data erasure and keep the interview flowing flawlessly.
*   **Dynamic Calibration Loops:** Designed an algorithmic turn processor that automatically scales question tracks (`easy` ⇄ `medium` ⇄ `hard`) depending on conceptual competency scores.
*   **Tokenized Skill Extraction:** Built a pipeline that extracts text from raw PDF resumes using structured token patterns to automatically prioritize interview questions that align with the candidate's actual tech stack.
*   **Native Programmatic Reporting:** Replaced raw JSON console dumps with an automated document generation engine that compiles and balances a multi-page business layout down to the exact millimeter on an A4 canvas.

---

## 🏗️ Inside the Repository

```text
ai-interview-agent/
│
├── app.py                # Core application dashboard and layout controller
├── orchestrator.py       # Turn processor, scoring routing, and flow engine
├── evaluator.py          # Semantic NLP evaluation rules & mathematical embeddings
├── feedback.py           # Markdown styling and text analytics engine
├── questions.py          # Categorized, multi-tiered mock technical repository
├── state.py              # Central template schema for session initialization
├── resume_parser.py      # High-level PDF data extraction and skill filter
├── report_generator.py   # Byte-level PDF matrix compiler using dynamic epw width
├── requirements.txt      # Python library dependencies
└── .gitignore            # Version control exceptions file
```

---

## 📊 Live Performance Tracking & Visualization

Instead of printing messy text blocks, the application computes metrics live in the sidebar dashboard:
*   **Dynamic Bar Charts:** Renders a real-time responsive proficiency matrix using native Streamlit data containers.
*   **Score Trajectories:** Tracks rolling micro-metric index cards monitoring performance trends over the last three consecutive rounds.
*   **Targeted Reinforcement Loops:** Intentionally intercepts weak concepts, holding the candidate on an active focus topic to provide targeted follow-ups until core criteria are met.

---

## 🛠️ Local Setup & Installation Guide

### Prerequisites
*   Make sure you have **Python 3.10 or higher** installed on your system.

### 1. Clone the Project
```bash
git clone https://github.com
cd ai-interview-agent
```

### 2. Isolate with a Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit Instance
```bash
streamlit run app.py
```

---

## 🏁 Exporting Final Assessment Metrics
At the end of an active interview session, candidates can instantly compile and download a clean, corporate-ready A4 PDF document containing:
1.  Identified skill proficiencies matched against uploaded resume metrics.
2.  A calculated conceptual matrix of demonstrated strengths and weaknesses.
3.  A complete, round-by-round historical transcript containing posed questions, candidate text inputs, and evaluation notes.
