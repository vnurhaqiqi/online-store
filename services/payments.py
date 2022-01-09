from models.payments import Payment
from models.products import Product
from models.orders import Order, OrderDetail
from helpers.responses import Responses
from app import db
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError


class PaymentServices(Responses):
    def get_payment_order_by_id(self, payment_id):
        payment = Payment.query.get(payment_id)

        # check payment data
        # if it exists or not
        if not payment:
            self.set_status(404)
            self.set_content("payment not found")

            return self.get_response()

        order = Order.query.get(payment.order_id)

        # check order data
        if not order:
            self.set_status(404)
            self.set_content("order not found")

            return self.get_response()

        payment_dict = {
            "payment_id": payment.id,
            "order_id": order.id,
            "order_date": order.order_date.strftime("%m-%d-%Y %H:%M:%S"),
            "payment_date": payment.payment_date.strftime("%m-%d-%Y %H:%M:%S"),
            "order_status": order.status,
            "payment_status": payment.status,
            "amount": payment.amount,
            "order_details": []
        }

        order_details = OrderDetail.query.filter_by(order_id=order.id).all()
        for detail in order_details:
            product = Product.query.get(detail.product_id)

            total_amount = (detail.quantity * detail.price)

            payment_dict["order_details"].append({
                "detail_id": detail.id,
                "product_id": product.id,
                "product_name": product.name,
                "quantity": detail.quantity,
                "price": detail.price,
                "amount": total_amount
            })

        self.set_status(200)
        self.set_content(payment_dict)

        return self.get_response()

    def create_payment_order(self, payload):
        try:
            # find order then get total amount
            order = Order.query.get(payload["order_id"])
            total_amount = order.total_amount()

            # check order if exist or not
            if not order:
                self.set_status(404)
                self.set_content("order not found")

                return self.get_response()

            # check order status
            if order.status != "checkout":
                self.set_status(400)
                self.set_content("only order with checkout status can be processed")

                return self.get_response()

            payment = Payment(order_id=payload["order_id"], order_date=order.order_date, status="paid",
                              payment_date=datetime.now(), amount=total_amount, created_date=datetime.now(),
                              updated_date=datetime.now())

            # create payment data base on order data
            # update order status, from checkout to paid
            db.session.add(payment)
            order.status = "paid"

            db.session.commit()

            payment_dict = {
                "id": payment.id,
                "order_id": payment.order_id,
                "order_date": payment.order_date.strftime("%m-%d-%Y %H:%M:%S"),
                "status": payment.status,
                "payment_date": payment.payment_date.strftime("%m-%d-%Y %H:%M:%S"),
                "amount": payment.amount
            }

            self.set_status(200)
            self.set_content(payment_dict)

            return self.get_response()

        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])

            self.set_status(400)
            self.set_content(error)

            return self.get_response()

    def confirm_payment_order(self, payment_id):
        try:
            payment = Payment.query.get(payment_id)

            # check payment data
            # if it exists or not
            if not payment:
                self.set_status(404)
                self.set_content("payment not found")

                return self.get_response()

            # check payment status
            # besides confirmed will be processed
            if payment.status == "confirmed":
                self.set_status(400)
                self.set_content("payment has been confirmed")

                return self.get_response()

            order = Order.query.get(payment.order_id)

            # check order data
            if not order:
                self.set_status(404)
                self.set_content("order not found")

                return self.get_response()

            # update payment and order data
            # payment (status and updated_date)
            # order (status and updated_date)
            payment.status = "confirmed"
            payment.updated_date = datetime.now()
            order.status = "payment_confirmed"
            order.updated_date = datetime.now()

            db.session.commit()

            payment_dict = {
                "id": payment.id,
                "order_id": payment.order_id,
                "order_date": payment.order_date.strftime("%m-%d-%Y %H:%M:%S"),
                "status": payment.status,
                "payment_date": payment.payment_date.strftime("%m-%d-%Y %H:%M:%S"),
                "amount": payment.amount
            }

            self.set_status(200)
            self.set_content(payment_dict)

            return self.get_response()

        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])

            self.set_status(400)
            self.set_content(error)

            return self.get_response()

    def reject_payment_order(self, payment_id):
        try:
            payment = Payment.query.get(payment_id)

            # check payment data
            # if it exists or not
            if not payment:
                self.set_status(404)
                self.set_content("payment not found")

                return self.get_response()

            order = Order.query.get(payment.order_id)

            # check order data
            if not order:
                self.set_status(404)
                self.set_content("order not found")

                return self.get_response()

            # get all order details
            # add ordered quantity to available product quantity
            order_details = OrderDetail.query.filter_by(order_id=order.id).all()
            for detail in order_details:
                product = Product.query.get(detail.product_id)
                product.add_product_quantity(detail.quantity)

            # update payment and order data
            # payment (status and updated_date)
            # order (status and updated_date)
            payment.status = "rejected"
            payment.updated_date = datetime.now()
            order.status = "payment_rejected"
            order.updated_date = datetime.now()

            db.session.commit()

            payment_dict = {
                "id": payment.id,
                "order_id": payment.order_id,
                "order_date": payment.order_date.strftime("%m-%d-%Y %H:%M:%S"),
                "status": payment.status,
                "payment_date": payment.payment_date.strftime("%m-%d-%Y %H:%M:%S"),
                "amount": payment.amount
            }

            self.set_status(200)
            self.set_content(payment_dict)

            return self.get_response()

        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])

            self.set_status(400)
            self.set_content(error)

            return self.get_response()
