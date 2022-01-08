from flask_restful import Resource
from flask import request
from app import api

from services.products import ProductServices

"""
=== Product Routes ===
all product routes are places here
"""


class ProductResource(Resource, ProductServices):
    def get(self):
        service = self.get_products()

        return service

    def post(self):
        json_data = request.get_json()
        service = self.add_product(json_data)

        return service


api.add_resource(ProductResource, "/api/v1/products", endpoint="get-all-products")
api.add_resource(ProductResource, "/api/v1/products", endpoint="add-product")
