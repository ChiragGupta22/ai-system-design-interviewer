
import gradio as gr

from bi_encoder import generate_embedding
from cross_encoder import evaluate_answer


def embedding_api(text):
    return generate_embedding(text)


def cross_encoder_api(candidate_answer, expected_answer):
    return evaluate_answer(
        candidate_answer,
        expected_answer
    )


with gr.Blocks() as demo:

    gr.Markdown("# AI Interviewer Model API")

    with gr.Tab("Bi Encoder"):

        text = gr.Textbox(label="Text")

        output = gr.JSON()

        btn = gr.Button("Generate Embedding")

        btn.click(
            embedding_api,
            inputs=text,
            outputs=output,
            api_name="embedding"
        )

    with gr.Tab("Cross Encoder"):

        candidate = gr.Textbox(label="Candidate Answer")

        expected = gr.Textbox(label="Expected Answer")

        result = gr.JSON()

        btn = gr.Button("Evaluate")

        btn.click(
            cross_encoder_api,
            inputs=[candidate, expected],
            outputs=result,
            api_name="cross"
        )


demo.queue().launch()
