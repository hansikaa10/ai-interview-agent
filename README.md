# Adaptive AI Interview Agent

Adaptive AI Interview Agent is a technical interview simulator built with Python and Streamlit. The application evaluates candidate responses, adapts question difficulty based on performance, extracts skills from uploaded PDF resumes, and generates downloadable interview assessment reports.

The project was built to explore natural language processing, state management in web applications, resume parsing, and adaptive learning systems.

---

## Features

### Semantic Answer Evaluation

Instead of relying only on exact keyword matching, the application uses Sentence Transformers and cosine similarity to evaluate answers based on their meaning. This allows users to phrase answers naturally while still receiving accurate feedback.

### Adaptive Interview Flow

The interview dynamically adjusts difficulty levels based on previous performance. Strong answers move the candidate toward more challenging questions, while weaker responses trigger simpler or follow-up questions.

### Resume Skill Extraction

Users can upload a PDF resume, and the system automatically extracts technical skills using text parsing techniques.

### Performance Tracking

The application continuously tracks:

- Topic-wise strengths and weaknesses
- Difficulty progression
- Score history
- Interview performance trends

### PDF Assessment Reports

At the end of an interview session, users can generate and download a structured PDF report summarizing their performance.

---

## Technologies Used

- Python
- Streamlit
- Sentence Transformers
- Scikit-learn
- PDFMiner
- FPDF2

---

## Project Structure

```text
ai-interview-agent/
│
├── app.py                # Streamlit application interface
├── orchestrator.py       # Interview flow and difficulty management
├── evaluator.py          # Semantic answer evaluation logic
├── feedback.py           # Feedback generation utilities
├── questions.py          # Technical question bank
├── state.py              # Session state management
├── resume_parser.py      # Resume text extraction and skill detection
├── report_generator.py   # PDF report generation
├── requirements.txt      # Project dependencies
└── .gitignore            # Git tracking exclusions
```

---

## How It Works

1. The user uploads a resume (optional).
2. The system extracts relevant technical skills from the PDF.
3. The interview begins with a technical question.
4. Answers are evaluated using semantic similarity scoring.
5. Difficulty adjusts based on performance.
6. Strengths and weaknesses are tracked across topics.
7. A downloadable PDF report is generated at the end of the session.

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/hansikaa10/ai-interview-agent.git
cd ai-interview-agent
```

### Create a Virtual Environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
streamlit run app.py
```

---

## Future Improvements

- Resume-driven question generation
- Expanded technical question bank
- More advanced performance analytics
- Voice-based interview support
- Additional interview domains beyond programming

---

## Author

**Hansika Poddar**

Built as a learning project exploring adaptive interview systems, NLP-based answer evaluation, and interactive web application development.