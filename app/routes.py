from flask import render_template


def home():
    return render_template('home.html')


def init_routes(app):
    app.add_url_rule('/', 'home', home)
