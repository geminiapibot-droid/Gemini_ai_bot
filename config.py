# Pyrogram setup
API_ID = "31476539"  # Replace this API ID with your actual API ID
API_HASH = "1fe6cd52cde03cdc0c2571ed750c19f4"  # Replace this API HASH with your actual API HASH
BOT_TOKEN = "8704218693:AAFvEBFPzO19yFHylXlcE-qj9NxQ-1GZZcU"  # Replace this BOT_TOKEN

# Google Api Key
GOOGLE_API_KEY = "AIzaSyBy8n080qZZr5ipa2fO-AMxBFkSPM0LvcA"  # Replace this Google Api Key
MODEL_NAME = "gemini-1.5-flash" # Don't Change this model
import os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-1.5-flash")
