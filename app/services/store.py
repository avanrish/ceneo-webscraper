from firebase_admin import firestore


class Store:

    @staticmethod
    def set_product(product_id, product_info, reviews):
        product_ref = firestore.client().collection('products').document(product_id)
        product_ref.set({**product_info, "reviews": reviews})
        return product_ref

    @staticmethod
    def get_product(product_id):
        product_ref = firestore.client().collection('products').document(product_id)
        product = product_ref.get()
        if not product.exists:
            return None
        return product.to_dict()
