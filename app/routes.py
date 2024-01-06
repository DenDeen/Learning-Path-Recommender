from flask import render_template, request, stream_with_context, Response, send_file
from app import app
from app.utils import models as model_utils

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/input", methods=["GET", "POST"])
def input_text():
    if request.method == "POST":
        input_text = request.form["input_text"]
        # Process input_text using your model_utils
        # You may want to store the processed data in a session variable
        return render_template("predictions.html", input_text=input_text)
    return render_template("input.html")


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


@app.route("/predictions", methods=["GET", "POST"])
def view_predictions():
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


@app.route("/output")
def output():
    # Get processed data from the session variable
    # You can now display the output and integrate chat functionality
    return render_template("output.html")

@app.route("/survey")
def survey():
    # Get processed data from the session variable
    # You can now display the output and integrate chat functionality
    return render_template("survey.html")

@app.route('/download')
def download_file():
    # Path to the file you want to serve
    file_path = 'static/resources/informatiebrief.pdf'
    return send_file(file_path, as_attachment=True)