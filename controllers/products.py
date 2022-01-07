from services.products import *
from helpers.responses import Responses

from flask import request


class ProductServices(Responses):
    def get_products(self):
        service = get_all_products()

        if not service:
            self.set_status(404)
            self.set_content([])

            return self.get_response()

        self.set_status(200)
        self.set_content(service)

        return self.get_response()

    def add_product(self):
        json_data = request.get_json()
        service = add_product_data(json_data)

        if not service:
            self.set_status(400)

            return self.get_response()

        self.set_status(200)
        self.set_content(service)

        return self.get_response()