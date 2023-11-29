import math
from firebase_admin import firestore

page_limit = 2


class Store:

    @staticmethod
    def set_product(product_id, product_info, reviews):
        product_ref = firestore.client().collection('products').document(product_id)
        product_ref.set({**product_info, "reviews": reviews, "created_at": firestore.SERVER_TIMESTAMP})
        return product_ref

    @staticmethod
    def get_product(product_id):
        product_ref = firestore.client().collection('products').document(product_id)
        product = product_ref.get()
        if not product.exists:
            return None
        return product.to_dict()

    @staticmethod
    def get_paginated_products(page):
        collection_ref = firestore.client().collection('products')
        result = collection_ref.count().get()
        amount_of_docs = result[0][0].value
        total_pages = math.ceil(amount_of_docs / page_limit)
        if page > total_pages:
            page = total_pages
        if page < 1:
            page = 1
        docs = collection_ref.order_by('created_at').limit(page_limit).offset(page_limit * (page - 1)).get()
        converted_docs = []
        for doc in docs:
            doc_dict = doc.to_dict()
            doc_dict['id'] = doc.id
            doc_dict['created_at'] = doc_dict['created_at'].strftime('%d/%m/%Y %H:%M')
            converted_docs.append(doc_dict)
        metadata = {"items_per_page": page_limit, "total_items": amount_of_docs, "current_page": page,
                    "total_pages": total_pages}
        return converted_docs, metadata
