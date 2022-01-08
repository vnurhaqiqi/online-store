from flask_restful import Resource
from flask import request
from app import api

from services.products import ProductServices


class ProductResource(Resource, ProductServices):
    def get(self):
        service = self.get_products()

        return service

    def post(self):
        json_data = request.get_json()
        service = self.add_product(json_data)

        return service


class CheckProductQuantityResources(Resource, ProductServices):
    def get(self):
        service = self.check_all_products_stock()

        return service


api.add_resource(ProductResource, "/api/v1/products", endpoint="get-all-products")
api.add_resource(ProductResource, "/api/v1/products", endpoint="add-product")
api.add_resource(CheckProductQuantityResources, "/api/v1/check-product-quantity", endpoint="check-product-quantity")
