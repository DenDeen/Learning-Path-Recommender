from flask import (
    render_template,
    request,
    stream_with_context,
    Response,
    send_file,
    session, jsonify,
)
from app import app
from app.utils import models as model_utils
from app.utils import matching as matching_utils


large_model_path = "https://huggingface.co/TheBloke/Mistral-7B-v0.1-GGUF/resolve/main/mistral-7b-v0.1.Q4_K_M.gguf"
small_model_path = "https://huggingface.co/TheBloke/phi-2-dpo-GGUF/resolve/main/phi-2-dpo.Q5_K_S.gguf	"
large_filename = "input/mistral-7b-v0.1.Q4_K_M.gguf"
small_filename = "input/phi-2-dpo.Q5_K_S.gguf"
global current_model


def load_model(model_size):
    # Unload the current model if it exists
    global current_model

    # Load the desired model
    if model_size == "large":
        current_model = model_utils.get_model(large_model_path, large_filename)
    elif model_size == "small":
        current_model = model_utils.get_model(small_model_path, small_filename)

    return current_model


@app.route("/")
def index_page():
    session["size"] = "large"
    load_model(session["size"])
    return render_template("index.html")


@app.route("/input_page")
def input_page():
    return render_template("input.html")


@app.route("/loading_page", methods=["POST"])
def loading_page():
    # Save the user input in the session
    session["user_input"] = request.form.get("input_text")

    return render_template("loading.html")


@app.route("/process_input", methods=["POST"])
def process_input():
    user_input = session.get("user_input", "")
    size = session["size"]

    # Improve the user_input
    # processed_output = model_utils.generate_skill_extraction_prompt(user_input, size)
    # processed_output = model_utils.get_llm_generation(processed_output, current_model)
    # print(f"Processed output: {processed_output}")
    # processed_output = model_utils.process_skill_extraction_prompt(
    #     processed_output, user_input
    # )

    # Embed the input and find the best matches
    embedded_output = matching_utils.embed_specific_query(processed_output)
    best_matches = matching_utils.find_best_matches(embedded_output)

    # Convert the best matches to JSON objects and Store the results in the session
    session["courses"] = matching_utils.convert_df_to_json(best_matches)
    return jsonify({"success": True, "courses": session["courses"]})


@app.route("/output_page", methods=["GET"])
def output_page():
    # Get the predicted courses from the session
    predicted_courses = session.get("courses", [])
    return render_template("output.html", courses=predicted_courses)


@app.route("/output")
def output():
    return render_template("output.html")


@app.route("/survey")
def survey():
    return render_template("survey.html")


@app.route("/download")
def download_file():
    # Path to the file you want to serve
    file_path = "static/resources/informatiebrief.pdf"
    return send_file(file_path, as_attachment=True)


@app.route("/account_page")
def account_page():
    return render_template("account.html")


@app.route("/switch_model", methods=["POST"])
def switch_model():
    # Get the model size from the user
    model_size = request.form.get("model_size")
    session["size"] = model_size

    # # Flush the memory and the session
    # # also check llamacpp code for flushing memory
    # session.clear()

    # Download the model
    load_model(model_size)

    print(f"Successfully switched to the {model_size} model.")
    return Response(f"Successfully switched to the {model_size} model.")


@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    processed_input = model_utils.generate_chat_prompt(user_input, session["size"])
    llm_output = model_utils.get_llm_generation(processed_input, current_model)

    return Response(llm_output)


# @app.route("/chat", methods=["POST"])
# def chat():
#     user_input = request.json.get("message")
#     processed_input = model_utils.generate_chat_prompt(user_input)
#     streamer = model_utils.get_llm_generator(processed_input)
#
#     buffer = []
#     buffer_size = 3
#
#     def generate():
#         for word in streamer:
#             buffer.append(word["choices"][0]["text"].strip())
#             if len(buffer) >= buffer_size:
#                 yield " ".join(buffer)
#                 buffer.clear()
#         if buffer:
#             yield " ".join(buffer)
#
#     return Response(stream_with_context(generate()))
