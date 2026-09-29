CREATE TABLE jobs (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    role_category TEXT NOT NULL,
    company TEXT NOT NULL,
    location TEXT NOT NULL,
    salary_min NUMERIC(10, 2) NOT NULL,
    salary_max NUMERIC(10, 2) NOT NULL,
    salary_mid NUMERIC(10, 2) NOT NULL,
    salary_is_predicted BOOLEAN NOT NULL,
    working_arrangement TEXT NOT NULL,
    contract_type TEXT,
    contract_time TEXT,
    created TIMESTAMPTZ NOT NULL,
    category TEXT NOT NULL,
    description TEXT NOT NULL,
    redirect_url TEXT NOT NULL,
    latitude NUMERIC(9, 6),
    longitude NUMERIC(9, 6),
    inclusion_reason TEXT NOT NULL
);

CREATE TABLE technologies (
    technology_id SERIAL PRIMARY KEY,
    technology_name TEXT UNIQUE NOT NULL
);

CREATE TABLE job_technologies (
    job_id TEXT NOT NULL,
    technology_id INTEGER NOT NULL,
    PRIMARY KEY (job_id, technology_id),
    FOREIGN KEY (job_id) REFERENCES jobs(id),
    FOREIGN KEY (technology_id) REFERENCES technologies(technology_id)
);