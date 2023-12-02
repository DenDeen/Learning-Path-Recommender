from flask import render_template, request
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


@app.route("/predictions", methods=["GET", "POST"])
def view_predictions():
    if request.method == "POST":
        # Get user tweaks and reprocess if needed
        # Update the processed data in the session variable
        return render_template("predictions.html")
    return render_template("predictions.html")


@app.route("/output")
def output():
    # Get processed data from the session variable
    # You can now display the output and integrate chat functionality
    return render_template("output.html")
