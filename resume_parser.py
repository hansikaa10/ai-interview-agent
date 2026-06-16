import pdfminer.high_level as pdf

def extract_resume_skills(file_path):

    text = pdf.extract_text(file_path)

    skills = []

    keywords = [
        "python", "java", "c++", "sql",
        "machine learning", "data science",
        "oop", "django", "flask"
    ]

    for k in keywords:
        if k in text.lower():
            skills.append(k)

    return skills