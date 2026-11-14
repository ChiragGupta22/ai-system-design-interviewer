
from sentence_transformers import CrossEncoder

model = None


def get_model():
    global model

    if model is None:
        print("Loading Cross-Encoder model...")

        model = CrossEncoder(
            "cross-encoder/stsb-roberta-base",
            device="cpu"
        )

    return model


def evaluate_answer(
    candidate_answer: str,
    expected_answer: str,
    max_marks: int = 10
):
    if not candidate_answer.strip() or not expected_answer.strip():
        raise ValueError("Both answers are required")

    cross_encoder = get_model()

    score = cross_encoder.predict(
        [(candidate_answer, expected_answer)]
    )[0]

    similarity = max(0.0, min(1.0, float(score)))

    marks = round(similarity * max_marks, 2)

    return {
        "similarity_score": round(similarity, 4),
        "marks": marks,
        "max_marks": max_marks
    }
