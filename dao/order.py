from conf.env_config import *
from commons.response import *
from datetime import datetime
from dao.products import *
import traceback
from conf.env_config import *

def create_order(order_data, user):
        try:
            cur = db_pg.cursor()
            cur.execute("set search_path to " + db_schema)

            now = datetime.now()

            order_items = order_data.get('order_items')
            if not order_items or not isinstance(order_items, list) or len(order_items) == 0:
                return bad_request("Invalid or empty order_items")
                        
            total_amount = 0
            for item in order_items:
                product_id = item.get('product_id')
                quantity = item.get('quantity')
                price = item.get('price')
                
                # # Check if product_id exists
                if len(fetch_product(product_id)) == 0:
                     return bad_request(f"Product with ID {product_id} does not exist")
                
                # Check if quantity is a positive integer
                if not isinstance(quantity, int) or quantity <= 0:
                    return bad_request("Invalid quantity for one or more order items")


                total_amount += price * quantity
            # Insert order into the database
            cur.execute("INSERT INTO orders (usr_id, total_amount) VALUES (%s, %s) RETURNING id",(user, total_amount))
            order_id = cur.fetchone()[0]
            
            # Update the inventory
            update_inventory(order_items)

            # Insert order items into the database
            for item in order_items:
                product_id = item.get('product_id')
                quantity = item.get('quantity')
                price = item.get('price')

                # Insert order items into the database
                cur.execute("INSERT INTO order_items (order_id, product_id, quantity, line_item_total) VALUES (%s, %s, %s, %s)",(order_id, product_id, quantity, price))

            # Commit the transaction
            db_pg.commit()

            cur.close()
            
            data = {"order_id" : order_id}
            return response(data)
        except Exception as e:
            traceback.print_exc()
            db_pg.rollback()
            logging.error(e)
            return bad_request(str(e))

def fetch_order_history(limit, offset, user_id):
    try:
        cur = db_pg.cursor()
        cur.execute("set search_path to " + db_schema)
        cur.execute("""SELECT id, total_amount, created_at FROM orders WHERE usr_id = %s LIMIT %s OFFSET %s;""", (user_id, limit, offset))            
        records = cur.fetchall()
        if records is None:
            return not_found('orders-not-found')
        else:
            orders = []
            for record in records:
                order = {'id': record[0],'total_amount': record[1], 'created_at': record[2]}
                orders.append(order)
            return response_list(len(orders), orders)
    except Exception as e:
        db_pg.rollback()
        logging.critical(e)
        return bad_request('orders-fetch-failed')