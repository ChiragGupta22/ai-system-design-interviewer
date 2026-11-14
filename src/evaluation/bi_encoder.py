
from sentence_transformers import SentenceTransformer, util

# Load the model once
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


# Generate embedding
def generate_embedding(text: str):
    if not text or not text.strip():
        raise ValueError("Text is required")

    embedding = model.encode(
        text,
        convert_to_numpy=True
    )

    return embedding.tolist()


def evaluate_answer(
    candidate_answer: str,
    expected_answer: str,
    max_marks: int = 10
):
    if not candidate_answer.strip() or not expected_answer.strip():
        raise ValueError("Both answers are required")

    candidate_embedding = model.encode(
        candidate_answer,
        convert_to_tensor=True
    )

    expected_embedding = model.encode(
        expected_answer,
        convert_to_tensor=True
    )

    similarity = util.cos_sim(
        candidate_embedding,
        expected_embedding
    ).item()

    similarity = max(0.0, min(1.0, similarity))
    marks = round(similarity * max_marks, 2)

    return {
        "similarity_score": round(similarity, 4),
        "marks": marks,
        "max_marks": max_marks
    }
