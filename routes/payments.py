from flask_restful import Resource
from flask import request
from app import api

from services.payments import PaymentServices


class PaymentResources(Resource, PaymentServices):
    def post(self):
        json_data = request.get_json()
        service = self.create_payment_order(json_data)

        return service

    def put(self, payment_id):
        service = self.confirm_payment_order(payment_id)

        return service


api.add_resource(PaymentResources, "/api/v1/payment-order", endpoint="payment-order")
api.add_resource(PaymentResources, "/api/v1/confirm-payment-order/<payment_id>", endpoint="confirm-payment-order")
