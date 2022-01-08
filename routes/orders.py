from flask_restful import Resource
from flask import request
from app import api

from services.orders import OrderServices


class OrderResources(Resource, OrderServices):
    def get(self, order_id):
        service = self.get_order_by_id(order_id)

        return service

    def post(self):
        json_data = request.get_json()
        service = self.add_order(json_data)

        return service


class CheckoutOrderResource(Resource, OrderServices):
    def post(self):
        json_data = request.get_json()
        service = self.checkout_order(json_data)

        return service


api.add_resource(OrderResources, "/api/v1/create-order", endpoint="create-order")
api.add_resource(OrderResources, "/api/v1/order/<order_id>", endpoint="get-order-by-id")
api.add_resource(CheckoutOrderResource, "/api/v1/checkout-order", endpoint="checkout-order")
