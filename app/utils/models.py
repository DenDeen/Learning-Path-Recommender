import os
import urllib.request

from langchain.embeddings import LlamaCppEmbeddings
from llama_cpp import Llama
from nltk.corpus import stopwords


stop_words = set(stopwords.words("english"))


def download_file(file_link, filename):
    # Checks if the file already exists before downloading
    if not os.path.isfile(filename):
        urllib.request.urlretrieve(file_link, filename)
        print("File downloaded successfully.")
    else:
        print("File already exists.")


def get_model(model_path, filename):
    download_file(model_path, filename)
    return Llama(model_path=filename, n_ctx=1024, n_batch=126)


def embed_specific_query(query, model_path):
    filtered_list = []
    for w in query.split():
        if w.lower() not in stop_words:
            filtered_list.append(w)
    filtered_query = " ".join(filtered_list)

    specific_embedding = LlamaCppEmbeddings(model_path=model_path).embed_query(
        filtered_query
    )
    return specific_embedding


def get_llm_generator(
    prompt,
    llm,
    max_tokens=512,
    temperature=0,
    top_p=0.9,
    echo=False,
    stop=["<|im_end|>"],
):
    text_generator = llm(
        prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        echo=echo,
        stream=True,
        stop=stop,
    )
    return text_generator


def get_llm_generation(
    prompt,
    llm,
    max_tokens=512,
    temperature=0,
    top_p=0.9,
    echo=False,
    stop=["<|im_end|>"],
):
    text_generation = llm(
        prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        echo=echo,
        stop=stop,
    )
    return text_generation["choices"][0]["text"].strip()


def generate_chat_prompt(prompt):
    system_message = "You are a helpful bot that answers any questions about the application with the given user context. The application is an ai powered course recommender. It predicts relevant courses that fit a query calculated with cosine similarity of the embeddings. Only answer in short clear sentences."
    chat_prompt_template = f"<|im_start|>system\n{system_message}<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant"
    return chat_prompt_template


def generate_skill_extraction_prompt(prompt):
    system_message = "You are a helpful bot that extracts skills that the user will learn after the given learnings. Only answer in a list of comma separated words in between curly brackets {}."
    chat_prompt_template = f"<|im_start|>system\n{system_message}<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant"
    return chat_prompt_template


def process_skill_extraction_prompt(input, prompt):
    if "{" in input and "}" in input:
        return input[input.find("{") + 1 : input.find("}")]
    else:
        return prompt
