CREATE TABLE IF NOT EXISTS cart (
    usr_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    quantity INTEGER NOT NULL,
    created_at TIMESTAMP without time zone DEFAULT (now() at time zone 'utc'),
    updated_at TIMESTAMP without time zone DEFAULT (now() at time zone 'utc'),
    PRIMARY KEY (usr_id, product_id),
    FOREIGN KEY (usr_id) REFERENCES users(usr_id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);