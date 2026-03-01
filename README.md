# 🚀 YouTube Telegram Summarizer & Q&A Bot

**AI-powered Telegram bot for summarizing YouTube videos and answering questions from transcripts**

This project implements a production-ready **Telegram bot** that:

* Extracts transcripts from YouTube videos
* Summarizes long videos using an LLM pipeline (via OpenClaw or fallback logic)
* Allows users to ask follow-up questions (“deep dive” mode)
* Caches transcripts locally for faster repeated queries

Designed as a **job assessment–ready project** showcasing:

* API integrations
* Async bot architecture
* NLP pipeline design
* Clean modular Python structure

---

## ✨ Features

✅ Telegram bot interface
✅ Automatic YouTube transcript extraction
✅ Video summarization pipeline
✅ Question answering over video content
✅ Local caching with SQLite
✅ Optional LLM integration (OpenClaw)
✅ Fallback summarization logic when LLM is unavailable
✅ Modular & extensible design

---

## 🧠 Architecture & Pipeline

```text
User (Telegram)
      │
      ▼
Telegram Bot (python-telegram-bot)
      │
      ▼
YouTube URL Parser
      │
      ▼
Transcript Fetcher (youtube-transcript-api)
      │
      ▼
Transcript Chunking
      │
      ├──▶ LLM Summarization (OpenClaw Skill API)
      │
      └──▶ Fallback Summarizer (local heuristic)
      │
      ▼
Summary Response to User
      │
      ▼
Deep Dive Mode → Question Answering over Transcript
```

---

## 📂 Project Structure

```bash
youtube-telegram-summarizer/
│
├── bot.py              # Telegram bot entrypoint
├── transcript.py       # Transcript fetching + SQLite caching
├── summarizer.py       # Chunking + summarization pipeline
├── qa_engine.py        # Question answering logic
├── openclaw_skill.py   # OpenClaw HTTP client
├── translator.py       # Optional translation wrapper
├── requirements.txt    # Dependencies
├── cache.db            # Local transcript cache
├── .env.example        # Environment variable template
└── README.md
```

---

## ⚙️ Setup & Installation

### 1️⃣ Clone the repo

```bash
git clone https://github.com/lalitaamsc23-hub/youtube-telegram-summarizer.git
cd youtube-telegram-summarizer
```

### 2️⃣ Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Setup environment variables

Create `.env`:

```bash
cp .env.example .env
```

Edit `.env`:

```env
BOT_TOKEN=your_telegram_bot_token_here
OPENCLAW_URL=http://localhost:8000   # optional
```

---

## ▶️ Run the Bot

```bash
python bot.py
```

Open Telegram → search your bot → send a YouTube link.

---

## 🤖 Telegram Commands

| Command             | Description                               |
| ------------------- | ----------------------------------------- |
| `/start`            | Start the bot                             |
| `/summary`          | Summarize a YouTube video                 |
| `/deepdive`         | Ask questions about last summarized video |
| *(or paste a link)* | Auto summarize                            |

---

## 🧩 OpenClaw (Optional LLM Backend)

If OpenClaw is running locally, the bot will call these endpoints:

### Summarization

```http
POST /skill/summarize
{
  "video_id": "...",
  "title": "...",
  "chunks": ["..."],
  "language": "en"
}
```

### Q&A

```http
POST /skill/answer
{
  "context": "...",
  "question": "...",
  "language": "en"
}
```

If OpenClaw is unavailable, the system falls back to local heuristic summarization.

---

## 🧪 Example Use Case

1. User sends a YouTube link
2. Bot extracts transcript
3. Transcript is chunked
4. LLM summarizes content
5. User asks:

   > “What is the main takeaway?”
6. Bot answers using transcript context

---

## 🔐 Security Notes

* `.env` is excluded from Git
* Telegram token is never hardcoded
* Local caching avoids repeated API calls

---

## 🛠 Tech Stack

* Python 3.10+
* python-telegram-bot
* youtube-transcript-api
* SQLite
* HTTP APIs
* Async I/O
* LLM integration (OpenClaw)

---

## 📌 Improvements (Roadmap)

* 🌐 Web UI
* 🧠 Vector embeddings for better Q&A
* 📊 Multi-video comparison
* ☁ Cloud deployment
* 🔐 OAuth user sessions
* 🧪 Unit tests

---

## 👨‍💻 Author

**Lalit**
Job Assessment Project – AI/NLP Engineering

---

