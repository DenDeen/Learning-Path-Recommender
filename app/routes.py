from flask import render_template
from app import app

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/newpath')
def newpath():
    return render_template('new-path.html')

@app.route('/mypaths')
def mypaths():
    return render_template('my-paths.html')

# @app.route('/path/<int:id>')
