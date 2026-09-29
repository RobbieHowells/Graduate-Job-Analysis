TRUNCATE TABLE job_technologies, technologies, jobs RESTART IDENTITY;

CREATE TEMP TABLE staging_jobs (
    id TEXT,
    title TEXT,
    role_category TEXT,
    company TEXT,
    location TEXT,
    salary_min NUMERIC(10, 2),
    salary_max NUMERIC(10, 2),
    salary_mid NUMERIC(10, 2),
    salary_is_predicted BOOLEAN,
    working_arrangement TEXT,
    technologies TEXT,
    contract_type TEXT,
    contract_time TEXT,
    created TIMESTAMPTZ,
    category TEXT,
    description TEXT,
    redirect_url TEXT,
    latitude NUMERIC(9, 6),
    longitude NUMERIC(9, 6),
    inclusion_reason TEXT
);

\copy staging_jobs FROM 'data/processed/jobs_clean.csv' WITH (FORMAT csv, HEADER true);

SELECT COUNT(*) FROM staging_jobs;

INSERT INTO jobs (
    id,
    title,
    role_category,
    company,
    location,
    salary_min,
    salary_max,
    salary_mid,
    salary_is_predicted,
    working_arrangement,
    contract_type,
    contract_time,
    created,
    category,
    description,
    redirect_url,
    latitude,
    longitude,
    inclusion_reason
)
SELECT
    id,
    title,
    role_category,
    company,
    location,
    salary_min,
    salary_max,
    salary_mid,
    salary_is_predicted,
    working_arrangement,
    contract_type,
    contract_time,
    created,
    category,
    description,
    redirect_url,
    latitude,
    longitude,
    inclusion_reason
FROM staging_jobs;

SELECT COUNT(*) FROM jobs;

INSERT INTO technologies (technology_name)
SELECT DISTINCT
    TRIM(BOTH '''' FROM technology)
FROM staging_jobs
CROSS JOIN LATERAL unnest(
    string_to_array(
        TRIM(BOTH '[]' FROM technologies),
        ', '
    )
) AS technology
WHERE technologies <> '[]';

SELECT * FROM technologies
ORDER BY technology_id;

INSERT INTO job_technologies (job_id, technology_id)
SELECT
    staging_jobs.id,
    technologies.technology_id
FROM staging_jobs
CROSS JOIN LATERAL unnest(
    string_to_array(
        TRIM(BOTH '[]' FROM staging_jobs.technologies),
        ', '
    )
) AS technology
JOIN technologies
    ON technologies.technology_name = TRIM(BOTH '''' FROM technology)
WHERE staging_jobs.technologies <> '[]';

SELECT * FROM job_technologies
ORDER BY job_id, technology_id;

SELECT
    (SELECT COUNT(*) FROM jobs) AS job_count,
    (SELECT COUNT(*) FROM technologies) AS technology_count,
    (SELECT COUNT(*) FROM job_technologies) AS job_technology_count;