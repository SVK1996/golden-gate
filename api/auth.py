from flask import request, jsonify
from dao.auth import *
from commons.response import *
from commons.response import *
import hashlib
import random
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from dao.user import user_valid
from datetime import timedelta
from commons.nos import *

def otp_request_route():
    data = request.json

    mobile = data['mobile']

    if mobile_valid(mobile):
        return bad_request('mobile-invalid')

    # Generate a random 6-digit OTP
    otp = ''.join(random.choices('0123456789', k=6))

    # Calculate SHA-256 hash of the OTP
    otp_hash = hashlib.sha256(otp.encode()).hexdigest()

    return otp_request(mobile, otp, otp_hash)

def otp_auth_route():
    data = request.json

    mdigest = data['mdigest']
    code = data['code']
    
    # check whether OTP is valid
    otp_data = otp_valid(mdigest)
        
    if otp_data['valid']:
        mobile = otp_data['mobile_no']

        user_data = user_valid(mobile)
        # check whether user is valid
        if user_data['valid']:
            usr_id = user_data['usr_id']

            # Set the token expiration time to 90 days (90 * 24 * 3600 seconds)
            expiration_time = timedelta(days=90)

            # Generate JWT token for the user with the specified expiration time
            access_token = create_access_token(identity=usr_id, expires_delta=expiration_time)

            # Get the client's IP address from the request object
            client_ip = request.remote_addr
            
            create_session(usr_id, access_token, client_ip)
            
            data = {"acess_token" : access_token, "token_type":"Bearer"}
            return response(data)
        else:
            return bad_request('user-not-registered')
    else:
        return bad_request('otp-invalid')

def logout_route(current_user):
   
    if invalidate_session(current_user):

        # Generate a new token with a short expiration time
        short_expiration_time = timedelta(minutes=1)
        new_access_token = create_access_token(identity=current_user, expires_delta=short_expiration_time)
        
        data = {"token": new_access_token}

        # Get the client's IP address from the request object
        client_ip = request.remote_addr
                
        create_session(current_user, new_access_token, client_ip)

        return handle_response('logout-succesful')
    else:
        return bad_request('logout-failed')
