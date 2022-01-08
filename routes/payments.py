from flask_restful import Resource
from flask import request
from app import api

from services.payments import PaymentServices


class PaymentResources(Resource, PaymentServices):
    def post(self):
        json_data = request.get_json()
        service = self.create_payment_order(json_data)

        return service


api.add_resource(PaymentResources, "/api/v1/payment-order", endpoint="payment-order")
