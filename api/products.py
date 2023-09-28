from flask import request, jsonify
from dao.products import *
from commons.response import *
import redis

def create_product_route():
        data = request.json

        name = data['name']
        description = data['description']
        price = data['price']
        inventory = data['inventory']

        return create_product(name, description, price, inventory)

def fetch_product_route(product_id):
        # Use the Redis connection from the pool
        redis_client = get_redis_connection()

        # Check if data exists in cache
        cached_data = redis_client.get(f'product:{product_id}')

        if cached_data:
                # Convert the cached data from bytes to string
                cached_data = cached_data.decode('utf-8')

                # Convert the cached data from string to dictionary
                cached_data = eval(cached_data)

                logging.info('Retrieved from cache')
                
                # Return the cached data
                return response(cached_data)
        else:
                # Fetch data from the database
                data = fetch_product(product_id)
                
                logging.info('Retrieved from database and cached')

                # Cache the data
                redis_client.set(f'product:{product_id}', str(data))

                # Return the data
                return response(data)

def fetch_product_list_route():
        # Retrieve query parameters for pagination
        page = int(request.args.get('page', default=0))
        page_size = int(request.args.get('page_size', default=20))

        return fetch_product_list(page_size,page)

def update_product_route(product_id):
        data = request.json

        if not data:
                return bad_request('At least one field is required for updating')

        return update_product(data, product_id)

def delete_product_route(product_id):
        return delete_product(product_id)

