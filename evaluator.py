# evaluator.py
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from functools import lru_cache
import numpy as np

# Load a lightweight, highly optimized open-source model into memory
# Using lru_cache ensures the model loads only ONCE to save memory
@lru_cache(maxsize=1)
def load_nlp_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

def evaluate_answer(question, answer):
    # Guard Rails for blank submissions
    if not answer or len(answer.strip()) < 5:
        return {
            "score": 0,
            "grade": "Weak",
            "feedback": ["The submission field was evaluated as blank or too short."],
            "matched_topic": "general"
        }

    # Initialize model instance safely
    model = load_nlp_model()
    
    # Define a technical anchor context string to judge substance
    tech_anchor = "implementation framework production deployment scalability standard syntax code automation database architecture"
    
    # 1. Encode all three strings into numerical vectors
    embeddings = model.encode([answer, question, tech_anchor])
    
    # 2. Extract individual vector coordinates cleanly from the array matrix
    answer_vector = embeddings[0].reshape(1, -1)
    question_vector = embeddings[1].reshape(1, -1)
    anchor_vector = embeddings[2].reshape(1, -1)
    
    # 3. Calculate exact math angles (Cosine Similarity scores between 0.0 and 1.0)
    question_similarity = float(cosine_similarity(answer_vector, question_vector)[0][0])
    substance_similarity = float(cosine_similarity(answer_vector, anchor_vector)[0][0])
    
    # Combine metrics using a balanced weighted average index
    smart_score_metric = (question_similarity * 0.4) + (substance_similarity * 0.6)
    
    # 4. Map the mathematical index output to your application's 0-5 grading tier
    if smart_score_metric >= 0.42:
        score = 5
        grade = "Strong"
        feedback = ["Excellent contextual depth! Your explanation maps precisely to the structural requirements."]
    elif smart_score_metric >= 0.30:
        score = 3
        grade = "Average"
        feedback = ["Good foundational explanation, but missing explicit technical vocabulary or architecture depth."]
    elif smart_score_metric >= 0.15:
        score = 1
        grade = "Weak"
        feedback = ["Concept mentioned vaguely, but your answer lacks explicit engineering keywords or practical detail."]
    else:
        score = 0
        grade = "Weak"
        feedback = ["No relevant programmatic conceptual patterns or technical substance detected."]
        
    return {
        "score": score,
        "grade": grade,
        "feedback": feedback,
        "matched_topic": "general"
    }
