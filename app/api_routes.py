from flask import Blueprint, jsonify

api = Blueprint('api', __name__)


@api.route('/hello-world')
def api_data():
    return jsonify({'hello': 'world'})
