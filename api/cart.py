from flask import request, jsonify
from dao.cart import *
from commons.response import *
from dao.products import *

def add_cart_route(user_id):
        data = request.json

        product_id = data['product_id']
        quantity = data['quantity']

        if len(fetch_product(product_id)) == 0 or len(fetch_product(product_id)) < 0:
                return not_found('product-not-found')


        return add_cart(user_id, product_id, quantity)

def update_cart_route(user_id):
        data = request.json

        product_id = data['product_id']
        quantity = data['quantity']

        if len(fetch_product(product_id)) == 0 or len(fetch_product(product_id)) < 0:
                return not_found('product-not-found')

        return update_cart(user_id, product_id, quantity)

def remove_from_cart_route(user_id):
       data = request.json

       product_id = data['product_id']

       if len(fetch_product(product_id)) == 0 or len(fetch_product(product_id)) < 0:
                return not_found('product-not-found')

       return remove_from_cart(user_id, product_id)

def fetch_cart_route(user_id):
    return fetch_cart(user_id)
    