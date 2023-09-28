from flask import jsonify
from http import HTTPStatus

def handle_response(message):
    response = jsonify({'message': str(message)})
    response.status_code = HTTPStatus.OK
    return response

def response(data):
    response = jsonify({'data':data})
    response.status_code = HTTPStatus.OK
    return response

def response_list(total, data):
    response = jsonify({'data':data, 'total': int(total)})
    response.status_code = HTTPStatus.OK
    return response

def remove_response():
    response = jsonify({})
    response.status_code = HTTPStatus.NO_CONTENT
    return response

def handle_error(error, status_code):
    response = jsonify({'error': str(error)})
    response.status_code = status_code
    return response

def bad_request(error):
    return handle_error(error, HTTPStatus.BAD_REQUEST)

def not_found(error):
    return handle_error(error, HTTPStatus.NOT_FOUND)

def internal_server_error(error):
    return handle_error(error, HTTPStatus.INTERNAL_SERVER_ERROR)

def unprocessable_entry(error):
    return handle_error(error, HTTPStatus.UNPROCESSABLE_ENTITY)