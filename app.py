from dotenv import load_dotenv
from pydub import AudioSegment
import os
import gradio as gr
import requests
import io

from PIL import Image
from huggingface_hub import InferenceClient

load_dotenv()

API_URL_IMAGE = "https://api-inference.huggingface.co/models/sd-community/sdxl-flash"
API_URL_AUDIO = "https://api-inference.huggingface.co/models/facebook/musicgen-small"

headers = {"Authorization": "Bearer " + os.getenv("HUGGINGFACE_TOKEN")}

   
    
client = InferenceClient(api_key=os.getenv("HUGGINGFACE_TOKEN"))

def query(payload, api_url):
    response = requests.post(api_url, headers = headers, json = payload)

    # Check if the status code indicates success
    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

    return response.content

def generate_image(prompt):
    image_bytes = query({"inputs": prompt}, API_URL_IMAGE)

    image = Image.open(io.BytesIO(image_bytes))
    return image

def generate_audio(prompt):
    audio_bytes = query({"inputs": prompt}, API_URL_AUDIO)
    print("Hier steht der typ:", type(audio_bytes))
    #audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format="mp3")  # e.g., "mp3", "wav", etc.
    return audio_bytes


def chatbot_response(message):
    # Make the request to the model
    response = client.chat_completion(
        model="meta-llama/Meta-Llama-3-8B-Instruct",
        messages=[{"role": "user", "content": message}],
        max_tokens=500,
        stream=False,  # Set to False to get the complete response
    )
    
    print(type(response))
    # The response should be a single string now
    content = response.choices[0].message.content
    return content
#gradio interface


with gr.Blocks() as blocks:
    
    gr.Markdown("## Chatbot")
    chat_input = gr.Textbox(label="Type your message")
    chat_output = gr.Textbox(label="Response", interactive=False)
    chat_submit_btn = gr.Button("Send")
    chat_submit_btn.click(fn=chatbot_response, inputs=chat_input, outputs=chat_output)


    prompt = gr.Textbox(label = "Prompt")
    output = gr.Image(label = "Output Image")
    submit_btn = gr.Button("Submit")
    submit_btn.click(fn = generate_image, inputs=prompt, outputs=output)

    audio_prompt = gr.Textbox(label ="Audio Prompt")
    audio_output = gr.Audio(label="Output Audio")
    audio_submit_btn = gr.Button("Submit Audio Prompt")
    audio_submit_btn.click(fn = generate_audio, inputs=audio_prompt, outputs=audio_output)
    

blocks.launch(share = True)
