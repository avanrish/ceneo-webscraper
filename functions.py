from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
from io import BytesIO
import base64
import numpy as np
import math
import requests

def fetch_opinions(id):
    URL = f"https://www.ceneo.pl/{id}"
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, "lxml")
    title = soup.find("h1", {"class": "product-top__product-info__name"}).text
    amount_of_opinions = int(soup.find("span", {"class": "product-review__qo"}).find("span").text)
    rating = float(soup.find("span", {"class": "product-review__score"})['content'])
    pages = math.ceil(amount_of_opinions / 10)
    pros_amount = 0
    cons_amount = 0
    all_reviews = []
    for i in range(1, pages + 1 if pages <= 50 else 51):
        URL = f"https://www.ceneo.pl/{id}/opinie-{i}"
        page = requests.get(URL)
        soup = BeautifulSoup(page.text, "lxml")
        opinions_tree = soup('div', {"class": "js_product-review"})
        for div in opinions_tree:
            obj = {}
            obj['id'] = div['data-entry-id']
            obj['author'] = div.find("span", {"class": "user-post__author-name"}).text.strip()
            obj['recommendation'] = div.find("span", {"class": "user-post__author-recomendation"}).find("em").text if div.find("span", {"class": "user-post__author-recomendation"}) else ''
            obj['rating'] = div.find("span", {"class": "user-post__score-count"}).text.split('/')[0]
            obj['confirmed'] = True if div.find("div", {"class": "review-pz"}) else False
            obj['opinion_date'] = formatDate(div("time")[0]["datetime"])
            obj['buy_date'] = formatDate(div("time")[1]["datetime"]) if len(div("time")) > 1 else ''
            obj['like'] = int(div.find("button", {"class": "vote-yes"}).find("span").text)
            obj['dislike'] = int(div.find("button", {"class": "vote-no"}).find("span").text)
            obj['text'] = div.find('div', {'class': 'user-post__text'}).text
            obj['pros'] = []
            obj['cons'] = []
            pros_node = div.find('div', {'class': 'review-feature__title--positives'})
            cons_node = div.find('div', {'class': 'review-feature__title--negatives'})
            if pros_node:
                review_items = pros_node.find_next_siblings('div', {'class': 'review-feature__item'})
                pros_amount += len(review_items)
                for i in review_items:
                    obj['pros'].append(i.text)
            if cons_node:
                review_items = cons_node.find_next_siblings('div', {'class': 'review-feature__item'})
                cons_amount += len(review_items)
                for i in review_items:
                    obj['cons'].append(i.text)
            all_reviews.append(obj)
    return {"title": title, "no_of_reviews": amount_of_opinions, "rating": rating, "pros": pros_amount, "cons": cons_amount, "reviews": all_reviews}

def formatDate(date):
    return '.'.join(date.split(' ')[0].split('-')[::-1])
    
def pieChart(recs):
    labels = ['Poleca', 'Nie poleca']
    data = np.array([recs['good'], recs['bad']])
    fig = plt.figure(figsize =(10, 7))
    plt.pie(data, labels = labels, autopct=lambda val: data[ np.abs(data - val/100.*data.sum()).argmin() ])
    plt.title('Rozk??ad rekomendacji')
    tmpfile = BytesIO()
    fig.savefig(tmpfile, format='png')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
    img = '<img src=\'data:image/png;base64,{}\'>'.format(encoded)
    return img

def barChart(stars):
    rating = []
    values = []
    for k, v in stars.items():
        if v > 0:
            rating.append(k)
            values.append(v)

    fig = plt.figure(figsize = (10, 5))
    plt.bar(rating, values, width = 0.4 )
    plt.xlabel("Ocena (w gwiazdkach)")
    plt.ylabel("Liczba os??b")
    plt.title("Rozk??ad ocen")
    for k, v in enumerate(values):
        plt.text(k, v + 3, str(v), ha='center')
    tmpfile = BytesIO()
    fig.savefig(tmpfile, format='png')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
    img = '<img src=\'data:image/png;base64,{}\'>'.format(encoded)
    return img