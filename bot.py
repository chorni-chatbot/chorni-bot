import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from yt_dlp import YoutubeDL

# BotFather'dan olgan tokeningiz
API_TOKEN = '8362871398:AAERtQR_OVJjGddYxHiRIy6-BcUs6t-MEeA'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Salom! Instagram yoki YouTube linkini yuboring, men uni yuklab beraman.")

@dp.message(F.text.contains("instagram.com") | F.text.contains("youtube.com") | F.text.contains("youtu.be"))
async def download_video(message: types.Message):
    url = message.text
    msg = await message.answer("Yuklanmoqda, iltimos kuting...")
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.mp4',
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        video = types.FSInputFile("video.mp4")
        await message.answer_video(video, caption="Tayyor!")
        os.remove("video.mp4")
        await msg.delete()
    except Exception as e:
        await message.answer(f"Xatolik yuz berdi: {e}")

async def main():
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
