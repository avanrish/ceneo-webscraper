def home():
    return 'Hello, World!'


def init_routes(app):
    app.add_url_rule('/', 'home', home)
