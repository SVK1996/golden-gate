from flask import request, jsonify
from dao.user import *
from commons.response import *
from commons.uuid import *
from commons.str import *
from commons.nos import *

def create_user_route():
    data = request.json

    name = data['name']
    email = data['email']
    mobile = data['mobile']

    if email_valid(email) == False:
        return bad_request('email-invalid')
    
    if mobile_valid(mobile) == False:
        return bad_request('mobile-invalid')


    usr_id = new_uuid_32()

    return create_user(usr_id, name, email, mobile)