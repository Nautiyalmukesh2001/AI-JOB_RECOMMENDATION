# AI Job Recommendation System (LangChain + Groq)

This project is an AI-powered job recommendation system that leverages [LangChain](https://github.com/langchain-ai/langchain), [Groq](https://groq.com/), and vector search (FAISS) to match users with relevant job postings based on their profile, skills, preferences, and resume.

---

## Features

- **AI-Powered Recommendations:** Uses LLMs (Groq Llama 3/4) to recommend jobs tailored to your profile.
- **Semantic Search:** Retrieves the most relevant jobs using vector embeddings and FAISS.
- **Resume Parsing:** Extracts text from uploaded PDF or TXT resumes.
- **Live Job Fetching:** Integrates with Apify to fetch real LinkedIn job postings.
- **Interactive UI:** Built with Streamlit for easy user interaction.
- **Downloadable Results:** Export recommendations as CSV.

---

## Project Structure

```
.env
app.py
data_loader.py
job_api.py
prompt.py
rag.py
readme.md
requirements.txt
resume.py
utils.py
__pycache__/
```

---

## File Overview

- [`app.py`](app.py): Main Streamlit app for user interaction and orchestration.
- [`data_loader.py`](data_loader.py): Loads and normalizes job data from CSV.
- [`job_api.py`](job_api.py): Fetches jobs from Apify (LinkedIn).
- [`prompt.py`](prompt.py): LLM prompt template for job recommendations.
- [`rag.py`](rag.py): RAG pipeline: vector store, retrieval, embeddings.
- [`resume.py`](resume.py): Resume PDF/TXT extraction.
- [`utils.py`](utils.py): Utilities for parsing and formatting.
- [`requirements.txt`](requirements.txt): Python dependencies.
- [`.env`](.env): API keys and secrets.

---

## Setup

1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd ai_job_recommendation
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Configure API keys:**
   - Edit the `.env` file and fill in your keys:
     - `GROQ_API_KEY` (for Groq LLM)
     - `APIFY_API_TOKEN` (for Apify LinkedIn jobs)
     - `RAPIDAPI_KEY` (optional, not used by default)

4. **Run the app:**
   ```sh
   streamlit run app.py
   ```

---

## Usage

1. **Enter your profile:** Fill in your skills, experience, and preferences. <img width="1804" height="860" alt="Screenshot 2025-08-15 234859" src="https://github.com/user-attachments/assets/25afc648-6099-4b15-a6fd-c507be74ea05" />
2. **Upload your resume (optional):** PDF or TXT supported.
3. **Load jobs:** Click "Load Jobs & Build Index" to fetch and index jobs.
4. **Get recommendations:** Click "Recommend Jobs" to see personalized matches.
5. **Download results:** Export recommendations as CSV.



<img width="1798" height="815" alt="Screenshot 2025-08-15 235010" src="https://github.com/user-attachments/assets/8621e70e-c0a2-453d-b205-8e5d8c0e1302" />

<img width="1784" height="769" alt="Screenshot 2025-08-15 235025" src="https://github.com/user-attachments/assets/21f21d5e-1268-470c-8677-5d1e98d524b7" />

---

## Notes

- Requires Python 3.8+.
- Uses [sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) for embeddings.
- LLM runs via Groq API (fast inference, Llama 3/4).
- Job data fetched from LinkedIn via Apify actor.

---

## License

MIT License

---

**Made with ❤️ using LangChain, Groq, and
