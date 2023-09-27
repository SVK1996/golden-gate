import re

def mobile_valid(mobile_no):
    pattern = r"^[0-9]{10,15}$"
    if not re.match(pattern, mobile_no):
        return False
    return True