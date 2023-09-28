from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from api.order import *
from flask_jwt_extended import jwt_required, get_jwt_identity

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
        user_id = get_jwt_identity()

        return create_order_route(user_id)

    @jwt_required()
    def get(self):
        # Fetch order history for the user
        user_id = get_jwt_identity()

        if user_id is None:
            return bad_request('user-id-required')
        else:
            return fetch_order_history_route(user_id)

api.add_resource(OrderResource, '/orders')