from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from api.user import *
from flask_jwt_extended import jwt_required

user_bp = Blueprint('user', __name__)
api = Api(user_bp)

@user_bp.before_request
@jwt_required()
def check_jwt():
    pass

class UserResource(Resource):
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='name-required')
        parser.add_argument('email', type=str, required=True, help='email-required')
        parser.add_argument('mobile', type=str, required=True, help='mobile-required')
        args = parser.parse_args()
        
        return create_user_route()

api.add_resource(UserResource,'/register')
