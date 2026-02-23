import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from yt_dlp import YoutubeDL

API_TOKEN = '8362871398:AAERtQR_OVJjGddYxHiRIy6-BcUs6t-MEeA'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Salom! Video linkini yuboring. (YouTube, TikTok, Instagram) 📥")

@dp.message(F.text.startswith("http"))
async def download_video(message: types.Message):
    url = message.text
    user_id = message.from_user.id
    status = await message.answer("Video yuklanmoqda... ⏳")
    
    file_path = f"v_{user_id}.mp4"
    
    ydl_opts = {
        'format': 'best[ext=mp4]/best', # Faqat MP4 formatini so'raymiz
        'outtmpl': file_path,
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'geo_bypass': True, # Bloklarni chetlab o'tishga urinish
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        if os.path.exists(file_path):
            video_file = types.FSInputFile(file_path)
            await message.answer_video(video_file, caption="Tayyor! ✅")
            os.remove(file_path)
        else:
            await message.answer("Fayl yuklandi, lekin topilmadi. ❌")
            
    except Exception as e:
        await message.answer("Kechirasiz, server videoni yuklay olmadi. Platforma botni bloklagan bo'lishi mumkin. ❌")
    
    await status.delete()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())





