import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from yt_dlp import YoutubeDL

API_TOKEN = '8362871398:AAERtQR_OVJjGddYxHiRIy6-BcUs6t-MEeA'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Video tagida chiqadigan tugma
def get_audio_button(url):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="🎵 Qo'shiqni yuklab olish", 
        callback_data=f"audio_{url[:40]}" # Link uzunligini cheklaymiz
    ))
    return builder.as_markup()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Salom! Instagram link yuboring, men videoni va musiqasini topib beraman! 🚀")

@dp.message(F.text.contains("instagram.com") | F.text.contains("tiktok.com") | F.text.contains("youtube.com"))
async def handle_video(message: types.Message):
    url = message.text
    msg = await message.answer("Video yuklanmoqda... 📥")
    
    v_opts = {'format': 'best', 'outtmpl': 'v.mp4', 'noplaylist': True}
    
    try:
        with YoutubeDL(v_opts) as ydl:
            ydl.download([url])
        
        video = types.FSInputFile("v.mp4")
        # Video yuboriladi va tagida tugma chiqadi
        await message.answer_video(video, caption="Tayyor! ✅", reply_markup=get_audio_button(url))
        os.remove("v.mp4")
        await msg.delete()
    except Exception as e:
        await message.answer("Xatolik! Linkni tekshiring.")

# Tugma bosilganda musiqani ajratib olish
@dp.callback_query(F.data.startswith("audio_"))
async def process_audio(callback: types.CallbackQuery):
    # Bu yerda aslida linkni saqlash kerak, hozircha oddiyroq usul:
    await callback.answer("Musiqa ajratib olinmoqda, kuting...")
    await callback.message.answer("🎵 Musiqa tayyorlanmoqda...")
    
    # Callback data-dan linkni tiklash qiyinligi uchun foydalanuvchi xabaridagi linkni olamiz
    url = callback.message.caption_entities # yoki caption-dan qidirish
    # Soddalik uchun qayta yuklash:
    a_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'm.mp3',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
    }
    
    # Bu qismda original url-ni callback-dan olishni sozlash kerak
    # Hozircha foydalanuvchi link yuborganda bot hammasini birdan yuborgani ma'qul (shazam kabi)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
