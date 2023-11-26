from flask import Blueprint, jsonify, request
from .lib.api_exception import APIException
from .services.scraper import Scraper
from .services.store import Store

api = Blueprint('api', __name__)


@api.route('/products', methods=['POST'])
def scrape_product():
    data = request.get_json()
    if not data or data['productUrl'].strip() == '':
        raise APIException("productUrl.empty", 400)
    scraper = Scraper(data['productUrl'])
    product_name = scraper.get_product_name()
    amount_of_reviews = scraper.get_amount_of_reviews()
    average_rating = scraper.get_average_rating()
    reviews = scraper.get_all_reviews(amount_of_reviews)
    amount_of_pros = sum([len(review['pros']) for review in reviews])
    amount_of_cons = sum([len(review['cons']) for review in reviews])
    product_info = {"product_name": product_name, "amount_of_reviews": amount_of_reviews,
                    "average_rating": average_rating, "amount_of_pros": amount_of_pros,
                    "amount_of_cons": amount_of_cons}
    product_ref = Store.set_product(scraper.product_id, product_info, reviews)
    return jsonify({"product_id": product_ref.id})


@api.errorhandler(APIException)
def handle_custom_exception(error):
    response = jsonify(message=error.message)
    response.status_code = error.status_code
    return response
