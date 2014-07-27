CREATE TABLE results (
    job_uuid character(32) NOT NULL,
    organism2 character varying(32) NOT NULL,
    score double precision NOT NULL,
    shuffle_score double precision,
    time timestamp
);
