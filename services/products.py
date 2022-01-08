from models.products import Product
from helpers.responses import Responses
from helpers.safety_stock import calculate_safety_stock
from app import db

from sqlalchemy.exc import SQLAlchemyError


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

    def check_all_products_stock(self):
        safety_stocks = calculate_safety_stock()

        if not safety_stocks:
            self.set_status(200)
            self.set_content("no ordered products")

            return self.get_response()

        self.set_status(200)
        self.set_content(safety_stocks)

        return self.get_response()
