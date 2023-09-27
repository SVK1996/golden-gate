CREATE SEQUENCE otps_id_seq;

CREATE TABLE otps (
    id INTEGER NOT NULL DEFAULT nextval('otps_id_seq') CONSTRAINT otps_pk PRIMARY KEY,
    mdigest VARCHAR NOT NULL UNIQUE,
    code VARCHAR(10),
    mobile_no VARCHAR(16) NOT NULL,
    created_at TIMESTAMP without time zone DEFAULT (now() at time zone 'utc'),
    accessed_at TIMESTAMP without time zone DEFAULT (now() at time zone 'utc')
);
