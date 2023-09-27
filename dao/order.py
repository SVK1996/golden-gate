from conf.env_config import *
from commons.response import *

def create_order(product_ids, quantities):
        cur = db_pg.cursor()
        cur.execute("set search_path to " + db_schema)
        try:
            # Start a transaction
            db_pg.autocommit = False
            
            order_pg_record_values = [user]
            # Insert the order into the 'orders' table and retrieve the inserted order_id
            cur.execute("""INSERT INTO orders (user_id) VALUES (%s) RETURNING id;""", order_pg_record_values)
            order_id = cur.fetchone()[0]

            # Calculate the total order amount
            total_amount = 0

            # Insert the order items into the 'order_items' table and update product inventory
            for product_id, quantity in zip(product_ids, quantities):
                # Fetch product details and price
                cur.execute("SELECT name, price, inventory FROM products WHERE id = %s", (product_id,))
                product_data = cursor.fetchone()

                if not product_data:
                    return not_found(f"Product with ID # {product_id} not found")

                product_name, product_price, product_inventory = product_data

                # Calculate the line item subtotal
                line_item_total = product_price * quantity

                # Update the product inventory
                if product_inventory < quantity:
                    return unprocessable_entry(f"Product {product_name} is out of stock")
                
                now = datetime.now()

                cur.execute("UPDATE products SET inventory = inventory - %s, updated_at = %s WHERE id = %s", (quantity, now, product_id))

                # Update the total order amount
                total_amount += line_item_total

                items_pg_record_values = [order_id, product_id, product_name, quantity, line_item_total]

                # Insert the order item
                cur.execute("""INSERT INTO order_items (order_id, product_id, product_name, quantity, line_item_total) "VALUES (%s, %s, %s, %s, %s)""", items_pg_record_values)

            # Update the order with the total amount
            cur.execute("UPDATE orders SET total_amount = %s,updated_at = %s WHERE id = %s", (total_amount, now, order_id))

            # Commit the transaction
            db_pg.commit()

            data = {"order_id" : order_id}
            return response(data)
        except Exception as e:
            # Rollback the transaction on error
            db_pg.rollback()
            logging.error(e)
            return bad_request(str(e))
        finally:
            # Restore autocommit mode and close the connection
            db_pg.autocommit = True
            db_pg.close()

def fetch_order_history(user_id):
    try:
        cur = db_pg.cursor()
        cur.execute("set search_path to " + db_schema)
        cur.execute("""SELECT id, total_amount, created_at FROM orders WHERE user_id = %s ORDER BY created_at DESC;""", (user_id,))
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
        