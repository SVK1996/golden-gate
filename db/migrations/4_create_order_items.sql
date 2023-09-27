CREATE SEQUENCE order_items_id_seq START 1 INCREMENT 1;

CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER NOT NULL DEFAULT nextval('order_items_id_seq') CONSTRAINT order_items_pk PRIMARY KEY,
    order_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    quantity BIGINT NOT NULL,
    line_item_total BIGINT NOT NULL,
    created_at TIMESTAMP without time zone DEFAULT (now() at time zone 'utc'),
    updated_at TIMESTAMP without time zone DEFAULT (now() at time zone 'utc'),
    FOREIGN KEY (order_id) REFERENCES orders(id)
);