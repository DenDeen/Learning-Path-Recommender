import os
import urllib.request
from llama_cpp import Llama


def download_file(file_link, filename):
    # Checks if the file already exists before downloading
    if not os.path.isfile(filename):
        urllib.request.urlretrieve(file_link, filename)
        print("File downloaded successfully.")
    else:
        print("File already exists.")


def get_model(model_path, filename):
    download_file(model_path, filename)
    return Llama(model_path=filename, n_ctx=512, n_batch=126)


def get_llm_generator(
    prompt,
    llm,
    max_tokens=512,
    temperature=0,
    top_p=0.9,
    echo=False,
    stop=["[INST]"],
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
    stop=["[INST]"],
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


def generate_chat_prompt(prompt, size="large"):
    system = ("You are a helpful bot that answers any questions the user may have. Only answer in short clear "
              "sentences.")
    if size == "large":
        chat_prompt_template = f"<s>[INST] {system} [/INST]</s>{prompt}"
    else:
        chat_prompt_template = f"""### Assistant: {system}\n\n### Human: {prompt}\n\n### Assistant:"""
    return chat_prompt_template


def generate_skill_extraction_prompt(prompt, size="large"):
    system = ("You are a helpful bot that extracts skills that the user will learn after the given learnings. Only answer in a list of comma separated words in between curly brackets {}.")
    if size == "large":
        chat_prompt_template = f"<s>[INST] {system} [/INST]</s>{prompt}"
    else:
        chat_prompt_template = f"### Assistant: {system}\n\n### Human: {prompt}\n\n### Assistant:"
    return chat_prompt_template


def process_skill_extraction_prompt(input, prompt):
    if "{" in input and "}" in input:
        return input[input.find("{") + 1 : input.find("}")]
    else:
        return prompt
