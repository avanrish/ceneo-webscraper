import json
from os import getenv
from flask import Flask
from firebase_admin import credentials, initialize_app
from .web_routes import web
from .api_routes import api


def create_app():
    app = Flask(__name__)

    cert = json.loads(getenv("FIREBASE_SERVICE_ACCOUNT"))
    cred = credentials.Certificate(cert)
    initialize_app(cred)

    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(web)
    return app
