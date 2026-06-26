
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from functools import lru_cache


@lru_cache(maxsize=1)
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


def evaluate_answer(question, answer, reference_answer):
    """
    Evaluates the user's answer by comparing it with an expected
    reference answer using semantic similarity.
    """

    if not answer or len(answer.strip()) < 5:
        return {
            "score": 0,
            "grade": "Weak",
            "feedback": ["Your answer is too short."],
            "matched_topic": "general"
        }

    model = load_model()

    embeddings = model.encode(
        [answer, reference_answer]
    )

    answer_vec = embeddings[0].reshape(1, -1)
    reference_vec = embeddings[1].reshape(1, -1)

    similarity = float(
        cosine_similarity(
            answer_vec,
            reference_vec
        )[0][0]
    )

    # -----------------------------
    # Score Mapping
    # -----------------------------

    if similarity >= 0.82:
        score = 5
        grade = "Excellent"
        feedback = [
            "Excellent answer.",
            "Your explanation closely matches the expected concept."
        ]

    elif similarity >= 0.70:
        score = 4
        grade = "Strong"
        feedback = [
            "Good answer.",
            "Most important concepts were covered."
        ]

    elif similarity >= 0.55:
        score = 3
        grade = "Average"
        feedback = [
            "Reasonable answer.",
            "Some important details are missing."
        ]

    elif similarity >= 0.40:
        score = 2
        grade = "Fair"
        feedback = [
            "Partial understanding.",
            "Try explaining the concept more clearly."
        ]

    else:
        score = 1
        grade = "Weak"
        feedback = [
            "The answer does not sufficiently match the expected concept."
        ]

    return {
        "score": score,
        "grade": grade,
        "feedback": feedback,
        "similarity": round(similarity, 2),
        "matched_topic": "general"
    }
