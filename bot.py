import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from yt_dlp import YoutubeDL

# Botingiz tokeni
API_TOKEN = '8362871398:AAERtQR_OVJjGddYxHiRIy6-BcUs6t-MEeA'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Vaqtincha linklarni saqlash
user_temp = {}

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Salom! Link yuboring yoki qo'shiq ismini yozing. 🎵📸")

@dp.message(F.text)
async def main_handler(message: types.Message):
    url = message.text
    user_id = message.from_user.id

    # 1. LINK YUBORILSA
    if url.startswith("http"):
        user_temp[user_id] = url
        msg = await message.answer("Video yuklanmoqda... 📥")
        
        ydl_opts = {
            'format': 'best',
            'outtmpl': f'v_{user_id}.mp4',
            'quiet': True,
            'no_warnings': True
        }
        
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            kb = InlineKeyboardBuilder()
            kb.row(types.InlineKeyboardButton(text="🎵 Musiqasini yuklash", callback_data="audio_only"))
            
            video = types.FSInputFile(f'v_{user_id}.mp4')
            await message.answer_video(video, caption="Tayyor! ✅", reply_markup=kb.as_markup())
            os.remove(f'v_{user_id}.mp4')
        except Exception:
            await message.answer("Xatolik! Instagram linki noto'g'ri yoki video yopiq profilda. ❌")
        await msg.delete()

    # 2. QO'SHIQ ISMI YOZILSA
    else:
        msg = await message.answer("Qidirilmoqda... 🔍")
        search_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'm_{user_id}.%(ext)s',
            'default_search': 'ytsearch1',
            'noplaylist': True,
            'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}]
        }
        try:
            with YoutubeDL(search_opts) as ydl:
                ydl.download([url])
            
            # Faylni topish (ext har xil bo'lishi mumkin)
            filename = f"m_{user_id}.mp3"
            audio = types.FSInputFile(filename)
            await message.answer_audio(audio, caption=f"Topildi: {url}")
            os.remove(filename)
        except Exception:
            await message.answer("Musiqa topilmadi. 😔 (Serverda FFmpeg o'rnatilishi kerak)")
        await msg.delete()

@dp.callback_query(F.data == "audio_only")
async def send_audio(call: types.CallbackQuery):
    url = user_temp.get(call.from_user.id)
    if not url: return await call.answer("Link topilmadi!")

    await call.answer("Musiqa tayyorlanmoqda...")
    status = await call.message.answer("🎵 Musiqa ajratilmoqda...")
    
    a_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'a_{call.from_user.id}.%(ext)s',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}]
    }
    
    try:
        with YoutubeDL(a_opts) as ydl:
            ydl.download([url])
        audio = types.FSInputFile(f'a_{call.from_user.id}.mp3')
        await call.message.answer_audio(audio)
        os.remove(f'a_{call.from_user.id}.mp3')
    except:
        await call.message.answer("Xatolik! Server sozlamalarini tekshiring.")
    await status.delete()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


