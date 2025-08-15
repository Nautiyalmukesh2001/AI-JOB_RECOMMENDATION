import json
from typing import List, Dict


def safe_json_parse(text: str) -> List[Dict]:
    """Try to parse LLM output as JSON array; fall back to extracting first [ ... ] block."""
    try:
        data = json.loads(text)
        return data if isinstance(data, list) else []
    except Exception:
        start = text.find("[")
        end = text.rfind("]")
        if start != -1 and end != -1 and end > start:
            snippet = text[start : end + 1]
            try:
                data = json.loads(snippet)
                return data if isinstance(data, list) else []
            except Exception:
                pass
    return []


def build_user_profile_text(skills: str, experience: str, preferences: str, resume_text: str, max_resume_chars: int = 4000) -> str:
    blocks = []
    if skills and skills.strip():
        blocks.append(f"Skills: {skills.strip()}")
    if experience and experience.strip():
        blocks.append(f"Experience: {experience.strip()}")
    if preferences and preferences.strip():
        blocks.append(f"Preferences: {preferences.strip()}")
    if resume_text and resume_text.strip():
        blocks.append("Resume Summary:" + resume_text.strip()[:max_resume_chars])
    return "".join(blocks)