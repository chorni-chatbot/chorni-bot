import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from yt_dlp import YoutubeDL
from aiohttp import web

# Bot token
API_TOKEN = '8362871398:AAERtQR_OVJjGddYxHiRIy6-BcUs6t-MEeA'
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Render kutayotgan "Port"ni ochish uchun kichik server
async def handle(request):
    return web.Response(text="Bot is live!")

app = web.Application()
app.router.add_get("/", handle)

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Salom! Video linkini yuboring, yuklab beraman! 📥")

@dp.message(F.text.startswith("http"))
async def download(message: types.Message):
    url = message.text
    msg = await message.answer("Yuklanmoqda... ⏳")
    path = f"v_{message.from_user.id}.mp4"
    try:
        # Eng yangi sozlamalar bilan yuklash
        ydl_opts = {
            'format': 'best',
            'outtmpl': path,
            'quiet': True,
            'no_warnings': True
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        await message.answer_video(types.FSInputFile(path), caption="Tayyor! ✅")
        os.remove(path)
    except Exception as e:
        await message.answer(f"Xatolik: Yuklab bo'lmadi. ❌")
    await msg.delete()

async def main():
    # Render'da port xatosini oldini olish
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv('PORT', 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    
    # Botni ishga tushirish
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())






