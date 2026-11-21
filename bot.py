
import os
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from groq import AsyncGroq

TOKEN = os.environ["BOT_TOKEN"]
client = AsyncGroq(api_key=os.environ["GROQ_API_KEY"])

RAHMAN_PROMPT = """
تو نسخه هوش مصنوعی رحمان هستی.

فارسی محاوره‌ای و طبیعی حرف بزن.
کوتاه، باهوش، کمی طعنه‌آمیز و بدون تعارف باش.
مثل یک آدم واقعی گفتگو کن.
از شخصیت، لحن و شیوه فکر رحمان الگوبرداری کن.
اگر چیزی را نمی‌دانی، ادعای دانستن نکن.
"""

async def handle_message(update, context):
    message = update.effective_message

    if not message or not message.text:
        return

    business_id = getattr(message, "business_connection_id", None)

    # جلوگیری از پاسخ به پیام‌های خود رحمان
    if business_id:
        connection = await context.bot.get_business_connection(
            business_id
        )

        if message.from_user and message.from_user.id == connection.user.id:
            return

    try:
        result = await client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": RAHMAN_PROMPT},
                {"role": "user", "content": message.text}
            ]
        )

        answer = result.choices[0].message.content

        if not answer:
            return

        if business_id:
            await context.bot.send_message(
                chat_id=message.chat.id,
                text=answer,
                business_connection_id=business_id
            )
        else:
            await message.reply_text(answer)

    except Exception as error:
        print(f"ERROR: {error}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    app.run_polling(
        allowed_updates=[
            "message",
            "business_message",
            "business_connection"
        ]
    )
