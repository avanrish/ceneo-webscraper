from flask import Flask, make_response, redirect, render_template, url_for
import json

from functions import fetch_opinions

app = Flask(__name__)

@app.route('/')
def home():
    url_for('static', filename='index.css')
    return render_template('homepage.html')

@app.route('/extract')
def extract():
    url_for('static', filename='index.css')
    return render_template('extract.html')

@app.route('/api/extract/<id>')
def get_opinions(id):
    try:
        res = fetch_opinions(id)
        exists = False
        products = []
        with open('products.json') as p:
            products = json.loads(p.read())
            for product in products:
                if product["id"] == id:
                    exists = True
                    break
        if not exists:
            with open('products.json', 'w') as f:
                products.append({"id": id, "title": res["title"]})
                f.write(json.dumps(products))
        with open(f'products/{id}.json', 'w') as item:
            item.write(json.dumps(res["reviews"]))

        return redirect(f'/product/{id}')
    except BaseException as e:
        return make_response('Wrong ID', 400)


@app.route('*')
def catch_all():
    url_for('static', filename='index.css')
    return render_template('homepage.html')