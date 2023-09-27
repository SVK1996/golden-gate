CREATE SEQUENCE products_id_seq START 1 INCREMENT 1;

CREATE TABLE IF NOT EXISTS products (
    id INTEGER NOT NULL DEFAULT nextval('products_id_seq') CONSTRAINT products_pk PRIMARY KEY,
    name VARCHAR NOT NULL UNIQUE,  -- NOT NULL and UNIQUE constraints on 'name'
    description VARCHAR NOT NULL,  -- NOT NULL constraint on 'description'
    price BIGINT NOT NULL,  -- NOT NULL constraint on 'price'
    inventory BIGINT NOT NULL,  -- NOT NULL constraint on 'inventory'
    created_at TIMESTAMP without time zone DEFAULT (now() at time zone 'utc'),
    updated_at TIMESTAMP without time zone DEFAULT (now() at time zone 'utc')
);