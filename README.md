# YouTube Telegram Summarizer & Q&A Bot (OpenClaw)

This template implements a Telegram bot that fetches YouTube transcripts, summarizes videos via a local OpenClaw skill (if available), and supports Q&A on the last summarized video.

Setup

- Copy `.env.example` to `.env` and set `BOT_TOKEN` (required) and optionally `OPENCLAW_URL`.
  Alternatively, you may hardcode a token in `bot.py` but this is less secure.
- Install dependencies:

```bash
pip install -r requirements.txt
```

- Run the bot:

```bash
python bot.py
```

OpenClaw

This template expects a local OpenClaw service exposing two endpoints:

- `POST /skill/summarize` with JSON {video_id, title, chunks, language} -> returns {summary}
- `POST /skill/answer` with JSON {context, question, language} -> returns {answer}

If you don't have OpenClaw running, the code falls back to simple heuristics, but for best results run OpenClaw and implement the two endpoints.

Files

- bot.py — Telegram bot wiring
- transcript.py — transcript fetcher + SQLite cache
- summarizer.py — chunking + OpenClaw summarizer wrapper
- qa_engine.py — question-answering over transcript
- openclaw_skill.py — HTTP wrapper to OpenClaw
- translator.py — simple translator wrapper (uses `deep-translator`)
- requirements.txt — Python deps

Notes

- This is a minimal template. Replace OpenClaw calls with your own LLM calls if needed.
- The transcript cache is `cache.db` in the repo directory.
