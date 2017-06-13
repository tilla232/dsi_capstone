from flask import Flask, render_template, request
import sys
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/positions')
def positions():
    return render_template('positions.html')

@app.route('/motivation')
def hello():
    return render_template('motivation.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/model')
def problem():
    return render_template('model.html')

@app.route('/conclusions')
def conclusions():
    return render_template('conclusions.html')

@app.route('/teamneeds', methods=['GET','POST'])
def score():
    return render_template('score_prompt.html', predicted=y)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

# <img src="../static/img/GitHub-Mark-32px.png" alt="github">
