from conf.env_config import *
from commons.response import *
from commons.response import *

def create_user(usr_id, name, email, mobile):
    try:
        cur = db_pg.cursor()
        cur.execute("set search_path to " + db_schema)

        # Check if the mobile number is unique
        cur.execute("SELECT * FROM users WHERE mobile_number = %s", (mobile,))
        existing_user = cur.fetchone()

        if existing_user:
            return bad_request('mobile-already-exists')

        pg_record_values = [usr_id, name, email, mobile]
        # Insert a new user into the database
        cur.execute("""INSERT INTO users (usr_id, display_name, email, mobile_number) VALUES (%s, %s, %s, %s) RETURNING usr_id;""",pg_record_values)
        product_id = cur.fetchone()[0]
        cur.execute("commit")
        # Return the product id
        data = {'usr_id': usr_id}
        return response(data)
    except Exception as e:
        db_pg.rollback()
        logging.critical(e)
        return bad_request('user-registration-failed')

def user_valid(mobile):
    try:
        cur = db_pg.cursor()
        cur.execute("set search_path to " + db_schema)
        pg_record_values = [mobile]
        cur.execute("""SELECT usr_id FROM users WHERE mobile_number = %s""", pg_record_values)
        pg_record = cur.fetchone()
        if pg_record is None:
            return False
        else:
            user_status = {"usr_id": pg_record[0], "valid":True}
            return user_status
    except Exception as e:
        logging.critical(e)
        user_status = {"valid":False}
        return user_status
