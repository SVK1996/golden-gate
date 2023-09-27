from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from api.order import *
from flask_jwt_extended import jwt_required

order_bp = Blueprint('order', __name__)
api = Api(order_bp)

@order_bp.before_request
@jwt_required()
def check_jwt():
    pass

class OrderResource(Resource):
    
    @jwt_required()
    def post(self):
        # Create a new order for the user
        parser = reqparse.RequestParser()
        parser.add_argument('product_ids', type=list, required=True, help='List of product IDs in the order')

        args = parser.parse_args()

        return create_order_route()

    @jwt_required()
    def get(self, user_id=None):
        # Fetch order history for the user
        if user_id is None:
            return bad_request('user-id-required')
        else:
            return fetch_order_history_route(user_id)

api.add_resource(OrderResource, '/orders', '/orders/<int:user_id>')