import os
import json
import urllib.request
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

app = Flask('')
@app.route('/')
def home(): return "بوت البرنس أنس صاحي وشغال!"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

TELEGRAM_TOKEN = "8090646941:AAFYQTpzjCe-YT7ml4PPvJrDR4QTsjeLT1s"
GEMINI_API_KEY = "AIzaSyBKlf85SnenZhKoAcmsFMvKyO1LHceVv04"
USER_ID = 7991342562

def ask_ai(text):
    # تم تغيير الموديل هنا إلى gemini-pro المستقر
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    data = json.dumps({
        "contents": [{"parts": [{"text": f"أنت صديق ومساعد لأنس رفيق. أجب بذكاء: {text}"}]}]
    }).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"عطل فني: {str(e)}"

async def handle_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != USER_ID: return
    reply = ask_ai(update.message.text)
    await update.message.reply_text(reply)

if __name__ == "__main__":
    Thread(target=run).start()
    bot = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    bot.add_handler(MessageHandler(filters.TEXT, handle_chat))
    bot.run_polling()
    
