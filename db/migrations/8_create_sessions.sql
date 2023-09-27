CREATE SEQUENCE sessions_id_seq;

CREATE TABLE sessions (
    id INTEGER NOT NULL DEFAULT nextval('sessions_id_seq') CONSTRAINT sessions_pk PRIMARY KEY,
    usr_id BIGINT NOT NULL,
    a_token VARCHAR NOT NULL,
    client_ip VARCHAR,
    is_valid BOOLEAN NOT NULL DEFAULT true,
    logged_in_time TIMESTAMP without time zone DEFAULT (now() at time zone 'utc'),
    accessed_at TIMESTAMP without time zone DEFAULT (now() at time zone 'utc'),
    created_at TIMESTAMP without time zone DEFAULT (now() at time zone 'utc'),
    updated_at TIMESTAMP without time zone DEFAULT (now() at time zone 'utc')
);
