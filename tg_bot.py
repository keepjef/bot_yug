import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
API_TOKEN = "6886028658:AAGvrrTKKMjzPhV0J3sdzEwleV8bOMGGS_8"
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Создаем клавиатуры
def start_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text='Показать кнопки'))
    return builder.as_markup(resize_keyboard=True)

def main_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        "Кнопка 1",
        "Кнопка 2",
        "Кнопка 3",
        "Кнопка 4",
        "Кнопка 5"
    ]
    builder = ReplyKeyboardBuilder()
    for button in buttons:
        builder.add(types.KeyboardButton(text=button))
    builder.adjust(2, 2, 1)  # Распределение кнопок по рядам
    return builder.as_markup(resize_keyboard=True)

# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Нажми кнопку ниже, чтобы увидеть больше кнопок:",
        reply_markup=start_keyboard()
    )

# Обработчик кнопки "Показать кнопки"
@dp.message(F.text == 'Показать кнопки')
async def show_buttons(message: types.Message):
    await message.answer(
        "Вот дополнительные кнопки:",
        reply_markup=main_keyboard()
    )

# Обработчики для дополнительных кнопок (пример для первой кнопки)
@dp.message(F.text == 'Кнопка 1')
async def button1_handler(message: types.Message):
    await message.answer("Вы нажали Кнопку 1!")

# Запуск бота
if __name__ == '__main__':
    dp.run_polling(bot)