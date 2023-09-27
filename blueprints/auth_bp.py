from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from api.auth import *
from flask_jwt_extended import jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__)
api = Api(auth_bp)

class LoginResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('mobile', type=str, required=True, help='mobile-required')
        args = parser.parse_args()

        return otp_request_route()
    
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('mdigest', type=str, required=True, help='mdigest-required')
        parser.add_argument('code', type=str, required=True, help='code-required')
        args = parser.parse_args()

        return otp_auth_route()


class LogoutResource(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        return logout_route(current_user)


api.add_resource(LoginResource,'/signin/primary/otp')
api.add_resource(LogoutResource,'/signout')
