from dotenv import load_dotenv
import os
import gradio as gr
import requests
import io

from PIL import Image
from huggingface_hub import InferenceClient

load_dotenv()

API_URL_IMAGE = "https://api-inference.huggingface.co/models/stable-diffusion-v1-5/stable-diffusion-v1-5"
API_URL_AUDIO = "https://api-inference.huggingface.co/models/facebook/musicgen-small"
API_URL_TOSPEECH = "https://api-inference.huggingface.co/models/facebook/mms-tts-eng"

RESPONSE = False

headers = {"Authorization": "Bearer " + os.getenv("HUGGINGFACE_TOKEN")}

client = InferenceClient(api_key=os.getenv("HUGGINGFACE_TOKEN"))

def query(payload, api_url):
    response = requests.post(api_url, headers = headers, json = payload)

    # Check if the status code indicates success
    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

    return response.content

def generate_image(prompt, neg_prompt):
    payload = {"inputs": prompt, "parameters": {"negative_prompt": neg_prompt}, "seed":-1, "scheduler": "Euler a"}
    image_bytes = query(payload, API_URL_IMAGE)

    image = Image.open(io.BytesIO(image_bytes))
    return image

def generate_audio(prompt):
    audio_bytes = query({"inputs": prompt}, API_URL_AUDIO)
    #audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format="mp3")  # e.g., "mp3", "wav", etc.
    return audio_bytes

def generate_speech(prompt):
    speech_bytes = query({"inputs": prompt}, API_URL_TOSPEECH)
    return speech_bytes

def chatbot_response(message):
    # Make the request to the model
    response = client.chat_completion(
        model="meta-llama/Meta-Llama-3-8B-Instruct",
        messages=[{"role": "user", "content": message}],
        max_tokens=500,
        stream=False,  # Set to False to get the complete response
    )

    # The response should be a single string now
    content = response.choices[0].message.content

    return content, gr.Button("Narrate", interactive=True)
#gradio interface


with gr.Blocks() as blocks:
    gr.Markdown("## Chatbot")
    chat_input = gr.Textbox(label="Type your message")
    chat_output = gr.Textbox(label="Response", interactive=False)
    chat_submit_btn = gr.Button("Send")

    speech_output = gr.Audio(label="Response Audio")
    speech_submit_btn = gr.Button("Narrate", interactive=False)

    chat_submit_btn.click(fn=chatbot_response, inputs=chat_input, outputs=[chat_output, speech_submit_btn])
    
    speech_submit_btn.click(fn = generate_speech, inputs=chat_output, outputs=speech_output)
    

    with gr.Row():
        with gr.Column(scale=3):
            prompt = gr.Textbox(label = "Prompt")
            neg_prompt = gr.Textbox(label="Negative Prompt")

        submit_btn = gr.Button("Submit Image Prompt")

    output = gr.Image(label = "Output Image", scale=0, height=512, width=512)

    submit_btn.click(fn = generate_image, inputs=[prompt, neg_prompt], outputs=output)

    audio_prompt = gr.Textbox(label ="Music Prompt")
    audio_output = gr.Audio(label="Output Music")
    audio_submit_btn = gr.Button("Submit Music Prompt")
    audio_submit_btn.click(fn = generate_audio, inputs=audio_prompt, outputs=audio_output)
    

if __name__ == "__main__":
    blocks.launch(share=False)
