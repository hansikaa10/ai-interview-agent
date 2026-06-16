# resume_parser.py
from pdfminer.high_level import extract_text

def extract_resume_skills(file_path):
    try:
        # CORRECT FIXED METHOD: Use the official pdfminer.six high-level API
        text = extract_text(file_path)
    except Exception as e:
        return ["Could not read resume file due to an error"]

    if not text or not text.strip():
        return ["Empty or unreadable resume content"]

    skills = []
    keywords = [
        "python", "java", "c++", "sql", "machine learning", 
        "data science", "oop", "django", "flask"
    ]
    
    # Process tokens to extract match values cleanly
    text_lower = text.lower()
    for k in keywords:
        if k in text_lower:
            skills.append(k)
            
    return skills if skills else ["No key tech skills detected"]

