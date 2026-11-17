
from sentence_transformers import SentenceTransformer, util

# Model will load only when first needed
model = None


def get_model():
    global model

    if model is None:
        print("Loading Bi-Encoder model...", flush=True)

        model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2",
            device="cpu"
        )

        print("Bi-Encoder model loaded!", flush=True)

    return model


def generate_embedding(text: str):
    if not text or not text.strip():
        raise ValueError("Text is required")

    embedding = get_model().encode(
        text,
        convert_to_numpy=True
    )
    print("Embedding shape:", embedding.shape)
    print("Embedding dimensions:", len(embedding))

    return embedding.tolist()


def evaluate_answer(
    candidate_answer: str,
    expected_answer: str,
    max_marks: int = 10
):
    if not candidate_answer.strip() or not expected_answer.strip():
        raise ValueError("Both answers are required")

    current_model = get_model()

    candidate_embedding = current_model.encode(
        candidate_answer,
        convert_to_tensor=True
    )

    expected_embedding = current_model.encode(
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
