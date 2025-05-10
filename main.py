import logging
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import os

# === 🔐 Get credentials from environment variables ===
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

# === 🎓 Custom GPT Instructions ===
SYSTEM_PROMPT = "You are a helpful assistant that answers briefly and clearly."

# === 🤖 GPT Handler Function ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    try:
        # Send to OpenAI GPT API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response.choices[0].message.content.strip()
        await update.message.reply_text(reply)

    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("⚠️ Sorry, something went wrong.")

# === 🟢 Start Command ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hi! I'm your GPT bot. Ask me anything.")

# === 🚀 Main Bot Setup ===
def main():
    app = ApplicationBuilder().token('8135129182:AAFzuChkeaZHjVLA0oztBrCct4pG1P8WUNI').build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
