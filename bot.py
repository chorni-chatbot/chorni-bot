import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from yt_dlp import YoutubeDL

API_TOKEN = '8362871398:AAERtQR_OVJjGddYxHiRIy6-BcUs6t-MEeA'
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Vaqtincha linklarni saqlash uchun
user_data = {}

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Salom! Link yuboring yoki qo'shiq nomini yozing😎")

@dp.message(F.text)
async def handle_message(message: types.Message):
    url = message.text
    user_id = message.from_user.id
    
    if "http" in url:
        user_data[user_id] = url
        msg = await message.answer("Video yuklanmoqda... 📥")
        opts = {'format': 'best', 'outtmpl': f'v_{user_id}.mp4', 'noplaylist': True}
        try:
            with YoutubeDL(opts) as ydl:
                ydl.download([url])
            kb = InlineKeyboardBuilder()
            kb.row(types.InlineKeyboardButton(text="🎵 Musiqasini yuklash", callback_data="get_mp3"))
            await message.answer_video(types.FSInputFile(f'v_{user_id}.mp4'), caption="Tayyor! ✅", reply_markup=kb.as_markup())
            os.remove(f'v_{user_id}.mp4')
        except:
            await message.answer("Xatolik! Linkni tekshiring.")
        await msg.delete()
    else:
        # MUSIQA QIDIRISH (Ism orqali)
        msg = await message.answer("Qidirilmoqda... 🔍")
        search_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'm_{user_id}.mp3',
            'default_search': 'ytsearch1',
            'noplaylist': True,
            'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}]
        }
        try:
            with YoutubeDL(search_opts) as ydl:
                ydl.download([f"ytsearch1:{url}"])
            await message.answer_audio(types.FSInputFile(f'm_{user_id}.mp3'), caption=f"Topildi: {url}")
            os.remove(f'm_{user_id}.mp3')
        except:
            await message.answer("Musiqa topilmadi. Ismni to'g'ri yozganingizga ishonch hosil qiling.")
        await msg.delete()

@dp.callback_query(F.data == "get_mp3")
async def extract_mp3(call: types.CallbackQuery):
    url = user_data.get(call.from_user.id)
    if not url: return await call.answer("Xatolik!")
    
    await call.answer("Musiqa ajratilmoqda...")
    opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'a_{call.from_user.id}.mp3',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}]
    }
    try:
        with YoutubeDL(opts) as ydl:
            ydl.download([url])
        await call.message.answer_audio(types.FSInputFile(f'a_{call.from_user.id}.mp3'))
        os.remove(f'a_{call.from_user.id}.mp3')
    except:
        await call.message.answer("FFmpeg xatoligi yoki linkda musiqa yo'q.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


