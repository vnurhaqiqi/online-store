from models.products import Product
from app import db

from sqlalchemy.exc import SQLAlchemyError


def get_all_products():
    products = Product.query.all()
    product_list = []

    if products:
        for product in products:
            product_list.append({
                "id": product.id,
                "name": product.name,
                "quantity": product.quantity,
                "price": product.price
            })

    return product_list


def add_product_data(payload):
    name = payload["name"]
    quantity = payload["quantity"]
    price = payload["price"]

    try:
        product = Product(name=name, quantity=quantity, price=price)

        db.session.add(product)
        db.session.commit()

        return product

    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])

        return error
