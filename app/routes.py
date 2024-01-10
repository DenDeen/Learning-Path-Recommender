from flask import render_template, request, stream_with_context, Response, send_file, session
from app import app
from app.utils import models as model_utils
from app.utils import matching as matching_utils


@app.route("/")
def index_page():
    return render_template("index.html")


@app.route("/input_page")
def input_page():
    return render_template("input.html")


@app.route("/loading_page", methods=["POST"])
def loading_page():
    # Get input from the user
    user_input = request.form.get("input_text")

    # Improve the user_input
    processed_output = model_utils.generate_skill_extraction_prompt(user_input)
    processed_output = model_utils.get_llm_generation(processed_output)
    processed_output = model_utils.process_skill_extraction_prompt(processed_output, user_input)
    print(processed_output)

    # Embed the input and find the best matches
    embedded_output = matching_utils.embed_specific_query(processed_output)
    best_matches = matching_utils.find_best_matches(embedded_output)

    # Convert the best matches to JSON objects
    session['courses'] = matching_utils.convert_df_to_json(best_matches)
    session['user_input'] = user_input
    return render_template("loading.html")


@app.route("/output_page", methods=["GET"])
def output_page():
    # Get the predicted courses from the session
    predicted_courses = session.get('courses', [])
    user_input = session.get('user_input', [])
    return render_template("output.html", courses=predicted_courses, user_input=user_input)


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


@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    processed_input = model_utils.generate_chat_prompt(user_input)
    llm_output = model_utils.get_llm_generation(processed_input)

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
