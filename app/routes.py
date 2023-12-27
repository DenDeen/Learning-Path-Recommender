from flask import render_template
from app import app

@app.route('/')
def home():
    return render_template('index.html')

# Define what you want to learn
@app.route('/learningpath')
def learningpath():
    return render_template('learningpath.html')

# Explanations page
@app.route('/recommendation')
def recommendation():
    return render_template('recommendation.html')

if __name__ == '__main__':
    app.run(debug=True)