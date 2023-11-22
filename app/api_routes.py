from flask import Blueprint, jsonify, request
from .lib.api_exception import APIException
from .services.scraper import Scraper

api = Blueprint('api', __name__)


@api.route('/products', methods=['POST'])
def scrape_product():
    data = request.get_json()
    if not data or data['productUrl'].strip() == '':
        raise APIException("productUrl.empty", 400)
    scraper = Scraper(data['productUrl'])
    product_name = scraper.get_product_name()
    number_of_reviews = scraper.get_number_of_reviews()
    average_rating = scraper.get_average_rating()
    reviews = scraper.get_all_reviews(number_of_reviews)
    total_pros = sum([len(review['pros']) for review in reviews])
    total_cons = sum([len(review['cons']) for review in reviews])
    return jsonify(data)


@api.errorhandler(APIException)
def handle_custom_exception(error):
    response = jsonify(message=error.message)
    response.status_code = error.status_code
    return response
