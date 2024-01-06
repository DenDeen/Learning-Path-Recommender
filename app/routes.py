from flask import render_template, request, stream_with_context, Response
from app import app
from app.utils import models as model_utils


@app.route("/")
def index_page():
    return render_template("index.html")


@app.route("/input_page")
def input_page():
    # Logic to get the results
    # ...

    return render_template("input.html")


@app.route("/loading_page", methods=["POST"])
def loading_page():
    # Process form data here
    # ...

    return render_template("loading.html")


@app.route("/output_page", methods=["GET", "POST"])
def output_page():
    courses = [
        {
            "name": "Course 1",
            "description": "Description for Course 1",
            "confidence": 95,
        },
        {
            "name": "Course 2",
            "description": "Description for Course 2",
            "confidence": 90,
        },
        {
            "name": "Course 3",
            "description": "Description for Course 3",
            "confidence": 85,
        },
        {
            "name": "Course 4",
            "description": "Description for Course 4",
            "confidence": 80,
        },
        {
            "name": "Course 5",
            "description": "Description for Course 5",
            "confidence": 75,
        },
    ]

    if request.method == "POST":
        return render_template("predictions.html", courses=courses)

    return render_template("predictions.html", courses=courses)


@app.route("/account_page")
def account_page():
    return render_template("account.html")



@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    buffer = []
    buffer_size = 3

    def generate():
        for token in user_message:
            buffer.append(token)
            if len(buffer) >= buffer_size:
                yield "".join(buffer)
                buffer.clear()
        if buffer:
            yield "".join(buffer)

    return Response(stream_with_context(generate()), content_type="text/plain")


# @app.route("/chat", methods=["POST"])
# def chat():
# user_message = request.json.get("message")
# response = chat_engine.stream_chat(user_message)
# buffer = []
# buffer_size = 3
#
# def generate():
#     for token in response.response_gen:
#         buffer.append(token)
#         if len(buffer) >= buffer_size:
#             yield "".join(buffer)
#             buffer.clear()
#     if buffer:
#         yield "".join(buffer)
#
# return Response(stream_with_context(generate()), content_type="text/plain")