import os
import urllib.request
import numpy as np
from numpy.linalg import norm
# from llama_cpp import Llama
# from langchain.embeddings import LlamaCppEmbeddings

# parameters 
# ggml_model_path = "https://huggingface.co/TheBloke/Mistral-7B-v0.1-GGUF/resolve/main/mistral-7b-v0.1.Q4_K_M.gguf"
# filename = "mistral-7b-v0.1.Q4_K_M.gguf"
# llm = Llama(model_path=filename, n_ctx=512, n_batch=126)
# llama = LlamaCppEmbeddings(model_path=filename)
# text = "This is a test."
# query_result = llama.embed_query(text)
# doc_result = llama.embed_documents(["This is a test.", "This is test number two.", "this not a test."])

def download_file(file_link, filename):
    # Checks if the file already exists before downloading
    if not os.path.isfile(filename):
        urllib.request.urlretrieve(file_link, filename)
        print("File downloaded successfully.")
    else:
        print("File already exists.")
        
def generate_text(
    prompt="What are you and what is your purpose?",
    max_tokens=256,
    temperature=0,
    top_p=0.5,
    echo=False,
    stop=["#"],
):
    output = llm(
        prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        echo=echo,
        stop=stop,
    )
    output_text = output["choices"][0]["text"].strip()
    return output_text


def generate_prompt_from_template(input):
    chat_prompt_template = f"""
    <|im_start|>system
    You are a helpful bot that extracts all the necessary skills the user needs to learn the described learnings. Only answer in a list of square brackets [].
    <|im_end|>
    <|im_start|>user
    {input}
    <|im_end|>"""
    return chat_prompt_template


def get_top_suggestions(input):
    
    return top_suggestions

# download_file(ggml_model_path, filename)

# prompt = generate_prompt_from_template(
#     "I want to learn to become a computer scientist specialised in machine learning."
# )

# generate_text(
#     prompt=prompt,
#     max_tokens=128,
# )

# np.dot(query_result,doc_result[2])/(norm(query_result)*norm(doc_result[2]))



