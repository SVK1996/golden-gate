from flask import request, jsonify
from dao.order import *
from commons.response import *

def create_order_route(usr_id):
        data = request.get_json()

        return create_order(data, usr_id)

def fetch_order_history_route(user_id):

        # Retrieve query parameters for pagination
        page = int(request.args.get('page', default=0))
        page_size = int(request.args.get('page_size', default=20))

        return fetch_order_history(page_size, page, user_id)