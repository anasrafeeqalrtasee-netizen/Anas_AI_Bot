import os
from flask import Flask
from threading import Thread
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

app = Flask('')
@app.route('/')
def home(): return "روبوت البرنس أنس شغال يا وحش!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

TELEGRAM_TOKEN = "8090646941:AAFYQTpzjCe-YT7ml4PPvJrDR4QTsjeLT1s"
GEMINI_API_KEY = "AIzaSyArhLwyapG_3AqC7JosJDtxKN1BKooDMBM"
USER_ID = 7991342562

# التعديل الذهبي هنا
genai.configure(api_key=GEMINI_API_KEY, transport='rest')
model = genai.GenerativeModel('gemini-1.5-flash')

async def handle_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != USER_ID: return
    try:
        # هنا سيخرج الذكاء الحقيقي
        response = model.generate_content(f"أنت مساعد أنس رفيق، طالب إداري وموظف بسما أبها. أجب بذكاء: {update.message.text}")
        await update.message.reply_text(response.text)
    except Exception as e:
        # لو حدث خطأ، سأخبرك ما هو بالضبط في تليجرام
        await update.message.reply_text(f"🤖 الذكاء يقول: {str(e)}")

if __name__ == "__main__":
    Thread(target=run).start()
    bot = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    bot.add_handler(MessageHandler(filters.TEXT, handle_chat))
    bot.run_polling()
    
