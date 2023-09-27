from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from api.products import *
from flask_jwt_extended import jwt_required

product_bp = Blueprint('product', __name__)
api = Api(product_bp)

@product_bp.before_request
@jwt_required()
def check_jwt():
    pass

class ProductResource(Resource):
    
    @jwt_required()
    def post(self):
        # Handle POST request
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('description', type=str, required=True)
        parser.add_argument('price', type=int, required=True)
        parser.add_argument('inventory', type=int, required=True)

        args = parser.parse_args()
        # Process and save the data
        return create_product_route() 

    @jwt_required()
    def get(self, product_id=None):
        # Handle GET request
        if product_id is None:
            return fetch_product_list_route()
        else:
            return fetch_product_route(product_id)
    
    @jwt_required()
    def put(self, product_id=None):
        # Handle PUT request
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('description', type=str)
        parser.add_argument('price', type=int)
        parser.add_argument('inventory', type=int)

        args = parser.parse_args()

        if product_id is None:
            return bad_request('product-id-required')
        else:
            return update_product_route(product_id)

    @jwt_required()
    def delete(self, product_id):
         # Handle DELETE request
        if product_id is None:
            return bad_request('product-id-required')
        else:
            return delete_product_route(product_id)

api.add_resource(ProductResource, '/products', '/products/<int:product_id>')
