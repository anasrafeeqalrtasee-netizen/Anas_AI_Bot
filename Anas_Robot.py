import os
from flask import Flask
from threading import Thread
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# --- تشغيل سيرفر وهمي لخدعة Render وإبقاء البوت حياً ---
app = Flask('')
@app.route('/')
def home(): return "روبوت البرنس أنس يعمل بنجاح!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# --- إعدادات البرنس أنس ---
TELEGRAM_TOKEN = "8090646941:AAFYQTpzjCe-YT7ml4PPvJrDR4QTsjeLT1s"
GEMINI_API_KEY = "AIzaSyArhLwyapG_3AqC7JosJDtxKN1BKooDMBM"
USER_ID = 7991342562

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

async def handle_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != USER_ID: return
    try:
        # هنا الذكاء الاصطناعي سيرد عليك بحرية
        response = model.generate_content(f"أنت مساعد أنس رفيق، طالب إداري ذكي. أجب بذكاء: {update.message.text}")
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text("🤖 الروبوت مستيقظ وجاهز!")

if __name__ == "__main__":
    # تشغيل المنبه في الخلفية
    Thread(target=run).start()
    # تشغيل البوت
    bot = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    bot.add_handler(MessageHandler(filters.TEXT, handle_chat))
    print("🚀 الروبوت انطلق في منصة Render الحرة!")
    bot.run_polling()
