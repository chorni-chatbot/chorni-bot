import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from yt_dlp import YoutubeDL

# Bot tokeningiz
API_TOKEN = '8362871398:AAERtQR_OVJjGddYxHiRIy6-BcUs6t-MEeA'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        "Salom! Men video yuklovchi botman. 📥\n\n"
        "Menga Instagram, TikTok yoki YouTube linkini yuboring, "
        "men uni sizga video formatida yuklab beraman!"
    )

@dp.message(F.text.startswith("http"))
async def download_video(message: types.Message):
    url = message.text
    user_id = message.from_user.id
    status = await message.answer("Video yuklanmoqda, iltimos kuting... ⏳")
    
    # Video yuklash sozlamalari
    file_path = f"video_{user_id}.mp4"
    ydl_opts = {
        'format': 'best',
        'outtmpl': file_path,
        'noplaylist': True,
        'quiet': True
    }
    
    try:
        # Videoni serverga yuklash
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # Videoni Telegramga yuborish
        video_file = types.FSInputFile(file_path)
        await message.answer_video(video_file, caption="Tayyor! ✅\n@chornichatuzbot orqali yuklandi.")
        
        # Serverdan faylni o'chirish (joy egallamasligi uchun)
        if os.path.exists(file_path):
            os.remove(file_path)
            
    except Exception as e:
        await message.answer("Kechirasiz, videoni yuklashda xatolik yuz berdi. Linkni tekshiring yoki keyinroq urinib ko'ring. ❌")
    
    await status.delete()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())




