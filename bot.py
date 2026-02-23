import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from yt_dlp import YoutubeDL

API_TOKEN = '8362871398:AAERtQR_OVJjGddYxHiRIy6-BcUs6t-MEeA'
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Salom! Link yuboring, videoni va musiqasini yuklab beraman! 🎵🎥")

@dp.message(F.text)
async def handle_all(message: types.Message):
    url = message.text
    if not url.startswith("http"):
        # Musiqa qidirish (YouTube orqali)
        msg = await message.answer("Musiqa qidirilmoqda... 🔍")
        opts = {'format': 'bestaudio/best', 'outtmpl': 'm.mp3', 'default_search': 'ytsearch1', 'noplaylist': True}
        try:
            with YoutubeDL(opts) as ydl:
                ydl.download([url])
            await message.answer_audio(types.FSInputFile('m.mp3'))
            os.remove('m.mp3')
        except:
            await message.answer("Musiqa topilmadi.")
        await msg.delete()
        return

    # Video yuklash (Instagram/TikTok/YT)
    msg = await message.answer("Yuklanmoqda... 📥")
    v_opts = {'format': 'best', 'outtmpl': 'v.mp4'}
    a_opts = {'format': 'bestaudio/best', 'outtmpl': 'a.mp3', 'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3'}]}
    
    try:
        with YoutubeDL(v_opts) as ydl:
            ydl.download([url])
        await message.answer_video(types.FSInputFile('v.mp4'), caption="Video tayyor! ✅")
        os.remove('v.mp4')
        
        # Avtomatik musiqasini ham yuboramiz
        with YoutubeDL(a_opts) as ydl:
            ydl.download([url])
        await message.answer_audio(types.FSInputFile('a.mp3'), caption="Musiqasi! 🎵")
        os.remove('a.mp3')
    except Exception as e:
        await message.answer(f"Xatolik yuz berdi. Linkni tekshiring.")
    await msg.delete()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())



