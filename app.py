from dotenv import load_dotenv
import os
import gradio as gr
import requests
import io

from PIL import Image

load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/sd-community/sdxl-flash"
headers = {"Authorization": "Bearer " + os.getenv("HUGGINGFACE_TOKEN")}


def query(payload):
    response = requests.post(API_URL, headers = headers, json = payload)

    # Check if the status code indicates success
    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

    return response.content

def generate_image(prompt):
    image_bytes = query({"inputs": prompt})

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
    prompt = gr.Textbox(label = "Prompt")
    output = gr.Image(label = "Output Image")
    submit_btn = gr.Button("Submit")
    submit_btn.click(fn = generate_image, inputs=prompt, outputs=output)

blocks.launch(share = True)
