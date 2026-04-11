# 🤖 Gemini Telegram Bot

A Telegram bot powered by **Google Gemini**, deployable to **Railway** in minutes via GitHub.

---

## ✨ Features

- 💬 Multi-turn conversations with memory per chat
- ⚡ Powered by Gemini 1.5 Flash (or Pro)
- 🔄 `/reset` to clear conversation history
- 📦 One-click Railway deployment via GitHub
- 🔒 Environment-variable based secrets (no hardcoded keys)

---

## 🚀 Quick Start

### 1 — Get your API keys

| Key | Where to get it |
|-----|----------------|
| `TELEGRAM_TOKEN` | [@BotFather](https://t.me/BotFather) → `/newbot` |
| `GEMINI_API_KEY` | [Google AI Studio](https://aistudio.google.com/app/apikey) |

---

### 2 — Fork & clone this repo

```bash
git clone https://github.com/YOUR_USERNAME/gemini-telegram-bot.git
cd gemini-telegram-bot
```

---

### 3 — Local development (optional)

```bash
cp .env.example .env
# Fill in TELEGRAM_TOKEN and GEMINI_API_KEY in .env

pip install -r requirements.txt
python bot.py
```

---

### 4 — Deploy to Railway

1. Push your fork to GitHub.
2. Go to [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub repo**.
3. Select your forked repo.
4. Click **Variables** and add:

   | Variable | Value |
   |----------|-------|
   | `TELEGRAM_TOKEN` | your token |
   | `GEMINI_API_KEY` | your key |
   | `GEMINI_MODEL` | `gemini-1.5-flash` *(optional)* |
   | `MAX_HISTORY` | `20` *(optional)* |

5. Railway auto-detects `railway.json` and deploys. Done! ✅

---

## 🛠 Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome message |
| `/reset` | Clear conversation history |
| `/model` | Show active Gemini model |

---

## 📁 Project Structure

```
gemini-telegram-bot/
├── bot.py            # Main bot logic
├── requirements.txt  # Python dependencies
├── Procfile          # Railway/Heroku process file
├── railway.json      # Railway deployment config
├── .env.example      # Environment variable template
└── .gitignore
```

---

## 🔄 Switching Models

Change `GEMINI_MODEL` in Railway variables:

- `gemini-1.5-flash` — fast & free tier friendly *(default)*
- `gemini-1.5-pro`   — more powerful, higher quota cost

---

## 📄 License

MIT

