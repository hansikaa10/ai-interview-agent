# AI Adaptive Interview Agent

This project is an AI-powered interview simulator that adapts questions based on user performance and resume skills. It evaluates answers, tracks progress across topics, and adjusts difficulty dynamically.

---

## What this project does

- Questions are selected based on topic and difficulty  
- Answers are evaluated using a rule-based scoring system  
- Difficulty adjusts automatically based on performance  
- Weak and strong topics are tracked  
- Follow-up questions are generated when needed  
- Resume skills influence question selection  

---

## Key Features

- Adaptive question selection  
- Dynamic difficulty progression (easy, medium, hard)  
- Topic-wise performance tracking  
- Resume-based skill extraction  
- Structured feedback system  
- Follow-up question generation  
- Session memory support  

---

## Tech Stack

- Python  
- Streamlit  
- pdfminer  
- Rule-based logic system  

---

## How it works

1. User starts interview  
2. System selects question based on:
   - difficulty  
   - weak topics  
   - resume skills  
3. User submits answer  
4. Answer is evaluated  
5. System updates:
   - score  
   - difficulty  
   - topic strengths/weaknesses  
6. Next question is generated  

---

## Project Structure

- app.py → Streamlit UI  
- orchestrator.py → Interview logic  
- evaluator.py → Scoring engine  
- questions.py → Question bank  
- state.py → Memory storage  
- resume_parser.py → Resume skill extraction  

---

## Limitations

- Keyword-based evaluation  
- Not fully semantic AI  
- Basic resume parsing  

---

## Running locally

```bash
pip install -r requirements.txt
streamlit run app.py

---
## Author

Hansika Poddar