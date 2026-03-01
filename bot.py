import logging
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from transcript import fetch_transcript_and_title
from summarizer import summarize_transcript
from qa_engine import answer_question_for_user

BOT_TOKEN = "8605032825:AAH3uYrCjLRDWKPA7iLX2woDN1d2kqGMg6k"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

VIDEO_URL_RE = re.compile(r"(?:v=|youtu\.be/)([A-Za-z0-9_-]{8,})")

def extract_video_id(text: str):
    m = VIDEO_URL_RE.search(text)
    return m.group(1) if m else None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome! 🎥\n"
        "Send a YouTube link to get a structured summary.\n"
        "Use /deepdive to ask questions after a summary.\n\n"
        "Commands:\n"
        "/summary <link>\n"
        "/deepdive"
    )

async def summary_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""
    vid = extract_video_id(text)
    if not vid and context.args:
        vid = extract_video_id(" ".join(context.args))

    if not vid:
        await update.message.reply_text("❌ Please send a valid YouTube link.")
        return

    await update.message.reply_text("⏳ Fetching transcript and creating summary...")
    transcript, title = fetch_transcript_and_title(vid)

    if not transcript:
        await update.message.reply_text("⚠️ Transcript not available for that video.")
        return

    summary = summarize_transcript(vid, transcript, title)
    context.user_data["last_video"] = {
        "video_id": vid,
        "title": title,
        "transcript": transcript
    }

    await update.message.reply_text(summary)

async def deepdive_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["deepdive"] = True
    await update.message.reply_text("🔎 Deepdive mode enabled. Ask questions about the last summarized video.")

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""
    vid = extract_video_id(text)

    if vid:
        await summary_cmd(update, context)
        return

    if context.user_data.get("deepdive") and context.user_data.get("last_video"):
        q = text.strip()
        if not q:
            await update.message.reply_text("Please ask a question about the video.")
            return

        answer = answer_question_for_user(context.user_data["last_video"], q)
        await update.message.reply_text(answer)
        return

    await update.message.reply_text("Send a YouTube link or use /summary <link>.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("summary", summary_cmd))
    app.add_handler(CommandHandler("deepdive", deepdive_cmd))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), message_handler))

    logger.info("Starting bot...")
    app.run_polling()

if __name__ == "__main__":
    main()