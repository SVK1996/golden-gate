from flask import request, jsonify
from dao.cart import *
from commons.response import *
from commons.response import *

def add_cart_route():
        data = request.json

        user_id = data['user_id']
        product_id = data['product_id']
        quantity = data['quantity']

        return add_cart(user_id, product_id, quantity)

def update_cart_route():
        data = request.json

        user_id = data['user_id']
        product_id = data['product_id']
        quantity = data['quantity']

        return update_cart(user_id, product_id, quantity)

def remove_from_cart_route():
       data = request.json

       user_id = data['user_id']
       product_id = data['product_id']

       return remove_from_cart(user_id, product_id)

def fetch_cart_route(user_id):
    return fetch_cart(user_id)
    