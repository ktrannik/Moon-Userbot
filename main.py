import asyncio
import os
from fastapi import FastAPI
from pyrogram import Client, filters

# ===== FastAPI для Render =====
app = FastAPI()

@app.get("/")
async def health():
    return {"status": "ok"}

# ===== Инициализация юзербота =====
userbot = Client(
    name="moon-userbot",
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH"),
    session_string=os.getenv("STRINGSESSION")
)

# ===== ОБРАБОТЧИК КОМАНД =====
@userbot.on_message(filters.command("ping", prefixes="."))
async def ping_command(client, message):
    await message.reply_text("🏓 Pong!")

# ===== ЗАПУСК ЮЗЕРБОТА =====
async def run_userbot():
    try:
        await userbot.start()
        print("🤖 Moon-Userbot успешно запущен!")
        # Бесконечное ожидание с обработчиками
        await asyncio.Event().wait()
    except Exception as e:
        print(f"❌ Ошибка: {e}")

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(run_userbot())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
