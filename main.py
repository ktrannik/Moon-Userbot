import asyncio
import os
from fastapi import FastAPI
from pyrogram import Client

# ===== Создаём ASGI-приложение для Render =====
app = FastAPI()

@app.get("/")
async def health():
    """Эндпоинт для проверки жизнеспособности Render"""
    return {"status": "ok"}

@app.get("/health")
async def health_check():
    """Дополнительный эндпоинт для надёжности"""
    return {"status": "alive"}

# ===== Инициализация твоего юзербота =====
# Создаём клиент Pyrogram с твоими данными
# (данные берутся из переменных окружения Render)
userbot = Client(
    name="moon-userbot",
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH"),
    session_string=os.getenv("STRINGSESSION")
)

# ===== Функция запуска юзербота =====
async def run_userbot():
    """Запускает Pyrogram клиент в фоне"""
    try:
        await userbot.start()
        print("🤖 Moon-Userbot успешно запущен!")
        # Здесь твой код с обработчиками (нажатие кнопок, расписание и т.д.)
        await userbot.join_chat("https://t.me/moon_userbot_chat")  # пример
        await asyncio.Event().wait()  # Бесконечное ожидание
    except Exception as e:
        print(f"❌ Ошибка при запуске юзербота: {e}")

from pyrogram import Client, filters

async def run_userbot():
    try:
        await userbot.start()
        print("🤖 Moon-Userbot успешно запущен!")

        # ===== ДОБАВЛЯЕМ ОБРАБОТЧИК КОМАНД =====
        @userbot.on_message(filters.command("ping", prefixes="."))
        async def ping_command(client, message):
            await message.reply_text("🏓 Pong!")

        # Здесь будут другие обработчики (для /click, /schedule и т.д.)

        await asyncio.Event().wait()  # Бесконечное ожидание
    except Exception as e:
        print(f"❌ Ошибка при запуске юзербота: {e}")

# ===== Запускаем FastAPI и юзербота вместе =====
@app.on_event("startup")
async def startup_event():
    """Запускает юзербота при старте FastAPI"""
    asyncio.create_task(run_userbot())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
