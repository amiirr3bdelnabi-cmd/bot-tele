import asyncio
import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

TELEGRAM_TOKEN = "7956406797:AAFpZ70QffJcrkfNuAkJQJac2F_ASL4cms8"
GEMINI_API_KEY = "AQ.Ab8RN6JfXvqGA-R4aREXJQmVMdq4ElB3_KXtWrNvwD-gcs6SSw"


def ask_gemini(text):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent"

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GEMINI_API_KEY
    }

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": text
                    }
                ]
            }
        ],
        "generationConfig": {
            "maxOutputTokens": 300,
            "temperature": 0.7
        }
    }

    response = requests.post(
        url,
        headers=headers,
        json=data,
        timeout=30
    )

    print("STATUS:", response.status_code)

    if response.status_code != 200:
        print("RESPONSE:", response.text)

    response.raise_for_status()

    result = response.json()

    return result["candidates"][0]["content"]["parts"][0]["text"]


async def reply_to_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if not update.message or not update.message.text:
        return

    user_text = update.message.text

    try:
        # نشغل طلب Gemini بدون ما نوقف البوت
        reply = await asyncio.to_thread(
            ask_gemini,
            user_text
        )

        await update.message.reply_text(reply)

    except Exception as e:
        print("ERROR:", repr(e))

        await update.message.reply_text(
            "حصل خطأ، بص على شاشة التشغيل لمعرفة السبب."
        )


def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            reply_to_message
        )
    )

    print("البوت اشتغل ✅")

    app.run_polling()


if __name__ == "__main__":
    main()