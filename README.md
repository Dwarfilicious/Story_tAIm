
# Story tAIm
A web application that helps you bring stories to life! 

This application uses the gradio frontend framework to integrate 4 AI models freely available on HuggingFace into one well-rounded story telling application. 

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
