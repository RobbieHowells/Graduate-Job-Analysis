import json
import pandas as pd

with open("data/raw/tech_jobs.json", "r", encoding="utf-8") as tech_jobs:
    jobs = json.load(tech_jobs)

unique_jobs = {}

for job in jobs:
    unique_jobs[job["id"]] = job

jobs = list(unique_jobs.values())

df = pd.DataFrame(jobs)

df["company"] = df["company"].apply(
    lambda x: x.get("display_name") if isinstance(x, dict) else None
)

df["location"] = df["location"].apply(
    lambda x: x.get("display_name") if isinstance(x, dict) else None
)

df["category"] = df["category"].apply(
    lambda x: x.get("label") if isinstance(x, dict) else None
)

df = df.drop(
    columns=["__CLASS__", "adref"],
    errors="ignore"
)

graduate_keywords = [
    "graduate",
    "junior",
    "entry level",
    "entry-level",
    "trainee",
    "intern",
    "internship",
]

role_keywords = [
    "data analyst",
    "data engineer",
    "software engineer",
    "software developer",
    "software development",
    "data scientist",
    "data science",
    "business analyst",
    "bi analyst",
    "digital data",
    "data consultant",
    "fullstack",
    "technology developer",
    "information & digital technology",
    "digital data and technology",
    "technology graduate programme - macquarie",
]

training_programme_keywords = [
    "self-funded career programme",
    "course fees back",
    "career programme",
    "career program",
    "live instructor-led online training",
    "accredited training",
    "career pathway",
    "recruitment support",
]

df["search_text"] = (
    df["title"].fillna("")
    + " "
    + df["description"].fillna("")
).str.lower()

df["title_lower"] = df["title"].fillna("").str.lower()

training_pattern = "|".join(training_programme_keywords)

df["training_programme"] = df["search_text"].str.contains(
    training_pattern,
    regex=True,
)

graduate_pattern = r"\b(?:" + "|".join(graduate_keywords) + r")\b"

df["matched_keyword"] = df["search_text"].str.extract(
    f"({graduate_pattern})",
    expand=False,
)

df["title_keyword"] = df["title_lower"].str.extract(
    f"({graduate_pattern})",
    expand=False,
)

internship_apprenticeship_pattern = (
    r"\b(?:intern|internship|apprentice|apprenticeship)\b"
)

df["internship_apprenticeship"] = df["title_lower"].str.contains(
    internship_apprenticeship_pattern,
    regex=True,
)

role_pattern = r"\b(?:" + "|".join(role_keywords) + r")\b"

df["relevant_role"] = df["title_lower"].str.contains(
    role_pattern,
    regex=True,
)

graduate_matches = df[
    df["search_text"].str.contains(
        graduate_pattern,
        regex=True,
    )
]

title_matches = df[
    df["title_keyword"].notna()
]

description_only_matches = graduate_matches[
    graduate_matches["title_keyword"].isna()
]

relevant_title_matches = title_matches[
    title_matches["relevant_role"]
]

valid_title_matches = relevant_title_matches[
    ~relevant_title_matches["training_programme"]
]

valid_graduate_titles = valid_title_matches[
    ~valid_title_matches["internship_apprenticeship"]
]

description_non_training = description_only_matches[
    ~description_only_matches["training_programme"]
]

strong_description_phrases = [
    "recent graduate",
    "graduate opportunity",
    "early-career professional",
]

strong_description_pattern = "|".join(
    strong_description_phrases
)

strong_description_candidates = description_non_training[
    description_non_training["description"]
    .fillna("")
    .str.lower()
    .str.contains(
        strong_description_pattern,
        regex=True,
    )
]

technology_context_phrases = [
    "data management",
    "systems and solutions",
]

technology_context_pattern = "|".join(
    technology_context_phrases
)

contextual_technology_candidates = title_matches[
    title_matches["title_lower"].str.contains(
        r"\btechnology graduate programme\b",
        regex=True,
    )
    &
    title_matches["description"]
    .fillna("")
    .str.lower()
    .str.contains(
        technology_context_pattern,
        regex=True,
    )
]

title_candidates = valid_graduate_titles.copy()
description_candidates = strong_description_candidates.copy()
technology_candidates = contextual_technology_candidates.copy()

title_candidates["inclusion_reason"] = "entry-level technology title"
description_candidates["inclusion_reason"] = (
    "strong entry-level evidence in description"
)
technology_candidates["inclusion_reason"] = (
    "technology graduate programme with digital context"
)

final_candidates = pd.concat(
    [
        title_candidates,
        description_candidates,
        technology_candidates,
    ],
    ignore_index=True,
)

final_candidates = final_candidates[
    ~(
        (final_candidates["company"] == "NEWTO TRAINING LIMITED")
        &
        (final_candidates["title"] == "Entry Level Data Consultant")
    )
].copy()

confirmed_duplicate_ids = [
    "5878471244",
    "5878470661",
    "5869554113",
    "5890388308",
]

final_candidates = final_candidates[
    ~final_candidates["id"].isin(confirmed_duplicate_ids)
].copy()

final_candidates["created"] = pd.to_datetime(
    final_candidates["created"],
    utc=True
)

final_candidates["salary_mid"] = (
    final_candidates["salary_min"] + final_candidates["salary_max"]
) / 2

def classify_role(title):
    title = title.lower()

    if "data analyst" in title:
        return "Data Analyst"
    elif (
        "software developer" in title
        or "fullstack" in title
        or "technology developer" in title
    ):
        return "Software Developer"
    elif "business analyst" in title:
        return "Business Analyst"
    else:
        return "Technology Graduate"


final_candidates["role_category"] = final_candidates["title"].apply(
    classify_role
)

print(
    final_candidates[
        ["title", "company", "role_category"]
    ].to_string(index=False)
)

technology_roles = final_candidates[
    final_candidates["role_category"] == "Technology Graduate"
]

def classify_working_arrangement(description):
    description = description.lower()

    if "hybrid" in description:
        return "Hybrid"
    elif "fully remote" in description or "remote working" in description:
        return "Remote"
    elif (
        "on-site" in description
        or "onsite" in description
        or "on site" in description
    ):
        return "On-site"
    else:
        return "Not specified"


final_candidates["working_arrangement"] = final_candidates[
    "description"
].apply(classify_working_arrangement)

print(
    final_candidates[
        ["title", "company", "working_arrangement"]
    ].to_string(index=False)
)

print("\nWorking arrangement counts:")
print(final_candidates["working_arrangement"].value_counts())

print("\nFinal candidates:", len(final_candidates))

skill_keywords = [
    "python",
    "sql",
    "power bi",
    "excel",
    "java",
    "javascript",
    "c#",
    "react",
    "aws",
    "azure",
    "docker",
    "git",
    "linux",
    "machine learning",
    "tableau",
    "spark",
]

for _, job in final_candidates.iterrows():
    print("\nTITLE:", job["title"])
    print("COMPANY:", job["company"])
    print("DESCRIPTION:", job["description"])