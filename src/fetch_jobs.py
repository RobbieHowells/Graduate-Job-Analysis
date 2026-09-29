import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

app_id = os.getenv("ADZUNA_APP_ID")
app_key = os.getenv("ADZUNA_APP_KEY")

search_terms = [
    "data analyst",
    "data engineer",
    "software engineer",
    "software developer",
    "business analyst",
    "BI analyst",
    "data scientist",
    "technology graduate",
]



all_jobs = []

for search_term in search_terms:
    params = {
    "results_per_page": 50,
     "app_id": app_id,
     "app_key": app_key,
     "what": search_term,
     "max_days_old": 30
    }

    for page in range(1, 4):
        url = f"https://api.adzuna.com/v1/api/jobs/gb/search/{page}"

        response = requests.get(url, params=params, timeput=30)
        response.raise_for_status()
        data = response.json()

        all_jobs.extend(data["results"])

with open("data/raw/tech_jobs.json", "w", encoding="utf-8") as tech_jobs:
    json.dump(all_jobs, tech_jobs, indent=4)

print(len(all_jobs))



