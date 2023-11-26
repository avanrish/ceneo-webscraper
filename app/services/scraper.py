from bs4 import BeautifulSoup
from datetime import datetime
import re
import requests
import math
from app.lib.api_exception import APIException


def extract_product_id(url):
    match = re.search(r'www\.ceneo\.pl/(\d+)', url)
    return match.group(1) if match else None


class Scraper:
    def __init__(self, url):
        self.product_id = extract_product_id(url)
        page_html = requests.get(f'https://www.ceneo.pl/{self.product_id}').text
        self.soup = BeautifulSoup(page_html, 'html.parser')

    def get_product_name(self):
        product_name_tag = self.soup.find('h1', {'class': 'product-top__product-info__name'})
        if product_name_tag is None:
            raise APIException("product.notFound", 400)
        return product_name_tag.text.strip()

    def get_number_of_reviews(self):
        number_of_reviews_tag = self.soup.find("span", {"class": "product-review__qo"}).find("span")
        if number_of_reviews_tag is None:
            raise APIException("product.noReviews", 400)
        return int(number_of_reviews_tag.text.strip())

    def get_average_rating(self):
        average_rating_tag = self.soup.find("span", {"class": "product-review__score"})
        if average_rating_tag is None:
            raise APIException("product.noReviews", 400)
        return float(average_rating_tag['content'])

    def get_all_reviews(self, number_of_reviews):
        pages = min(math.ceil(number_of_reviews / 10), 50)  # Ceneo limits pages to 50
        current_page = 1
        all_reviews = []
        while current_page <= pages:
            page_html = requests.get(f'https://www.ceneo.pl/{self.product_id}/opinie-{current_page}').text
            soup = BeautifulSoup(page_html, 'html.parser')
            reviews_tree = soup('div', {"class": "js_product-review"})
            for review in reviews_tree:
                all_reviews.append(self._extract_review(review))
            current_page += 1
        return all_reviews

    @staticmethod
    def _extract_review(review):
        review_dict = {
            'author': review.find("span", {"class": "user-post__author-name"}).text.strip(),
            'is_recommended': review.find("em", {"class": "recommended"}) is not None,
            'rating': float(
                review.find("span", {"class": "user-post__score-count"}).text.split('/')[0].replace(',', '.')),
            'is_confirmed': review.find("div", {"class": "review-pz"}) is not None
        }
        dates = review.find_all("time")
        review_dict['created_at'] = datetime.strptime(dates[0]["datetime"], "%Y-%m-%d %H:%M:%S")
        review_dict['bought_at'] = datetime.strptime(dates[1]["datetime"], "%Y-%m-%d %H:%M:%S") if len(
            dates) > 1 else None
        review_dict['agree'] = int(review.find("button", {"class": "vote-yes"})['data-total-vote'])
        review_dict['disagree'] = int(review.find("button", {"class": "vote-no"})['data-total-vote'])
        review_dict['content'] = review.find('div', {'class': 'user-post__text'}).text
        review_dict['pros'] = []
        review_dict['cons'] = []
        pros_node = review.find('div', {'class': 'review-feature__title--positives'})
        cons_node = review.find('div', {'class': 'review-feature__title--negatives'})
        if pros_node:
            pros = pros_node.find_next_siblings('div', {'class': 'review-feature__item'})
            for pro in pros:
                review_dict['pros'].append(pro.text)
        if cons_node:
            cons = cons_node.find_next_siblings('div', {'class': 'review-feature__item'})
            for con in cons:
                review_dict['cons'].append(con.text)
        return review_dict
