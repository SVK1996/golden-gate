CREATE SEQUENCE orders_id_seq START 1 INCREMENT 1;

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER NOT NULL DEFAULT nextval('orders_id_seq') CONSTRAINT orders_pk PRIMARY KEY,
    usr_id BIGINT NOT NULL,
    total_amount BIGINT,
    created_at TIMESTAMP without time zone DEFAULT (now() at time zone 'utc'),
    updated_at TIMESTAMP without time zone DEFAULT (now() at time zone 'utc'),
    FOREIGN KEY (usr_id) REFERENCES users(usr_id)
);