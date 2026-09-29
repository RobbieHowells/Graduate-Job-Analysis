SELECT
    role_category,
    COUNT(*) AS job_count
FROM jobs
GROUP BY role_category
ORDER BY job_count DESC;

SELECT
    role_category,
    COUNT(*) AS job_count,
    ROUND(AVG(salary_mid), 2) AS average_salary,
    MIN(salary_mid) AS minimum_salary,
    MAX(salary_mid) AS maximum_salary
FROM jobs
GROUP BY role_category
ORDER BY average_salary DESC;

SELECT
    salary_is_predicted,
    COUNT(*) AS job_count,
    ROUND(AVG(salary_mid), 2) AS average_salary
FROM jobs
GROUP BY salary_is_predicted
ORDER BY salary_is_predicted;

SELECT
    working_arrangement,
    COUNT(*) AS job_count,
    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (),
        2
    ) AS percentage
FROM jobs
GROUP BY working_arrangement
ORDER BY job_count DESC;

SELECT
    location,
    COUNT(*) AS job_count,
    ROUND(AVG(salary_mid), 2) AS average_salary
FROM jobs
GROUP BY location
ORDER BY job_count DESC, average_salary DESC;

SELECT
    t.technology_name,
    COUNT(DISTINCT jt.job_id) AS job_count
FROM technologies t
JOIN job_technologies jt
    ON t.technology_id = jt.technology_id
JOIN jobs j
    ON jt.job_id = j.id
GROUP BY t.technology_name
ORDER BY job_count DESC, t.technology_name;

SELECT
    COUNT(*) AS job_count,
    ROUND(AVG(salary_mid), 2) AS average_salary,
    MIN(salary_mid) AS minimum_salary,
    MAX(salary_mid) AS maximum_salary
FROM jobs;

SELECT
    j.title,
    j.company,
    j.role_category,
    t.technology_name
FROM jobs j
JOIN job_technologies jt
    ON j.id = jt.job_id
JOIN technologies t
    ON jt.technology_id = t.technology_id
ORDER BY j.title, t.technology_name;