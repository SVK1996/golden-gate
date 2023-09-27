from conf.env_config import *
from commons.response import *

def add_cart(user_id, product_id, quantity):
    try:
        cur = db_pg.cursor()
        cur.execute("set search_path to " + db_schema)
        pg_record_values = [user_id, product_id, quantity]
        # Add item into the cart
        cur.execute("""INSERT INTO cart (user_id, product_id, quantity) VALUES (%s, %s, %s)""",pg_record_values)
        cur.execute("commit")
        return handle_response('cart-addition-successful')
    except Exception as e:
        db_pg.rollback()
        logging.critical(e)
        return bad_request('cart-addition-failed')
    
def update_cart(user_id,product_id,quantity):
    try:
        cur = db_pg.cursor()
        cur.execute("set search_path to " + db_schema)

        now = datetime.now()

        pg_record_values = [quantity, now, user_id, product_id]
        # Update the quantity of the item in the cart
        cur.execute("""UPDATE cart SET quantity = %s,updated_at = %s WHERE user_id = %s AND product_id = %s""",pg_record_values)
        cur.execute("commit")
        return handle_response('cart-update-successful')
    except Exception as e:
        db_pg.rollback()
        logging.critical(e)
        return bad_request('cart-update-failed')
    
def remove_from_cart(user_id, product_id):
    try:
        cur = db_pg.cursor()
        cur.execute("set search_path to " + db_schema)
        pg_record_values = [user_id, product_id]
        # Remove the item from the cart
        cur.execute("""DELETE FROM cart WHERE user_id = %s AND product_id = %s""",pg_record_values)
        cur.execute("commit")
        return handle_response('cart-removal-successful')
    except Exception as e:
        db_pg.rollback()
        logging.critical(e)
        return bad_request('cart-removal-failed')

def fetch_cart(user_id):
    try:
        cur = db_pg.cursor()
        cur.execute("set search_path to " + db_schema)
        cur.execute("""SELECT product_id, quantity FROM cart WHERE user_id = %s""", (user_id,))
        records = cur.fetchall()
        if records is None:
            return handle_response('cart-empty')
        else:
            cart = []
            for record in records:
                item = {'product_id': record[0], 'quantity': record[1]}
                cart.append(item)
            return response_list(len(cart), cart)
    except Exception as e:
        db_pg.rollback()
        logging.critical(e)
        return bad_request('cart-fetch-failed')
