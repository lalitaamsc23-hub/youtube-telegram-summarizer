import sqlite3
import json
import time
from typing import Tuple, Optional, List
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled
from youtube_transcript_api.formatters import TextFormatter
import requests

DB = "cache.db"

def _init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS transcripts (
        video_id TEXT PRIMARY KEY,
        transcript_json TEXT,
        title TEXT,
        fetched_at REAL
    )
    """)
    conn.commit()
    conn.close()

def _get_cached(video_id: str) -> Optional[Tuple[List[dict], str]]:
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT transcript_json, title FROM transcripts WHERE video_id=?", (video_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    return json.loads(row[0]), row[1]

def _save_cached(video_id: str, transcript: List[dict], title: str):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("REPLACE INTO transcripts (video_id, transcript_json, title, fetched_at) VALUES (?,?,?,?)",
                (video_id, json.dumps(transcript), title, time.time()))
    conn.commit()
    conn.close()

def _fetch_title(video_id: str) -> str:
    # lightweight title fetch via YouTube oEmbed
    try:
        r = requests.get(f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json", timeout=5)
        if r.ok:
            return r.json().get("title", "Untitled")
    except Exception:
        pass
    return "Untitled"

def fetch_transcript_and_title(video_id: str):
    _init_db()
    cached = _get_cached(video_id)
    if cached:
        return cached

    try:
        # list_transcripts was removed in recent versions; use instance method `list`
        ytt = YouTubeTranscriptApi()
        transcript_list = ytt.list(video_id)

        # Try manually created English first
        try:
            transcript_obj = transcript_list.find_manually_created_transcript(["en"]).fetch()
        except NoTranscriptFound:
            # Fallback to auto-generated English
            transcript_obj = transcript_list.find_generated_transcript(["en"]).fetch()

        # convert to plain list of dicts so it's JSON-serializable
        # each item is a dataclass-like FetchedTranscriptSnippet
        transcript = [
            {"start": s.start, "duration": s.duration, "text": s.text}
            for s in transcript_obj
        ]

    except (TranscriptsDisabled, NoTranscriptFound, Exception) as e:
        print("Transcript error:", e)
        return None, None

    title = _fetch_title(video_id)
    _save_cached(video_id, transcript, title)
    return transcript, title