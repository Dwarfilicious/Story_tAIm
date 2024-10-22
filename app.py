from dotenv import load_dotenv
import os
import gradio as gr
import requests
import io

from PIL import Image

load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/stable-diffusion-v1-5/stable-diffusion-v1-5"
headers = {"Authorization": "Bearer " + os.getenv("HUGGINGFACE_TOKEN")}


def query(payload):
    response = requests.post(API_URL, headers = headers, json = payload)

    # Check if the status code indicates success
    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

    return response.content

def generate_image(prompt, neg_prompt):
    payload = {"inputs": prompt, "parameters": {"negative_prompt": neg_prompt}, "seed":-1, "scheduler": "Euler a"}
    print(payload)
    image_bytes = query(payload)

    image = Image.open(io.BytesIO(image_bytes))
    return image

#gradio interface

demo = gr.Interface(
    fn = generate_image,
    inputs = "text",
    outputs = "image",

    # Descriptive Stuff
    title = "DnD Companion",
    description = "Start your adventure by providing a promt that describes a scene in your world"
)

with gr.Blocks() as blocks:
    with gr.Row():
        with gr.Column(scale=3):
            prompt = gr.Textbox(label = "Prompt")
            neg_prompt = gr.Textbox(label="Negative Prompt")

        submit_btn = gr.Button("Submit")

    output = gr.Image(label = "Output Image", scale=0, height=512, width=512)

    submit_btn.click(fn = generate_image, inputs=[prompt, neg_prompt], outputs=output)

if __name__ == "__main__":
    blocks.launch(share=False)
