from models.orders import Order, OrderDetail
from services.products import *
from helpers.responses import Responses
from app import db
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError


class OrderServices(Responses):
    def get_order_by_id(self, order_id):
        order = Order.query.get(order_id)

        # check order is exist or not
        if not order:
            self.set_status(404)
            self.set_content("order not found")

            return self.get_response()

        # call function to get all order details
        order_details = self.get_order_detail_order_id(order_id)
        total_order_amount = 0.0

        # calculate total order details amount
        # only order with available quantity will be calculated
        for detail in order_details:
            if detail["product_status"]["status"] == "available":
                total_order_amount += detail["amount"]

        order_dict = {
            "id": order.id,
            "order_date": order.order_date.strftime("%m-%d-%Y %H:%M:%S"),
            "status": order.status,
            "total_amount": total_order_amount,
            "order_details": order_details
        }

        self.set_status(200)
        self.set_content(order_dict)

        return self.get_response()

    def add_order(self, payload):
        products = payload["products"]

        try:
            # check the products are not empty
            if not products:
                self.set_status(400)
                self.set_content("products must be filled")

                return self.get_response()

            order = Order(order_date=datetime.now(), status="draft")

            db.session.add(order)
            db.session.commit()

            order_details = []

            # after check products in request
            # check product if it exists or not
            for p in products:
                product = order_get_product_by_id(p["product_id"])

                # if the product is not exist
                # it will give an error message and transaction cannot be continued
                if not product:
                    self.set_status(404)
                    self.set_content("product not found")

                    return self.get_response()

                # check ordered quantity
                # handle condition if the available quantity reduce before
                # the order details created
                if p["quantity"] > product.quantity:
                    self.set_status(400)
                    self.set_content("order quantity is greater than available quantity")

                    return self.get_response()

                order_detail_dict = {
                    "order_id": order.id,
                    "product_id": p["product_id"],
                    "quantity": p["quantity"],
                    "price": product.price
                }

                # create order details
                # create process is in another function
                create_order_detail = self.create_order_details(order_detail_dict)
                order_details.append(create_order_detail)

            order_dict = {
                "id": order.id,
                "order_date": order.order_date.strftime("%m-%d-%Y %H:%M:%S"),
                "status": order.status,
                "order_details": order_details
            }

            self.set_status(200)
            self.set_content(order_dict)

            return self.get_response()

        except SQLAlchemyError as e:
            error = str(e.__dict__)

            self.set_status(400)
            self.set_content(error)

            return self.get_response()

    def get_order_detail_order_id(self, order_id):
        # function to get all order details
        order_details = OrderDetail.query.filter_by(order_id=order_id).all()
        order_details_list = []

        if order_details:
            for detail in order_details:
                total_amount = detail.quantity * detail.price

                # call function to check available quantity all products ordered
                # status: available, not_available
                status = check_product_available_quantity(detail.product_id)

                order_details_list.append({
                    "id": detail.id,
                    "product_id": detail.product_id,
                    "quantity": detail.quantity,
                    "price": detail.price,
                    "amount": total_amount,
                    "product_status": status
                })

        return order_details_list

    def create_order_details(self, payload):
        # here is function to create the details
        # we can only call this function in this file
        order_detail = OrderDetail(order_id=payload["order_id"], quantity=payload["quantity"],
                                   product_id=payload["product_id"], price=payload["price"])

        db.session.add(order_detail)
        db.session.commit()

        total_amount = payload["quantity"] * payload["price"]

        order_detail_dict = {
            "id": order_detail.id,
            "order_id": order_detail.order_id,
            "product_id": payload["product_id"],
            "quantity": order_detail.quantity,
            "price": order_detail.price,
            "amount": total_amount
        }

        return order_detail_dict

    def checkout_order(self, payload):
        order = Order.query.get(payload["order_id"])
