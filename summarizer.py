from typing import List, Dict
import math
from openclaw_skill import summarize_chunks

CHUNK_TOKENS = 800

def _transcript_to_text(transcript: List[Dict]) -> str:
    return "\n".join([t.get("text", "") for t in transcript])

def _chunk_text(text: str, max_tokens=CHUNK_TOKENS) -> List[str]:
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_tokens):
        chunks.append(" ".join(words[i:i+max_tokens]))
    return chunks

def summarize_transcript(video_id: str, transcript: List[Dict], title: str, language: str = "en") -> str:
    text = _transcript_to_text(transcript)
    chunks = _chunk_text(text)
    payload_chunks = []
    for idx, c in enumerate(chunks):
        payload_chunks.append({"chunk_id": idx, "text": c})

    # try OpenClaw first
    try:
        summary = summarize_chunks(video_id, title, payload_chunks, language=language)
        return summary
    except Exception:
        # fallback naive summarization
        first = chunks[0] if chunks else ""
        return f"Title: {title}\n\nQuick summary (fallback):\n{first[:1000]}\n\n(Enable OpenClaw at OPENCLAW_URL for better summaries.)"
