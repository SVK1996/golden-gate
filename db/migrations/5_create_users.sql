CREATE SEQUENCE users_id_seq START 1 INCREMENT 1;

CREATE TABLE IF NOT EXISTS users (
    id INTEGER NOT NULL DEFAULT nextval('users_id_seq') CONSTRAINT users_pk PRIMARY KEY,
    usr_id BIGINT NOT NULL UNIQUE,
    display_name VARCHAR(300),
    email VARCHAR(100) UNIQUE,
    mobile_number VARCHAR(16) NOT NULL UNIQUE,
    created_at TIMESTAMP without time zone DEFAULT (now() at time zone 'utc'),
    updated_at TIMESTAMP without time zone DEFAULT (now() at time zone 'utc')
);