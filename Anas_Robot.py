import os
from flask import Flask
from threading import Thread
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# --- تشغيل منبه بسيط لإبقاء السيرفر مستيقظاً ---
app = Flask('')
@app.route('/')
def home(): return "روبوت البرنس أنس يعمل بنجاح بمفتاحه الخاص!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# --- إعدادات البرنس أنس (المفاتيح الجديدة) ---
TELEGRAM_TOKEN = "8090646941:AAFYQTpzjCe-YT7ml4PPvJrDR4QTsjeLT1s"
GEMINI_API_KEY = "AIzaSyBKlf85SnenZhKoAcmsFMvKyO1LHceVv04" # مفتاحك الجديد
USER_ID = 7991342562

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

async def handle_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # التأكد أن أنس هو فقط من يتحكم بالبوت
    if update.message.from_user.id != USER_ID: return
    
    try:
        # استدعاء الذكاء الاصطناعي
        response = model.generate_content(
            f"أنت المساعد الشخصي لأنس رفيق، خبير إدارة أعمال. أجب بذكاء وواقعية: {update.message.text}"
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        # في حال حدوث ضغط لحظي من جوجل
        await update.message.reply_text("🤖 يا برنس، الذكاء يحتاج ثواني ليركز، أعد إرسال سؤالك.")
        print(f"Error: {e}")

if __name__ == "__main__":
    # تشغيل المنبه في الخلفية
    Thread(target=run).start()
    # إطلاق البوت
    bot = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    bot.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_chat))
    print("🚀 مبروك! البوت انطلق بمفتاحك الخاص على Render.")
    bot.run_polling()
    
