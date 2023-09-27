from conf.env_config import *
from commons.response import *
from commons.response import *

def create_product(name, description, price, inventory):
    try:
        cur = db_pg.cursor()
        cur.execute("set search_path to " + db_schema)
        pg_record_values = [name, description, price, inventory]
        # Insert a new product into the database
        cur.execute("""INSERT INTO products (name, description, price, inventory) VALUES (%s, %s, %s, %s) RETURNING id;""",pg_record_values)
        product_id = cur.fetchone()[0]
        cur.execute("commit")
        # Return the product id
        data = {'product_id': product_id}
        return response(data)
    except Exception as e:
        db_pg.rollback()
        logging.critical(e)
        return bad_request('product-creation-failed')

def fetch_product(product_id):
    try:
        cur = db_pg.cursor()
        cur.execute("set search_path to " + db_schema)
        cur.execute("""SELECT id, name, description, price, inventory FROM products WHERE id = %s;""", (product_id,))
        record = cur.fetchone()
        if record is None:
            return not_found('product-not-found')
        else:
            product = {'id': record[0], 'name': record[1], 'description': record[2], 'price': record[3], 'inventory': record[4]}
            data = [product]
            return data
    except Exception as e:
        db_pg.rollback()
        logging.critical(e)
        return []

def fetch_product_list(limit,offset):
    try:
        cur = db_pg.cursor()
        cur.execute("set search_path to " + db_schema)
        # 1. Get total number of products
        cur.execute("SELECT COUNT(*) FROM products")
        total_products = cur.fetchone()[0]
        # 2. Get products for the based on page and size
        cur.execute("""SELECT id, name, description, price, inventory FROM products LIMIT %s OFFSET %s;""", (limit, offset))
        records = cur.fetchall()
        if records is None:
            return not_found('products-not-found')
        else:
            products = []
            for record in records:
                product = {'id': record[0], 'name': record[1], 'description': record[2], 'price': record[3], 'inventory': record[4]}
                products.append(product)
            return response_list(total_products, products)
    except Exception as e:
        db_pg.rollback()
        logging.critical(e)
        return bad_request('products-fetch-failed')

def update_product(data, product_id):
    try:
        cur = db_pg.cursor()
        cur.execute("set search_path to " + db_schema)
        
        update_query = "UPDATE products SET "
        update_values = []

        name = data.get('name')
        description = data.get('description')
        price = data.get('price')
        inventory = data.get('inventory')

        if name is not None:
            update_query += "name = %s, "
            update_values.append()
        if description is not None:
            update_query += "description = %s, "
            update_values.append(description)
        if price is not None:
            update_query += "price = %s, "
            update_values.append(price)
        if inventory is not None:
            update_query += "inventory = %s, "
            update_values.append(inventory)

        now = datetime.now()

        # Remove the trailing comma and add the WHERE clause
        update_query = update_query.rstrip(', ') + ",updated_at = %s WHERE id = %s"
        update_values.append(now, product_id)

        cur.execute(update_query, tuple(update_values))
        cur.execute("commit")
        # Return the product id
        resp = {'product_id': product_id}
        return response(resp)
    except Exception as e:
        db_pg.rollback()
        logging.critical(e)
        return bad_request('product-update-failed')

def delete_product(product_id):
    try:
        cur = db_pg.cursor()
        cur.execute("set search_path to " + db_schema)
        cur.execute("""DELETE FROM products WHERE id = %s;""", (product_id,))
        cur.execute("commit")
        return remove_response()
    except Exception as e:
        db_pg.rollback()
        logging.critical(e)
        return bad_request('product-deletion-failed')