from flask import jsonify

def handle_response(message):
    response = jsonify({'message': str(message)})
    response.status_code = 200
    return response

def response(data):
    response = jsonify({'data':data})
    response.status_code = 200
    return response

def response_list(total, data, status_code):
    response = jsonify({'data':data, 'total': int(total)})
    response.status_code = 200
    return response

def remove_response():
    response = jsonify({})
    response.status_code = 204
    return response

def handle_error(error, status_code):
    response = jsonify({'error': str(error)})
    response.status_code = status_code
    return response

def bad_request(error):
    return handle_error(error, 400)

def not_found(error):
    return handle_error(error, 404)

def internal_server_error(error):
    return handle_error(error, 500)

def unprocessable_entry(error):
    return handle_error(error, 422)