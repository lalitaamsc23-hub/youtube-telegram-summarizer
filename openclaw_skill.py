import os
import requests
from typing import List, Dict, Any

OPENCLAW_URL = os.getenv("OPENCLAW_URL", "http://localhost:8000")

def summarize_chunks(video_id: str, title: str, chunks: List[Dict[str, Any]], language: str = "en") -> str:
    """Call local OpenClaw summarization skill. Expects an endpoint /skill/summarize"""
    try:
        payload = {"video_id": video_id, "title": title, "chunks": chunks, "language": language}
        r = requests.post(f"{OPENCLAW_URL}/skill/summarize", json=payload, timeout=30)
        r.raise_for_status()
        return r.json().get("summary", r.text)
    except Exception as e:
        raise RuntimeError(f"OpenClaw summarize error: {e}")

def answer_question(context_text: str, question: str, language: str = "en") -> str:
    try:
        payload = {"context": context_text, "question": question, "language": language}
        r = requests.post(f"{OPENCLAW_URL}/skill/answer", json=payload, timeout=20)
        r.raise_for_status()
        return r.json().get("answer", r.text)
    except Exception as e:
        raise RuntimeError(f"OpenClaw answer error: {e}")
