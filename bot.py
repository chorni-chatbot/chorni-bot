import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from yt_dlp import YoutubeDL

# BotFather'dan olgan tokeningiz
API_TOKEN = '8362871398:AAERtQR_OVJjGddYxHiRIy6-BcUs6t-MEeA'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Menyu tugmalari
def main_menu():
    kb = [
        [types.KeyboardButton(text="Musiqa qidirish 🔍")],
        [types.KeyboardButton(text="Linkdan yuklash 📥"), types.KeyboardButton(text="Yordam ❓")]
    ]
    return types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        "Salom! Men aqlli botman. Instagram linkini tashlasangiz, videoni ham, undagi musiqani ham topib beraman!",
        reply_markup=main_menu()
    )

@dp.message()
async def handle_everything(message: types.Message):
    if not message.text: return
    url = message.text
    
    # Agar bu link bo'lsa
    if "instagram.com" in url or "tiktok.com" in url or "youtube.com" in url or "youtu.be" in url:
        msg = await message.answer("Video va musiqa ajratib olinmoqda, kuting...")
        
        # 1. Videoni yuklash sozlamasi
        v_opts = {'format': 'best', 'outtmpl': 'video.mp4'}
        # 2. Musiqani ajratib olish sozlamasi
        a_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'music.mp3',
            'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
        }

        try:
            # Videoni yuklash va yuborish
            with YoutubeDL(v_opts) as ydl:
                ydl.download([url])
            await message.answer_video(types.FSInputFile("video.mp4"), caption="Mana video! 🎥")
            
            # Musiqani ajratib olish va yuborish
            with YoutubeDL(a_opts) as ydl:
                ydl.download([url])
            await message.answer_audio(types.FSInputFile("music.mp3"), caption="Mana videodagi musiqa! 🎵")
            
            # Fayllarni tozalash
            if os.path.exists("video.mp4"): os.remove("video.mp4")
            if os.path.exists("music.mp3"): os.remove("music.mp3")
            
        except Exception as e:
            await message.answer("Xatolik: Linkni tekshiring yoki botni qayta ishga tushiring.")
        await msg.delete()
    
    # Agar shunchaki matn bo'lsa (Musiqa qidirish)
    else:
        msg = await message.answer("Musiqa qidirilmoqda...")
        search_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'search_music.mp3',
            'default_search': 'ytsearch1',
            'noplaylist': True,
        }
        try:
            with YoutubeDL(search_opts) as ydl:
                ydl.download([url])
            await message.answer_audio(types.FSInputFile("search_music.mp3"), caption=f"Topildi: {url} ✅")
            os.remove("search_music.mp3")
        except:
            await message.answer("Hech narsa topilmadi 😔")
        await msg.delete()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

