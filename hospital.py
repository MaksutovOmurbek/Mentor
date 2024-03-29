from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sqlite3
import logging
import random
import string

token = "7106836516:AAHdrX2n783ZcMNhVRaKnEEkt0uYCIaVL64"

storage = MemoryStorage()

bot = Bot(token)
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

conn = sqlite3.connect('bot_bot.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
user_id INTEGER PRIMARY KEY,
full_name VARCHAR (100) NOT NULL,
age INTEGER NOT NULL,
email TEXT DEFAULT NULL,
phone_number TEXT,
time TEXT DEFAULT NULL,
doctor TEXT DEFAULT NULL,
ticket_code TEXT DEFAULT NULL
)""")
conn.commit()

start_buttons = [
    types.KeyboardButton('/doctor'),
    types.KeyboardButton('Register'),
    types.KeyboardButton('About-us'),
]
start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_buttons)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer(f"Здраствуйте, {message.from_user.full_name}!", reply_markup=start_keyboard)


@dp.message_handler(text='About-us')
async def about_us(message: types.Message):
    await message.answer('Это больница, где работают квалифицированные доктора. '
                         'Чтобы записаться, нажмите /register.')


@dp.message_handler(text='/doctor')
async def doctor_info(message: types.Message):
    doctors_info = [
        {'name': 'Роберт', 'photo': 'https://cosmedica.com/wp-content/uploads/2023/10/%D0%94%D0%BE%D0%BA%D1%82%D0%BE%D1%80-%D0%BF%D0%BE-%D0%BF%D0%B5%D1%80%D0%B5%D1%81%D0%B0%D0%B4%D0%BA%D0%B5-%D0%B2%D0%BE%D0%BB%D0%BE%D1%81-Levent-Acar-2.png', 'description': ' опытный и заботливый медицинский специалист ', 'address': 'Ош,  Мырзалы Аматова 1б ', 'cabinet': 'Кабинет 53'},
        {'name': 'Андрей', 'photo': 'https://lahtaclinic.ru/wp-content/uploads/2023/02/smiling-doctor-with-strethoscope-isolated-grey.jpeg', 'description': 'ценный член медицинской команды, способствующий эффективной работе отделения/клиники/госпиталя', 'address': 'Ош, Навои', 'cabinet': 'Кабинет 131'},
        {'name': 'Дима', 'photo': 'https://hron.ru/images/news/05122019/_5de8f6bc774fc6.81035456.jpg', 'description': 'уважаемый специалист в медицинской области с множеством научных публикаций и исследований.', 'address': 'Ош, Курманжан Датка', 'cabinet': 'Кабинет 98'}
    ]

    for doctor in doctors_info:
        await message.answer(f"Имя: {doctor['name']}\nОписание: {doctor['description']}\nАдрес: {doctor['address']}\nКабинет: {doctor['cabinet']}")
        await message.answer_photo(doctor['photo'])



class HospitalState(StatesGroup):
    get_full_name = State()
    get_age = State()
    get_email = State()
    get_phone_number = State()
    get_time = State()


@dp.message_handler(commands='register')
async def start_resume(message: types.Message):
    await HospitalState.get_full_name.set()
    await message.answer("Введите ваше полное имя:")


@dp.message_handler(state=HospitalState.get_full_name)
async def full_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['full_name'] = message.text
    await HospitalState.next()
    await message.answer("Введите ваш возраст:")


@dp.message_handler(state=HospitalState.get_age)
async def age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:

            await HospitalState.next()
            await message.answer("Введите ваш email:")
        


@dp.message_handler(state=HospitalState.get_email)
async def email(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['email'] = message.text
    await HospitalState.next()
    await message.answer("Введите ваш номер телефона:")


@dp.message_handler(state=HospitalState.get_phone_number)
async def phone_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_number'] = message.text
    await HospitalState.next()
    await message.answer("Во сколько вам удобно записаться?")


@dp.message_handler(state=HospitalState.get_time)
async def time(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['time'] = message.text

    
    ticket_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    data['ticket_code'] = ticket_code

    cursor.execute("""
    INSERT OR REPLACE INTO users (user_id, full_name, age,  email, phone_number, time, doctor, ticket_code)
    VALUES (?, ?, ?, ?, ? , ?, ?, ?)""", (message.from_user.id, data['full_name'], data['age'], data['email'], data['phone_number'], data['time'], data['doctor'], data['ticket_code']))
    conn.commit()

    await state.finish()
    await message.answer(f"Мы сохранили ваши данные. Ваш код талона: {ticket_code}\nИнформация о записи:\n"
                         f"Время: {data['time']}\nИмя доктора: {data['doctor']}\nАдрес: ...\nКабинет: ...")



executor.start_polling(dp)



