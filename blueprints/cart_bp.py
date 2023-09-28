from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from api.cart import *
from flask_jwt_extended import jwt_required, get_jwt_identity

cart_bp = Blueprint('cart', __name__)
api = Api(cart_bp)

@cart_bp.before_request
@jwt_required()
def check_jwt():
    pass


class CartResource(Resource):
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('product_id', type=int, required=True, help='product-id-required')
        parser.add_argument('quantity', type=int, required=True, help='quantity-required')
        args = parser.parse_args()

        user_id = get_jwt_identity()
        if user_id is None:
            return bad_request('user-id-required')
        else:
            return add_cart_route(user_id)

    @jwt_required()
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('product_id', type=int, required=True, help='product-id-required')
        parser.add_argument('quantity', type=int, required=True, help='quantity-required')
        args = parser.parse_args()

        user_id = get_jwt_identity()

        if user_id is None:
            return bad_request('user-id-required')
        else:
            return update_cart_route(user_id)

    @jwt_required()
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('product_id', type=int, required=True, help='product-id-required')
        args = parser.parse_args()

        user_id = get_jwt_identity()

        if user_id is None:
            return bad_request('user-id-required')
        else:
            return remove_from_cart_route(user_id)

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()

        if user_id is None:
            return bad_request('user-id-required')
        else:
            return fetch_cart_route(user_id)
    
api.add_resource(CartResource, '/cart')