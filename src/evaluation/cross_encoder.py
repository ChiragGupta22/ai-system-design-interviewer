
from sentence_transformers import CrossEncoder


# Load the model once when this module is imported
model = CrossEncoder("cross-encoder/stsb-roberta-base")


def evaluate_answer(
    candidate_answer: str,
    expected_answer: str,
    max_marks: int = 10
):
    if not candidate_answer.strip() or not expected_answer.strip():
        raise ValueError("Both answers are required")

    # Cross-encoder compares both answers together
    score = model.predict(
        [(candidate_answer, expected_answer)]
    )[0]

    # STS-B model scores are generally on a 0-5 scale
    similarity = max(0.0, min(1.0, float(score) / 5.0))

    marks = round(similarity * max_marks, 2)

    return {
        "similarity_score": round(similarity, 4),
        "marks": marks,
        "max_marks": max_marks
    }
