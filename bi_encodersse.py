
from src.evaluation.bi_encoder import evaluate_answer


expected = """
A scalable video streaming system uses a CDN to deliver
video content from edge locations. Videos are stored in
object storage and transcoded into multiple resolutions.
"""

candidate = """
We can use a CDN to cache videos near users. Store video
files in object storage and transcode them into different
resolutions for streaming.
"""

result = evaluate_answer(candidate, expected)

print(result)
