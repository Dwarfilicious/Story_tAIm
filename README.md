
# Story tAIm

*A web application that helps you bring stories to life!* 

This application uses the gradio frontend framework to integrate four AI models (freely available on HuggingFace) into one well-rounded and user friendly story telling application. 

Story tAIm allows the user to make a query to an LLM with the intending purpose of obtaining a short story as a response. 
The user may also (separately) request an image to be generated to aid in the illustration of the story. 
Furthermore, the story telling experience may be enhanced by generating some background music using the music generator provided or by having an artificially generated voice narrate the story (namely, the output of the request to the LLM) by simply clicking one button. 

The story (or text) is generated using `Llama-3-8B`[^1], a large language model which was developed using a transformer architecture. 
This is then "read outloud" by using a text-to-speech model directly on the output of the language model, namely `
mms-tts-eng `[^2].
The images are generated from a list of positive and negative prompts using the `stable-diffusion-v1-5`[^3] text to image model, which as the name indicates is a diffusion based model. 
Finally, for the music we used `MusicGen-small`[^4] which is also regressive model using a transformer architecture.

[^1]: https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct
[^2]: https://huggingface.co/facebook/mms-tts-eng
[^3]: https://huggingface.co/benjamin-paine/stable-diffusion-v1-5
[^4]: https://huggingface.co/facebook/musicgen-small
## Requirements

In order to get access to the models used in this app you will need to create a HuggingFace access token and include it in a `.env` file as follows:
```
HUGGINGFACE_TOKEN="hf_********************a"
```
To create an access token sign in to your HuggingFace account and go to **Settings -> Access Tokens -> Create New Token**. 
Make sure to select a **Write** token type.

You will also need to install the required python packages. You can do this by running `pip install requirements.txt`

## Running 
Once the requirements are met the web application can be launched by running `python app.py`

Note that this app runs locally, in order to deploy it publicly, you will need to set `share` to `True` in  
```python

if __name__ == "__main__":
    blocks.launch(share=False)

```
