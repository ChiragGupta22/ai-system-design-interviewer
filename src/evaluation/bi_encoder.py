
from sentence_transformers import SentenceTransformer, util


# Load the model once when this module is imported
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def evaluate_answer(
    candidate_answer: str,
    expected_answer: str,
    max_marks: int = 10
):
    if not candidate_answer.strip() or not expected_answer.strip():
        raise ValueError("Both answers are required")

    # Convert both answers into embeddings
    candidate_embedding = model.encode(
        candidate_answer,
        convert_to_tensor=True
    )

    expected_embedding = model.encode(
        expected_answer,
        convert_to_tensor=True
    )

    # Calculate cosine similarity
    similarity = util.cos_sim(
        candidate_embedding,
        expected_embedding
    ).item()

    # Convert similarity into a provisional mark
    similarity = max(0.0, min(1.0, similarity))
    marks = round(similarity * max_marks, 2)

    return {
        "similarity_score": round(similarity, 4),
        "marks": marks,
        "max_marks": max_marks
    }
