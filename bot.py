import telebot
import requests
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.environ['TOKEN']
bot = telebot.TeleBot(TOKEN)

headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/x-www-form-urlencoded"
}

def get_instagram_video(insta_url):
    data = {
        "q": insta_url,
        "t": "media",
        "lang": "en"
    }
    r = requests.post("https://saveig.app/api/ajaxSearch", data=data, headers=headers)
    result = r.json()
    video_links = result.get("links", [])
    if video_links:
        return video_links[0].get("url", None)
    return None

@bot.message_handler(commands=['start'])
def welcome(msg):
    bot.reply_to(msg, (
        "👋 Salom! Men Instagram videolarini yuklaydigan botman.\n"
        "📎 Menga shunchaki video havolasini yuboring.\n"
        "📥 Men sizga yuklab olish tugmasini yuboraman."
    ))

@bot.message_handler(func=lambda msg: 'instagram.com' in msg.text)
def download(msg):
    if not any(x in msg.text for x in ['/reel/', '/p/', '/tv/']):
        bot.send_message(msg.chat.id, "Faqat video (reel/post/igtv) havolasini yuboring.")
        return
    try:
        video_url = get_instagram_video(msg.text)
        if video_url:
            markup = InlineKeyboardMarkup()
            btn = InlineKeyboardButton(text="📥 Yuklab olish", url=video_url)
            markup.add(btn)
            bot.send_message(msg.chat.id, "Video tayyor:", reply_markup=markup)
        else:
            bot.send_message(msg.chat.id, "❌ Video topilmadi yoki yuklab bo‘lmadi.")
    except Exception as e:
        print(e)
        bot.send_message(msg.chat.id, "❌ Xatolik yuz berdi. Havolani tekshiring yoki keyinroq urinib ko‘ring.")

bot.polling()
