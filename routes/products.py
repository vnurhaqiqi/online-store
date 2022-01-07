from flask_restful import Resource
from app import api

from controllers.products import ProductServices


class ProductResource(Resource, ProductServices):
    def get(self):
        service = self.get_products()

        return service


api.add_resource(ProductResource, "/api/v1/products", endpoint="get-all-products")
