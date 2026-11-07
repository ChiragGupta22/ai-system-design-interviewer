
from sentence_transformers import SentenceTransformer, util

# Load model once
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2",
    device="cpu"
)


def evaluate_answer(
    candidate_answer: str,
    expected_answer: str,
    max_marks: int = 10
):
    if not candidate_answer.strip() or not expected_answer.strip():
        raise ValueError("Both answers are required")

    # Generate both embeddings together
    embeddings = model.encode(
        [candidate_answer, expected_answer],
        convert_to_tensor=True
    )

    similarity = util.cos_sim(
        embeddings[0],
        embeddings[1]
    ).item()

    similarity = max(0.0, min(1.0, similarity))
    marks = round(similarity * max_marks, 2)

    return {
        "similarity_score": round(similarity, 4),
        "marks": marks,
        "max_marks": max_marks
    }
