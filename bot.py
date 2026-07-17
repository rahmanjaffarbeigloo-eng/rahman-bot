import os
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from groq import Groq

# اینا رو توی Render به عنوان متغیر محیطی تنظیم می‌کنیم
TOKEN = os.environ.get('BOT_TOKEN')
GROQ_API = os.environ.get('GROQ_API_KEY')
client = Groq(api_key=GROQ_API)

RAHMAN_PROMPT = """تو رحمان هستی. کوتاه، سرد، محاوره‌ای و بدون تعارف جواب بده. 
اگر سوال چرت بود یا وقتت رو گرفت، با بی‌حوصلگی جواب بده. وقت تلف نکن."""

async def handle_message(update, context):
    text = update.message.text
    response = client.chat.completions.create(
        messages=[{"role": "system", "content": RAHMAN_PROMPT}, {"role": "user", "content": text}],
        model="llama-3.3-70b-versatile"
    )
    await update.message.reply_text(response.choices[0].message.content)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()
