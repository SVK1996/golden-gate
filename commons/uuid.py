import uuid

def new_uuid_32():
    # Generate a UUID
    generated_uuid = uuid.uuid4()

    # Convert the UUID to a 128-bit integer
    uuid_int = int(generated_uuid.int)

    # Extract the least significant 32 bits
    uuid_32 = uuid_int & 0xFFFFFFFF  # Mask to keep only 32 bits

    return uuid_32
