from src.evaluation.bi_encoder import generate_embedding

embedding = generate_embedding(
    "Redis is used for caching frequently accessed data."
)

print("Dimensions:", len(embedding))
print("First 5 values:", embedding[:5])