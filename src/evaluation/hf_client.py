import os
from gradio_client import Client
from dotenv import load_dotenv
load_dotenv()

SPACE_ID = "Chirag56/ai-interviewer-evaluation"
HF_TOKEN = os.getenv("HF_TOKEN")

client = None

def get_client():
    global client

    if client is None:
        client = Client(SPACE_ID, token=HF_TOKEN)

    return client


def generate_embedding(text: str):
    return get_client().predict(
        text,
        api_name="/embedding"
    )


def evaluate_with_cross_encoder(candidate_answer: str, expected_answer: str):
    return get_client().predict(
        candidate_answer,
        expected_answer,
        api_name="/cross"
    )