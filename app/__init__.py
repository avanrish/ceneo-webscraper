import json
from os import getenv
from flask import Flask
from firebase_admin import credentials, initialize_app
from .routes import init_routes


def create_app():
    app = Flask(__name__)

    cert = json.loads(getenv("FIREBASE_SERVICE_ACCOUNT"))
    cred = credentials.Certificate(cert)
    initialize_app(cred)

    init_routes(app)
    return app
