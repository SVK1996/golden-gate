from flask import request, jsonify
from dao.order import *
from commons.response import *

def create_order_route():
        data = request.json

        product_ids = data['product_ids']
        quantities = data.get('quantities', [1] * len(product_ids)) # Default to 1 if not provided 

        return create_order(product_ids, quantities)

def fetch_order_history_route(user_id):
        return fetch_order_history(user_id)