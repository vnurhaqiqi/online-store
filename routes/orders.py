from flask_restful import Resource
from flask import request
from app import api

from services.orders import OrderServices


class OrderResources(Resource, OrderServices):
    def post(self):
        json_data = request.get_json()
        service = self.add_order(json_data)

        return service


api.add_resource(OrderResources, "/api/v1/create-order", endpoint="create-order")
