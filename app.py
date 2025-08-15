import os
import json
from typing import List, Dict

import streamlit as st
from dotenv import load_dotenv
import requests
import pandas as pd

from langchain.chains import LLMChain
from langchain_groq import ChatGroq  # ✅ Groq integration
from prompt import job_recommendation_prompt
from data_loader import SAMPLE_JOBS
from rag import build_vectorstore, retrieve
from resume import extract_text_from_pdf
from utils import safe_json_parse, build_user_profile_text
from job_api import fetch_linkedin_jobs

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="AI Job Recommender (LangChain + Groq)",
    page_icon="💼",
    layout="wide",
)
st.title("💼 AI-Powered Job Recommendation (Groq)")

# Load .env if present
load_dotenv()

# -----------------------------
# Sidebar settings
# -----------------------------


# -----------------------------
# Inputs
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("👤 Your Profile")
    skills = st.text_area("Position (comma-separated)", placeholder="Data Analyst, Data Scientist, Data Engineer")
    experience = st.text_area("Experience", placeholder="1 year in data analytics; internships; projects")
    preferences = st.text_area("Preferences", placeholder="Bangalore; remote-friendly; full-time; salary > 10 LPA")

with col2:
    st.subheader("📄 Resume (optional)")
    resume_file = st.file_uploader("Upload PDF/TXT", type=["pdf", "txt"])
    resume_text = ""
    if resume_file:
        if resume_file.type == "text/plain":
            resume_text = resume_file.read().decode("utf-8", errors="ignore")
        else:
            resume_text = extract_text_from_pdf(resume_file)

        if resume_text.strip():
            with st.expander("Preview extracted text"):
                st.write(resume_text[:2000] + ("..." if len(resume_text) > 2000 else ""))

# Build user profile text
user_profile_text = build_user_profile_text(skills, experience, preferences, resume_text)

# -----------------------------
# Session state
# -----------------------------
st.session_state.setdefault("jobs", [])
st.session_state.setdefault("vectorstore", None)

# -----------------------------
# Load Jobs Button
# -----------------------------
if st.button("📚 Load Jobs & Build Index", use_container_width=True):
    try:
        if skills.strip():
            # ✅ Use Apify instead of RapidAPI JSearch
            jobs = fetch_linkedin_jobs(search_query=skills, location=preferences)

            if jobs:
                st.session_state.jobs = jobs
                st.session_state.vectorstore = build_vectorstore(jobs)
                st.success(f"Loaded {len(jobs)} jobs from Apify and built FAISS index ✅")

                # Display first 10 jobs
                with st.expander("📄 Current job corpus (first 10)"):
                    df = pd.DataFrame([
                        {
                            "Title": job.get("title"),
                            "Company": job.get("companyName"),
                            "Location": job.get("location"),
                            "Link": job.get("applyUrl")
                        }
                        for job in jobs[:10]
                    ])
                    st.dataframe(df)
            else:
                st.warning("No jobs found for your query.")
        else:
            st.warning("Please enter a job position/skills before loading jobs.")

    except Exception as e:
        st.error(f"Failed to load/build index: {e}")


# -----------------------------
# Recommend Jobs Button
# -----------------------------
if st.button("🎯 Recommend Jobs", use_container_width=True):
    if not os.getenv("GROQ_API_KEY"):
        st.error("Please set a valid GROQ_API_KEY in .env or Streamlit secrets.")
    elif not st.session_state.vectorstore:
        st.error("Please load jobs and build the index first.")
    elif not user_profile_text.strip():
        st.error("Please enter your skills/experience/preferences or upload a resume.")
    else:
        with st.spinner("Generating recommendations with Groq..."):
            try:
                retrieved_docs = retrieve(st.session_state.vectorstore, user_profile_text)
                retrieved_text = "".join(d.page_content for d in retrieved_docs)[:5000]

                # ✅ Using Groq's LLaMA 3 model
                llm = ChatGroq(
                    groq_api_key=os.getenv("GROQ_API_KEY"),
                    model_name="meta-llama/llama-4-scout-17b-16e-instruct",  # you can change to mixtral-8x7b
                    temperature=0.5
                )
                chain = LLMChain(llm=llm, prompt=job_recommendation_prompt)
                raw = chain.run(user_profile=user_profile_text, retrieved_jobs=retrieved_text)

                recs = safe_json_parse(raw)
                if not recs:
                    st.warning("Could not parse model output into JSON. Showing raw response.")
                    st.code(raw)
                else:
                    st.subheader("✅ Top Recommendations")
                    for r in recs:
                        with st.container(border=True):
                            st.markdown(f"### {r.get('Job Title','')} — {r.get('Company','')}")
                            st.write(r.get("Match Reason", ""))
                            if r.get("Apply Link"):
                                st.link_button("Apply / View", url=str(r.get("Apply Link")))

                    st.markdown("---")
                    st.markdown("**Table View**")
                    df = pd.DataFrame(recs)
                    st.dataframe(df, use_container_width=True)
                    csv = df.to_csv(index=False).encode("utf-8")
                    st.download_button("⬇️ Download CSV", csv, file_name="recommendations.csv", mime="text/csv")
            except Exception as e:
                st.error(f"Error generating recommendations: {e}")
