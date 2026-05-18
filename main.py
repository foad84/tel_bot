from fastapi import FastAPI, Request
from telegram import Update, Bot
from telegram.ext import Application
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = Bot(token=TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

app = FastAPI()

telegram_app = Application.builder().token(TOKEN).build()


@app.post("/")
async def webhook(request: Request):
    data = await request.json()

    update = Update.de_json(data, bot)

    if update.message:
        user_message = update.message.text
        chat_id = update.message.chat.id

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "user", "content": user_message}
            ]
        )

        reply = response.choices[0].message.content

        await bot.send_message(chat_id=chat_id, text=reply)

    return {"ok": True}
