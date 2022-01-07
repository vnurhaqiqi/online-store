from flask import Response
import json

STATUS_CODE = {
    200: "Success", 201: "Created", 400: "Bad Request", 401: "Unauthorized", 403: "Forbidden", 404: "Not Found",
    405: "Method Not Acceptable", 500: "Internal Server Error", 503: "Service Unavailable"
}


class Responses(Response):
    def __init__(self):
        super().__init__()
        self.status_code = False
        self.message = ""
        self.data_response = {
            'data': {},
            'meta': {},
            'status': {
                'code': 0,
                'message_server': '',
                'message_client': ''
            }
        }

    def set_status(self, code):
        self.status_code = code
        self.data_response['status']['code'] = code
        self.set_message()

    def set_message(self):
        self.message = STATUS_CODE[self.status_code]
        self.data_response['status']['message_server'] = self.message
        self.data_response['status']['message_client'] = self.message

    def set_additional_message(self, message):
        self.message = message
        self.data_response['message'] = self.message

    def set_content(self, content):
        self.data_response['data'] = content

    def set_pagination(self, total, total_page, current_page=1, per_page=10):
        self.data_response['meta']['pagination'] = {
            'current_page': current_page,
            'per_page': per_page,
            'total': total,
            'total_page': total_page
        }

    def get_response(self):
        response = Response(
            response=json.dumps(self.data_response),
            status=self.status_code,
            mimetype='application/json'
        )

        return response
