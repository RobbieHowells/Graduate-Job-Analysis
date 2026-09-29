# Data Dictionary

This document describes the fields in the cleaned UK graduate technology jobs dataset ('jobs_clean.csv').

| Column | Type | Description | Source/Transformation |
|---|---|---|---|
| 'id' | String | Unique identifier for each job listing | Provided by the Adzuna API |
| 'title' | String | Job title advertised for the vacancy | Provided by the Adzuna API |
| 'role_category' | String | Standardised role group used to compare similar vacancies | Derived from the job title during cleaning |
| 'company' | String | Name of the company advertising the vacancy | Extracted from the Adzuna company field |
| 'location' | String | Location associated with the job listing | Extracted from the Adzuna location field | 
| 'salary_min' | Float | Minimum annual salary associated with the vacancy | Provided by the Adzuna API |
| 'salary_max' | Float | Maximum annual salary associated with the vacancy | Provided by the Adzuna API |
| 'salary_mid' | Float | Midpoint of the minimum and maximum salary values | Calculated as ('salary_min' + 'salary_max) / 2 |
| 'salary_is_predicted' | String | Indicates whether the salary was predicted by Adzuna rather than explicitly provided | Provided by the Adzuna API |
| 'working_arrangement' | String | Classified working arrangement for the vacancy | Derived from explicit hybrid, remote or on-site wording in the job description, otherwise set to Not specified |
| 'technologies' | List | Technologies and software tools explicitly mentioned in the available job description | Extracted from the job description using predefined regular expression patterns |
| 'contract_type' | String | Type of employment contract associated with the vacancy | Provided by the Adzuna API |
| 'contract_time' | String | Working time classification associated with the vacancy | Provided by the Adzuna API |
| 'created' | Datetime | Date and time the job listing was created | Provided by the Adzuna API and converted to a UTC datetime |
| 'category' | String | Adzuna category assigned to the job listing | Extracted from the Adzuna category field |
| 'description' | String | Available description text for vacancy | Provided by the Adzuna API, descriptions may be truncated |
| 'redirect_url' | String | URL used to access the advertised vacancy | Provided by the Adzuna API |
| 'latitude' | Float | Latitude associated with the job location | Provided by the Adzuna API where available |
| 'longitude' | Float | Longitude associated with the job location | Provided by the Adzuna API where available |
| 'inclusion_reason' | String | Reason the vacancy was included in the final analytical dataset | Assigned during cleaning based on the graduate and technology role filtering rules |

## Notes and Limitations

- The dataset represents UK graduate technology vacancies collected through the Adzuna API during the defined collection period and should not be interpreted as a complete representation of the UK graduate technology job market.
- Job descriptions returned by the Adzuna API may be truncated. Technology extraction therefore represents technologies explicitly mentioned in the available description text rather than all technologies required by each vacancy.
- Working arrangements are classified only when the available description explicitly identifies a role as hybrid, remote or on-site. Vacancies without sufficient information are classified as 'Not specified'.
- Some fields, including contract information and geographic coordinates, are not available for every vacancy.
- Duplicate and non-relevant listings, internships, apprenticeships and identified training programmes were removed during data cleaning to create the final analytical dataset.