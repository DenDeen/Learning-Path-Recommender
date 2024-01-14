from flask import (
    render_template,
    request,
    stream_with_context,
    Response,
    send_file,
    session,
    jsonify,
)
from app import app
from app.utils import models as model_utils
from app.utils import matching as matching_utils


model_path = "https://huggingface.co/TheBloke/dolphin-2.6-mistral-7B-dpo-laser-GGUF/resolve/main/dolphin-2.6-mistral-7b-dpo-laser.Q3_K_S.gguf"
filename = "input/dolphin-2.6-mistral-7b-dpo-laser.Q3_K_S.gguf"
global current_model
global embedder


def load_model():
    # Unload the current model if it exists
    global current_model

    current_model = model_utils.get_model(model_path, filename)

    return current_model


@app.route("/")
def index_page():
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
    load_model()

    user_input = session.get("user_input", "")

    # Embed the input and find the best matches
    embedded_output = model_utils.embed_specific_query(user_input, filename)
    best_matches = matching_utils.find_best_matches(embedded_output, user_input, 9)

    # Convert the best matches to JSON objects and Store the results in the session
    session["courses"] = matching_utils.convert_df_to_json(best_matches)

    # Generate similarity matrix and embedding comparison
    # matching_utils.generate_similarity_matrix()
    # matching_utils.generate_embedding_similarity(embedded_output)

    return jsonify({"success": True, "courses": session["courses"]})


@app.route("/output_page", methods=["GET"])
def output_page():
    # Get the predicted courses from the session
    predicted_courses = session.get("courses", [])
    return render_template(
        "output.html", courses=predicted_courses, user_input=session.get("user_input", "")
    )


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


@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    processed_input = model_utils.generate_chat_prompt(user_input)
    streamer = model_utils.get_llm_generator(processed_input, current_model)

    buffer = []
    buffer_size = 3

    def generate():
        for word in streamer:
            buffer.append(word["choices"][0]["text"])
            if len(buffer) >= buffer_size:
                yield "".join(buffer)
                buffer.clear()
        if buffer:
            yield " ".join(buffer)

    return Response(stream_with_context(generate()))
