import requests
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, executor, types
import time, logging


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
    
  
    usd_rate = soup.find_all('td', class_='exrate')
    eur_rate = soup.find_all('td', class_='exrate')
    rub_rate = soup.find_all('td', class_='exrate')


    for rub, usd, euro in zip(rub_rate, eur_rate, usd_rate ):
        await message.answer(f"\n Доллар {usd} \n Евро {euro} \n Рубль {rub}")
    



executor.start_polling(dp)






    

