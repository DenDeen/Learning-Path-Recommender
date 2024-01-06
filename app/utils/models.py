import os
import urllib.request
from llama_cpp import Llama

ggml_model_path = "https://huggingface.co/TheBloke/Mistral-7B-v0.1-GGUF/resolve/main/mistral-7b-v0.1.Q4_K_M.gguf"
filename = "input/mistral-7b-v0.1.Q4_K_M.gguf"

llm = Llama(model_path=filename, n_ctx=512, n_batch=126)


def download_file(file_link, filename):
    # Checks if the file already exists before downloading
    if not os.path.isfile(filename):
        urllib.request.urlretrieve(file_link, filename)
        print("File downloaded successfully.")
    else:
        print("File already exists.")


def get_streamer(prompt, context):
    # Generate llm streamer
    return llm(
        prompt,
        max_tokens=1024,
        temperature=0.1,
        stream=True,
    )
