from flask import Flask, redirect, render_template, request, send_file, url_for
import pandas as pd
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
            with open(f'products/{id}.json', 'w') as item:
                item.write(json.dumps(res["reviews"]))
            with open('products.json') as p:
                products = json.loads(p.read())
                for product in products:
                    if product["id"] == id:
                        exists = True
                        break
            if not exists:
                with open('products.json', 'w') as f:
                    del res["reviews"]
                    res["id"] = id
                    products.append(res)
                    f.write(json.dumps(products))
            return redirect(f'/product/{id}')
        except:
            return render_template('extract.html', error="Nie znaleziono produktu.")
    else:
        return render_template('extract.html')

@app.route('/products')
def products():
    with open('products.json') as f:
        data_array = json.loads(f.read())
    url_for('static', filename='index.css')
    return render_template('products.html', prods=data_array)

@app.route('/product/<id>')
def product(id):
    try:
        with open('products.json') as f:
            all_products = json.loads(f.read())
        product = next(item for item in all_products if item['id'] == id)
        with open(f'products/{id}.json') as f2:
            data=json.loads(f2.read())
        headers=['ID', "Autor", "Rekomendacja", "Ocena", "Potwierdzone zakupem", "Data opinii", "Data zakupu", "Przydatna", "Nieprzydatna", "Treść", "Zalety", "Wady"]
        url_for('static', filename='index.css')
        return render_template('product.html', title=product['title'], id=product["id"], data=data, headers=headers)
    except:
        return redirect(url_for('extract'))

@app.route('/product/<id>/stats')
def stats(id):

    return '<p>Stats</p>'

@app.route("/download/<id>/<type>")
def download(id, type):
    df = pd.read_json(f'products/{id}.json')
    if type == "csv":
        df.to_csv('output/output.csv', index=False)
    elif type == "xlsx":
        df.to_excel('output/output.xlsx', index=False)
    else:
        return send_file(f'products/{id}.json')

    return send_file(f'output/output.{type}', download_name=f'{id}.{type}')

@app.route('/author')
def author():
    return '<p>Author</p>'

@app.route('/*')
def catch_all():
    url_for('static', filename='index.css')
    return render_template('homepage.html')