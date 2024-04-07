import requests
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, executor, types
import time, logging
from datetime import datetime
import asyncio


Token= '7106836516:AAHdrX2n783ZcMNhVRaKnEEkt0uYCIaVL64'

bot = Bot(Token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer("Валюта")

    url = 'https://www.nbkr.kg/index.jsp?lang=RUS'
    response = requests.get(url)
    soup  = BeautifulSoup(response.text, 'lxml')
    time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    usd_rate = soup.find_all('td', class_='exrate')
    eur_rate = soup.find_all('td', class_='exrate')
    rub_rate = soup.find_all('td', class_='exrate')
    time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


    for rub, usd, euro in zip(rub_rate, eur_rate, usd_rate ):
        await message.answer(f" Валюта {time}:\nКурс USD: {usd[0].text}\nКурс EUR: {euro[2].text}\nКурс RUB: {rub[4].text}\n")
    

async def send_send(message):
    while True:
        await message.answer(message)
        await asyncio.sleep(60)  


async def on_startup(dispatcher):
    pass


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer(message)
    asyncio.create_task(send_send(message))


executor.start_polling(dp)






    

