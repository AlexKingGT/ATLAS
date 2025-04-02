#@rootaccess2 сабайся

import logging
import asyncio
import base64
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from aiogram.utils import executor
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

TOKEN = input("Введите токен бота: ")
ADMIN_ID = int(input("Введите ID администратора: "))
CHANNEL_LINK = input("Введите ссылку на канал: ")
PRICE_INFO = input("Введите прайс (через пробел или строку): ")
WELCOME_TEXT = "Добро пожаловать!"
PHOTO_ID = None

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

USER_FILE = "users.txt"
DATA_FILE = "data.txt"
PRICE_FILE = "price.txt"

logging.basicConfig(level=logging.INFO)


class AdminState(StatesGroup):
    waiting_for_photo = State()
    waiting_for_text = State()
    waiting_for_broadcast = State()
    waiting_for_username = State()
    waiting_for_check_def = State()
    waiting_for_price = State()

def add_user(username):
    with open(USER_FILE, "a", encoding="utf-8") as file:
        file.write(username + "\n")

def save_user(user_id):
    users = get_all_bot_users()
    if str(user_id) not in users:
        with open(DATA_FILE, "a", encoding="utf-8") as file:
            file.write(str(user_id) + "\n")

def get_all_users():
    try:
        with open(USER_FILE, "r", encoding="utf-8") as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return []

def get_all_bot_users():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return []

#@rootaccess2 сабайся

def get_price():
    try:
        with open(PRICE_FILE, "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "Прайс не установлен"

def save_price(new_price):
    with open(PRICE_FILE, "w", encoding="utf-8") as file:
        file.write(new_price)

def check_def(username):
    users = get_all_users()
    return username in users

keyboard = InlineKeyboardMarkup().add(
    InlineKeyboardButton("Проверить на DEF", callback_data="check_def"),
    InlineKeyboardButton("Прайс", callback_data="price"),
    InlineKeyboardButton("Вступить в канал", url=CHANNEL_LINK),
    InlineKeyboardButton("Создатель", callback_data="creator")
)

admin_keyboard = InlineKeyboardMarkup().add(
    InlineKeyboardButton("Изменить текст приветствия", callback_data="set_text"),
    InlineKeyboardButton("Изменить фото", callback_data="set_photo"),
    InlineKeyboardButton("Добавить пользователя", callback_data="add_user"),
    InlineKeyboardButton("Сделать рассылку", callback_data="broadcast"),
    InlineKeyboardButton("Изменить прайс", callback_data="set_price")
)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    save_user(message.from_user.id)
    if PHOTO_ID:
        await message.answer_photo(PHOTO_ID, caption=WELCOME_TEXT, reply_markup=keyboard)
    else:
        await message.answer(WELCOME_TEXT, reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data == "check_def")
async def ask_for_def_username(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Введите @username для проверки.")
    await AdminState.waiting_for_check_def.set()

@dp.message_handler(state=AdminState.waiting_for_check_def)
async def handle_check_def(message: types.Message, state: FSMContext):
    username = message.text.strip()
    if not username.startswith("@"):
        await message.reply("Ошибка! Введите username в формате @username")
        return
    username = username[1:]
    if check_def(username):

#@rootaccess2 сабайся

        report = f"✅ @{username} найден в базе данных."
    else:
        report = f"❌ @{username} отсутствует в базе данных."
    await message.reply(report)
    await state.finish()

@dp.callback_query_handler(lambda c: c.data == "price")
async def send_price(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    current_price = get_price()
    await bot.send_message(callback_query.from_user.id, f"📋 Прайс:\n{current_price}")

_creator_enc = b'QHJvb3RhY2Nlc3My'
CREATOR = base64.b64decode(_creator_enc).decode('utf-8')

@dp.callback_query_handler(lambda c: c.data == "creator")
async def send_creator_info(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"👤 Создатель: {CREATOR}")

@dp.message_handler(commands=["admin"])
async def admin_panel(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    await message.reply("Админ панель:", reply_markup=admin_keyboard)

@dp.callback_query_handler(lambda c: c.data == "set_text")
async def set_text(callback_query: types.CallbackQuery):
    if callback_query.from_user.id != ADMIN_ID:
        return
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Введите новый текст приветствия:")
    await AdminState.waiting_for_text.set()

@dp.message_handler(state=AdminState.waiting_for_text)
async def process_new_text(message: types.Message, state: FSMContext):
    global WELCOME_TEXT
    new_text = message.text.strip()
    WELCOME_TEXT = new_text
    await message.reply("Текст приветствия успешно обновлен!")
    await state.finish()

@dp.callback_query_handler(lambda c: c.data == "set_photo")
async def set_photo(callback_query: types.CallbackQuery):
    if callback_query.from_user.id != ADMIN_ID:
        return

#@rootaccess2 сабайся

    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Отправьте новое фото для приветствия:")
    await AdminState.waiting_for_photo.set()

@dp.message_handler(content_types=['photo'], state=AdminState.waiting_for_photo)
async def process_new_photo(message: types.Message, state: FSMContext):
    global PHOTO_ID
    PHOTO_ID = message.photo[-1].file_id
    await message.reply("Фото приветствия успешно обновлено!")
    await state.finish()

@dp.callback_query_handler(lambda c: c.data == "add_user")
async def admin_add_user(callback_query: types.CallbackQuery):
    if callback_query.from_user.id != ADMIN_ID:
        return
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Введите @username пользователя для добавления:")
    await AdminState.waiting_for_username.set()

@dp.message_handler(state=AdminState.waiting_for_username)
async def process_new_user(message: types.Message, state: FSMContext):
    username = message.text.strip()
    if not username.startswith("@"):
        await message.reply("Ошибка! Введите username в формате @username")
        return
    username = username[1:]
    add_user(username)
    await message.reply(f"Пользователь @{username} успешно добавлен в базу!")
    await state.finish()

@dp.callback_query_handler(lambda c: c.data == "broadcast")
async def broadcast(callback_query: types.CallbackQuery):
    if callback_query.from_user.id != ADMIN_ID:
        return
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Введите текст для рассылки.")
    await AdminState.waiting_for_broadcast.set()

@dp.message_handler(state=AdminState.waiting_for_broadcast)
async def send_broadcast(message: types.Message, state: FSMContext):
    text = message.text.strip()
    users = get_all_bot_users()
    failed_users = []  # Список пользователей, которым не удалось отправить сообщение

    for user in users:
        try:
            await bot.send_message(user, text)
        except Exception as e:
            logging.warning(f"Не удалось отправить сообщение пользователю {user}: {e}")
            failed_users.append(user)  # Добавляем пользователя в список неудачных

    if failed_users:
        failed_message = f"Не удалось отправить сообщение следующим пользователям: {', '.join(failed_users)}"
        await message.reply(failed_message)

    await message.reply("✅ Рассылка завершена!")
    await state.finish()

#@rootaccess2 сабайся

@dp.callback_query_handler(lambda c: c.data == "set_price")
async def set_price(callback_query: types.CallbackQuery):
    if callback_query.from_user.id != ADMIN_ID:
        return
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Введите новый прайс:")
    await AdminState.waiting_for_price.set()

@dp.message_handler(state=AdminState.waiting_for_price)
async def process_new_price(message: types.Message, state: FSMContext):
    new_price = message.text.strip()
    save_price(new_price)
    await message.reply("Прайс успешно обновлен!")
    await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

#@rootaccess2 сабайся
