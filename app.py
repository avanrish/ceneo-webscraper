from flask import Flask, make_response, render_template, url_for

app = Flask(__name__)

@app.route('/')
def home():
    url_for('static', filename='index.css')
    res = render_template('homepage.html')
    return res

# @app.errorhandler(404)
# def not_found():
#     return make_response(
#         render_template("404.html"),
#         404
#      )