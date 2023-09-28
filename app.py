#!/usr/bin/env python3

from flask import Flask
from blueprints.product_bp import product_bp
from blueprints.order_bp import order_bp
from blueprints.cart_bp import cart_bp
from blueprints.user_bp import user_bp
from blueprints.auth_bp import auth_bp
from flask_jwt_extended import JWTManager
from conf.env_config import *
from flask_jwt_extended.exceptions import InvalidHeaderError
from commons.response import *


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = SECRET_KEY
jwt = JWTManager(app)

@app.errorhandler(InvalidHeaderError)
def handle_invalid_header_error(e):
    return unauthorized(e)

app.register_blueprint(product_bp, url_prefix='/gateway/v1')
app.register_blueprint(order_bp, url_prefix='/gateway/v1')
app.register_blueprint(cart_bp, url_prefix='/gateway/v1')
app.register_blueprint(user_bp, url_prefix='/gateway/v1')
app.register_blueprint(auth_bp, url_prefix='/gateway/v1')

if __name__ == '__main__':
    app.run(debug=True)

