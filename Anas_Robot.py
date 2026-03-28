import os
from flask import Flask
from threading import Thread
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

app = Flask('')
@app.route('/')
def home(): return "الروبوت مستعد لخدمة أنس!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

TELEGRAM_TOKEN = "8090646941:AAFYQTpzjCe-YT7ml4PPvJrDR4QTsjeLT1s"
GEMINI_API_KEY = "AIzaSyArhLwyapG_3AqC7JosJDtxKN1BKooDMBM"
USER_ID = 7991342562

# التعديل المستقر هنا
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro') # هذا هو الموديل المستقر

async def handle_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != USER_ID: return
    try:
        response = model.generate_content(f"أنت مساعد أنس رفيق، طالب إداري من مأرب. أجب بذكاء: {update.message.text}")
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"🤖 خطأ بسيط، جرب سؤاله مرة أخرى.")

if __name__ == "__main__":
    Thread(target=run).start()
    bot = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    bot.add_handler(MessageHandler(filters.TEXT, handle_chat))
    bot.run_polling()
    
