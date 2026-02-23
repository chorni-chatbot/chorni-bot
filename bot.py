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
    await message.answer("Salom! Link yuborsangiz video yuklayman, ism yozsangiz musiqa topaman! 🎵🎥")

@dp.message()
async def handle_all(message: types.Message):
    if not message.text: return
    
    text = message.text
    msg = await message.answer("Bajarilmoqda... 🚀")

    # 1. VIDEO YUKLASH (Instagram, YouTube, TikTok linklari bo'lsa)
    if "http" in text:
        ydl_opts = {
            'format': 'best',
            'outtmpl': f'v_{message.from_user.id}.mp4',
            'noplaylist': True,
        }
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([text])
            await message.answer_video(types.FSInputFile(f'v_{message.from_user.id}.mp4'), caption="Mana video! 🎥")
            os.remove(f'v_{message.from_user.id}.mp4')
        except Exception:
            await message.answer("Videoni yuklashda xatolik yuz berdi. ❌")
            
    # 2. MUSIQA QIDIRISH (Shunchaki ism yoki nom yozilsa)
    else:
        # YouTube'dan qidirib, MP3 qilib berish sozlamasi
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'm_{message.from_user.id}.mp3',
            'default_search': 'ytsearch1', # YouTube'dan 1-chi natijani qidiradi
            'noplaylist': True,
        }
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([text])
            
            audio = types.FSInputFile(f'm_{message.from_user.id}.mp3')
            await message.answer_audio(audio, caption=f"Topildi: {text} 🎵")
            os.remove(f'm_{message.from_user.id}.mp3')
        except Exception:
            await message.answer("Musiqa topilmadi. Iltimos, boshqacharoq yozib ko'ring. 😔")
    
    await msg.delete()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())



