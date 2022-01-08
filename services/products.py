from models.products import Product
from helpers.responses import Responses
from app import db

from sqlalchemy.exc import SQLAlchemyError

"""
=== Product Services ===
included transactions and logics to access products
"""


class ProductServices(Responses):
    def get_products(self):
        products = Product.query.all()
        product_list = []

        if not products:
            self.set_status(404)
            self.set_content([])

        if products:
            for product in products:
                product_list.append({
                    "id": product.id,
                    "name": product.name,
                    "quantity": product.quantity,
                    "price": product.price
                })

            self.set_status(200)
            self.set_content(product_list)

        return self.get_response()

    def add_product(self, payload):
        try:
            product = Product(**payload)

            db.session.add(product)
            db.session.commit()

            product_dict = {
                "id": product.id,
                "name": product.name,
                "quantity": product.quantity,
                "price": product.price
            }

            self.set_status(200)
            self.set_content(product_dict)

            return self.get_response()

        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])

            self.set_status(400)
            self.set_content(error)

            return self.get_response()


def order_get_product_by_id(product_id):
    product = Product.query.get(product_id)

    return product
