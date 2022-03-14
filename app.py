from flask import Flask, redirect, render_template, request, url_for
import json

from functions import fetch_opinions

app = Flask(__name__)

@app.route('/')
def home():
    url_for('static', filename='index.css')
    return render_template('homepage.html')

@app.route('/extract', methods=['GET', 'POST'])
def extract():
    if request.method == "POST":
        try:
            id = request.form['product-id']
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
        except:
            return render_template('extract.html', error="Nie znaleziono produktu.")
    else:
        return render_template('extract.html')

@app.route('/products')
def products():
    return '<p>Products</p>'

@app.route('/author')
def author():
    return '<p>Author</p>'

@app.route('/*')
def catch_all():
    url_for('static', filename='index.css')
    return render_template('homepage.html')