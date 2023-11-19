from flask import Blueprint, jsonify, request
from .lib.api_exception import APIException

api = Blueprint('api', __name__)


@api.route('/products', methods=['POST'])
def api_data():
    data = request.get_json()
    if not data or data['productUrl'].strip() == '':
        raise APIException("productUrl.empty", 400)

    return jsonify(data)


@api.errorhandler(APIException)
def handle_custom_exception(error):
    response = jsonify(message=error.message)
    response.status_code = error.status_code
    return response
