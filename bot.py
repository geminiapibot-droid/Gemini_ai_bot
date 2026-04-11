import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import google.generativeai as genai

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ── Config ────────────────────────────────────────────────────────────────────
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
MODEL_NAME     = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
MAX_HISTORY    = int(os.getenv("MAX_HISTORY", "20"))

# ── Gemini setup ──────────────────────────────────────────────────────────────
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

# In-memory conversation store  {chat_id: [{"role": ..., "parts": [...]}]}
conversations: dict[int, list] = {}


# ── Helpers ───────────────────────────────────────────────────────────────────
def get_history(chat_id: int) -> list:
    return conversations.setdefault(chat_id, [])


def trim_history(chat_id: int) -> None:
    h = conversations[chat_id]
    if len(h) > MAX_HISTORY:
        conversations[chat_id] = h[-MAX_HISTORY:]


async def ask_gemini(chat_id: int, user_text: str) -> str:
    history = get_history(chat_id)
    history.append({"role": "user", "parts": [user_text]})
    trim_history(chat_id)

    try:
        chat  = model.start_chat(history=history[:-1])
        reply = chat.send_message(user_text)
        answer = reply.text
    except Exception as exc:
        logger.error("Gemini error: %s", exc)
        answer = "⚠️ Gemini is unavailable. Please try again later."

    history.append({"role": "model", "parts": [answer]})
    return answer


# ── Handlers ──────────────────────────────────────────────────────────────────
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    name = update.effective_user.first_name
    await update.message.reply_text(
        f"👋 Welcome, {name}!\n\n"
        "👋 Welcome to Gemini AI Bot!\n\n"
        "🤖 Powered by Google Gemini 2.5 Flash\n\n"
        "✨ What I can do:\n"
        "• Answer any question instantly\n"
        "• Help with coding & debugging\n"
        "• Explain complex topics simply\n"
        "• Write essays, emails & stories\n"
        "• Translate languages\n"
        "• Solve math problems\n"
        "• Have natural conversations\n\n"
        "💬 Just send me any message and I'll reply!\n\n"
        "Commands:\n"
        "/start – Welcome message\n"
        "/reset – Clear conversation history\n"
        "/model – Show current AI model\n\n"
        "👨‍💻 Developed by @Sudhakaran12",
    )


async def reset(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    conversations.pop(update.effective_chat.id, None)
    await update.message.reply_text("🗑️ Conversation history cleared!")


async def show_model(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"🤖 Current model: `{MODEL_NAME}`", parse_mode="Markdown")


async def handle_message(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text
    chat_id   = update.effective_chat.id

    # Step 1 — Send waiting message
    waiting_msg = await update.message.reply_text("⏳ Please wait, generating reply...")

    # Step 2 — Show typing action
    await ctx.bot.send_chat_action(chat_id=chat_id, action="typing")

    # Step 3 — Get Gemini answer
    answer = await ask_gemini(chat_id, user_text)

    # Step 4 — Delete waiting message
    await waiting_msg.delete()

    # Step 5 — Send actual answer
    if len(answer) > 4096:
        for i in range(0, len(answer), 4096):
            await update.message.reply_text(answer[i : i + 4096])
    else:
        await update.message.reply_text(answer)


async def handle_error(update: object, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Update %s caused error: %s", update, ctx.error)


# ── Entry point ───────────────────────────────────────────────────────────────
def main() -> None:
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(CommandHandler("model", show_model))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(handle_error)

    logger.info("Bot is running with model: %s", MODEL_NAME)
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
    
