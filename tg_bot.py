import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply(
        "Assalomu alaykum!\nBotga shahar manzilini kiriting va u sizga ob-havo ma'lumotini chiqarib beradi!"
    )


@dp.message_handler(commands=['help', 'yordam'])
async def send_welcome(message: types.Message):
    await message.reply(
        "Assalomu alaykum!\nBotning ishlashida muammo bo'layotgan bo'lsa @shavkat_mustafoyev akkauntiga murojaat qiling."
    )


@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Quyoshli \U00002600",
        "Clouds": "Bulutli \U00002601",
        "Rain": "Yomg'irli \U00002614",
        "Drizzle": "Yomg'ir yog'ishi mumkin \U00002614",
        "Thunderstorm": "Momoqaldiroq \U000026A1",
        "Snow": "Qor \U0001F328",
        "Mist": "Tuman \U0001F328"
    }

    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Ob-havo qandayligini bilish uchun derazadan qarang :)"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(
            data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(
            data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
                data["sys"]["sunrise"])

        await message.reply(
            f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%H')}***\n"
            f"Shahardagi ob-havo: {city}\nHarorat: {cur_weather}℃  {wd}\nNamlik: {humidity}%\nBosim: {pressure}\nShamol: {wind} m/s\n"
            f"Quyosh chiqishi: {sunrise_timestamp}\nQuyosh botishi: {sunset_timestamp}\nKunning davomiyligi {length_of_the_day}\n"
            f"***Kuningiz xayrli o'tsin!***")

    except:
        await message.reply(" \U00002628 Shahar nomini tekshiring \U00002628 ")


if __name__ == "__main__":
    executor.start_polling(dp)
