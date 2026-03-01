from typing import Dict, Any, List
import re
from openclaw_skill import answer_question

def _split_chunks(transcript: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    # create simple chunks with timestamps
    chunks = []
    current = {"start": 0.0, "text": ""}
    for seg in transcript:
        text = seg.get("text", "")
        start = seg.get("start", 0.0)
        if len(current["text"]) > 800:
            chunks.append(current)
            current = {"start": start, "text": text}
        else:
            if current["text"]:
                current["text"] += " " + text
            else:
                current["text"] = text
    if current["text"]:
        chunks.append(current)
    return chunks

def _score_overlap(a: str, b: str) -> int:
    aw = set(re.findall(r"\w+", a.lower()))
    bw = set(re.findall(r"\w+", b.lower()))
    return len(aw & bw)

def answer_question_for_user(last_video: Dict[str, Any], question: str, language: str = "en") -> str:
    transcript = last_video.get("transcript", [])
    title = last_video.get("title", "Untitled")
    chunks = _split_chunks(transcript)
    # pick best chunk by overlap
    best = None
    best_score = -1
    for c in chunks:
        s = _score_overlap(c.get("text", ""), question)
        if s > best_score:
            best_score = s
            best = c

    if best and best_score > 0:
        context = f"Title: {title}\n\n{best.get('text','')}"
    else:
        context = f"Title: {title}\n\n" + "\n".join([c.get("text","") for c in chunks[:3]])

    try:
        return answer_question(context, question, language=language)
    except Exception:
        # fallback simple answer: echo best chunk excerpt
        if best:
            excerpt = best.get("text", "")[:800]
            return f"Best context excerpt:\n{excerpt}"
        return "I couldn't find an answer in the transcript."
