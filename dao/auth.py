from conf.env_config import *
from commons.response import *
from commons.response import *


def otp_request(mobile, otp, otp_hash):
    try:
        cur = db_pg.cursor()
        cur.execute("set search_path to " + db_schema)
        pg_record_values = [mobile, otp, otp_hash]
        # Insert a new otp into the database
        cur.execute("""INSERT INTO otps (mobile_no, code, mdigest) VALUES (%s, %s, %s);""", pg_record_values)
        cur.execute("commit")

        # Mask the mobile number
        masked_mobile = '******' + mobile[-4:]

        data = {"mdigest" : otp_hash, "masked_mobile" : masked_mobile}
        return response(data)
    except Exception as e:
        db_pg.rollback()
        logging.critical(e)
        return bad_request('otp-capture-failed')

def otp_valid(mdigest):
    try:
        cur = db_pg.cursor()
        cur.execute("set search_path to " + db_schema)
        pg_record_values = [mdigest]
        cur.execute("""SELECT mobile_no, code FROM otps WHERE mdigest = %s AND age(created_at, now() at time zone 'utc') < interval '15 minutes'""", pg_record_values)
        pg_record = cur.fetchone()
        if pg_record is None:
            return False
        else:
            otp_status = {"mobile_no": pg_record[0], "code": pg_record[1], "valid":True}
            return otp_status
    except Exception as e:
        logging.critical(e)
        otp_status = {"valid":False}
        return otp_status

def create_session(usr_id, a_token, client_ip):
    try:
        cur = db_pg.cursor()
        cur.execute("set search_path to " + db_schema)
        pg_record_values = [usr_id, a_token, client_ip]
        # Insert a session into the database
        cur.execute("""INSERT INTO sessions (usr_id, a_token, client_ip) VALUES (%s, %s, %s);""", pg_record_values)
        cur.execute("commit")
        return handle_response('session-created')
    except Exception as e:
        db_pg.rollback()
        logging.critical(e)
        return bad_request('session-creation-failed')

def invalidate_session(usr_id):
    try:
        cur = db_pg.cursor()
        cur.execute("set search_path to " + db_schema)

        now = datetime.now()

        pg_record_values = [now, usr_id]
        # Invalidate the user's session by updating is_valid to False
        cur.execute("""UPDATE sessions SET is_valid = FALSE,updated_at=%s WHERE usr_id = %s""",pg_record_values)
        cur.execute("commit")
        return True
    except Exception as e:
        db_pg.rollback()
        logging.critical(e)
        return False
   

    