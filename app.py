import gradio as gr
import requests
import io

from PIL import Image

API_URL = "https://api-inference.huggingface.co/models/sd-community/sdxl-flash"
headers = {"Authorization": "Bearer " + "brother"}


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
    outputs = "image"
)

demo.launch(share = True)
