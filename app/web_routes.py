from flask import Blueprint, render_template
from .services.store import Store

web = Blueprint('web', __name__)


@web.route('/')
def home():
    return render_template('home/page.html')


@web.route('/products')
def products():
    return render_template('products/page.html')


@web.route('/products/<product_id>')
def product(product_id):
    product = Store.get_product(product_id)
    if product is None:
        return render_template('product/not-found.html'), 404
    return render_template('product/page.html')


@web.route('/<path:path>')
def catch_all(path):
    return render_template('404.html', hide_navigation=True), 404
