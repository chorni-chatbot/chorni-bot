import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from yt_dlp import YoutubeDL

# Bot tokeningiz
API_TOKEN = '8362871398:AAERtQR_OVJjGddYxHiRIy6-BcUs6t-MEeA'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Video tagidagi tugma funksiyasi
def get_audio_kb(url):
    builder = InlineKeyboardBuilder()
    # Callback_data cheklovi sababli urlni qisqartiramiz yoki saqlaymiz
    builder.row(types.InlineKeyboardButton(
        text="🎵 Qo'shiqni yuklab olish", 
        callback_data=f"mp3_download") 
    )
    return builder.as_markup()

# Global lug'at - vaqtincha linklarni saqlash uchun
user_links = {}

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Salom! Menga Instagram yoki TikTok linkini yuboring. Men videoni va undagi musiqani topib beraman! ✨")

@dp.message(F.text.contains("http"))
async def handle_video(message: types.Message):
    url = message.text
    user_links[message.from_user.id] = url # Linkni eslab qolamiz
    
    msg = await message.answer("Video tayyorlanmoqda... 📥")
    
    v_opts = {
        'format': 'best',
        'outtmpl': f'v_{message.from_user.id}.mp4',
        'noplaylist': True,
    }
    
    try:
        with YoutubeDL(v_opts) as ydl:
            ydl.download([url])
        
        video_file = types.FSInputFile(f'v_{message.from_user.id}.mp4')
        await message.answer_video(
            video_file, 
            caption="Tayyor! ✅\n\n@chornichatuzbot orqali yuklab olindi",
            reply_markup=get_audio_kb(url)
        )
        os.remove(f'v_{message.from_user.id}.mp4')
        await msg.delete()
    except Exception as e:
        await message.answer("Xatolik: Link noto'g'ri yoki video yopiq profilda.")
        await msg.delete()

# Tugma bosilganda musiqani ajratib yuborish
@dp.callback_query(F.data == "mp3_download")
async def send_audio(callback: types.CallbackQuery):
    url = user_links.get(callback.from_user.id)
    
    if not url:
        return await callback.answer("Xatolik: Link topilmadi. Qaytadan link yuboring.", show_alert=True)
    
    await callback.answer("Musiqa ajratib olinmoqda... 🎧")
    status_msg = await callback.message.answer("🎵 Musiqa yuklanmoqda...")

    a_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'm_{callback.from_user.id}.mp3',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with YoutubeDL(a_opts) as ydl:
            ydl.download([url])
        
        audio_file = types.FSInputFile(f'm_{callback.from_user.id}.mp3')
        await callback.message.answer_audio(audio_file, caption="Mana videodagi musiqa! 🎶")
        os.remove(f'm_{callback.from_user.id}.mp3')
        await status_msg.delete()
    except Exception as e:
        await callback.message.answer("Musiqani yuklashda xatolik yuz berdi.")
        await status_msg.delete()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

