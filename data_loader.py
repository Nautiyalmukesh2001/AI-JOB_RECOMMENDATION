from typing import List, Dict
import pandas as pd

# Minimal schema expected in CSV
REQUIRED_COLS = ["title", "company", "description", "link"]


def load_jobs_from_csv(file) -> List[Dict]:
    """Load a CSV (uploaded file or path) and normalize columns."""
    df = pd.read_csv(file)
    colmap = {c.lower().strip(): c for c in df.columns}
    for rc in REQUIRED_COLS:
        if rc not in colmap:
            raise ValueError(f"CSV missing required column: {rc}")

    jobs: List[Dict] = []
    for _, row in df.iterrows():
        jobs.append({
            "title": row[colmap["title"]],
            "company": row[colmap["company"]],
            "description": row[colmap["description"]],
            "location": row[colmap.get("location", "location")] if "location" in colmap else "",
            "type": row[colmap.get("type", "type")] if "type" in colmap else "",
            "link": row[colmap["link"]],
            "experience": row[colmap.get("experience", "experience")] if "experience" in colmap else "",
            "skills": row[colmap.get("skills", "skills")] if "skills" in colmap else "",
            "salary": row[colmap.get("salary", "salary")] if "salary" in colmap else "",
        })
    return jobs


SAMPLE_JOBS = [
    {
        "title": "Data Analyst",
        "company": "ABC Corp",
        "description": "Work on dashboards and analytics. Requires Python, SQL, Tableau. Location: Bangalore. Remote possible.",
        "location": "Bangalore",
        "type": "Full-time",
        "link": "https://example.com/abc-analyst",
    },
    {
        "title": "Machine Learning Engineer",
        "company": "XYZ Tech",
        "description": "Design NLP pipelines using Python and TensorFlow. Location: Mumbai.",
        "location": "Mumbai",
        "type": "Full-time",
        "link": "https://example.com/xyz-ml",
    },
    {
        "title": "Business Analyst",
        "company": "QRS Solutions",
        "description": "Stakeholder analytics, SQL, Power BI. Location: Bangalore. Hybrid.",
        "location": "Bangalore",
        "type": "Hybrid",
        "link": "https://example.com/qrs-ba",
    },
]