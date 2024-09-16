CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD 'rep';

SELECT pg_create_physical_replication_slot('replication_slot');

CREATE TABLE emails(
    id SERIAL PRIMARY KEY,
    email VARCHAR(50)
);

CREATE TABLE phones(
    id SERIAL PRIMARY KEY,
    phone VARCHAR(50)
);
