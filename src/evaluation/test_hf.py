
from hf_client import generate_embedding, evaluate_with_cross_encoder

embedding = generate_embedding("Load balancer distributes traffic")

print("Embedding dimensions:", len(embedding))

result = evaluate_with_cross_encoder(
    "A load balancer distributes traffic across servers.",
    "A load balancer distributes incoming requests across multiple backend servers."
)

print("Cross Encoder:", result)
