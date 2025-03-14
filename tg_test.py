import asyncio
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

# Configure logging
logging.basicConfig(level=logging.INFO)

# Bot token from BotFather
BOT_TOKEN = "7600020466:AAEpvQn-bo8E2LalBLDqG6sXwzaX6xAmHVs"

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Define states
class ReminderStates(StatesGroup):
    date_day = State()
    date_month = State()
    date_year = State()
    time_hour = State()
    time_minute = State()
    text = State()

async def send_reminder(bot: Bot, chat_id: int, text: str, delay: float):
    try:
        await asyncio.sleep(delay)
        await bot.send_message(chat_id, f"Напоминание: {text}")
    except Exception as error:
        logging.error(f"Ошибка: {error}")
def create_days_keyboard():
    buttons = [KeyboardButton(text=str(day)) for day in range(1, 32)]
    return ReplyKeyboardMarkup(keyboard=[buttons[i:i+6] for i in range(1, 32, 6)])
    # return ReplyKeyboardMarkup(keyboard=[buttons[i:i+7] for i in range(0, 31, 7)], resize_keyboard=True)

def create_months_keyboard():
    buttons = [KeyboardButton(text=str(month)) for month in range(1, 13)]
    return ReplyKeyboardMarkup(keyboard=[buttons[i:i+4] for i in range(0, 12, 4)], resize_keyboard=True)

def create_years_keyboard():
    current_year = datetime.now().year
    buttons = [
        KeyboardButton(text=str(current_year)) for current_year in range(current_year, current_year + 10)
    ]
    return ReplyKeyboardMarkup(keyboard=[buttons], resize_keyboard=True)

def create_hours_keyboard():
    buttons = [KeyboardButton(text=f"{hour:02d}") for hour in range(0, 24)]
    return ReplyKeyboardMarkup(keyboard=[buttons[i:i+6] for i in range(0, 24, 6)], resize_keyboard=True)

def create_minutes_keyboard():
    buttons = [
        KeyboardButton(text="00"),
        KeyboardButton(text="15"),
        KeyboardButton(text="30"),
        KeyboardButton(text="45"),
        KeyboardButton(text="50"),
        KeyboardButton(text="55")

    ]
    return ReplyKeyboardMarkup(keyboard=[buttons], resize_keyboard=True)
@dp.message(Command("start", "setreminder"))
async def cmd_start(message: Message, state: FSMContext):
    await message.answer("Let's create a reminder! Please select the year:", reply_markup=create_years_keyboard())
    await state.set_state(ReminderStates.date_year)


@dp.message(Command("start", "setreminder"))
async def cmd_start(message: Message, state: FSMContext):
    await message.answer("Let's create a reminder! Please select the year:", reply_markup=create_years_keyboard())
    await state.set_state(ReminderStates.date_year)

@dp.message(ReminderStates.date_year)
async def process_year(message: Message, state: FSMContext):
    try:
        year = int(message.text)
        if 2024 <= year <= 2036:
            await state.update_data(year=year)
            await message.answer("Год выбран. Выберите месяц.", reply_markup=create_months_keyboard())
            await state.set_state(ReminderStates.date_month)
        else:
            await message.answer("Введите год с 2025 по 2035. Попробуйте еще раз!")
    except ValueError:
        await message.answer("Ошибка, некоректно введен год.")

@dp.message(ReminderStates.date_month)
async def process_month(message: Message, state: FSMContext):
    try:
        month = int(message.text)

        if 1 <= month <= 12:
            await state.update_data(month=month)
            await message.answer("Месяц выбран. Выберите день.", reply_markup=create_days_keyboard())
            await state.set_state(ReminderStates.date_day)
        else:
            await message.answer("Введите месяц с 1 по 12. Попробуйте еще раз!")
    except ValueError:
        await message.answer("Ошибка, некоректно введен месяц.")


@dp.message(ReminderStates.date_day)
async def process_day(message: Message, state: FSMContext):
    try:
        day = int(message.text)

        if 1 <= day <= 31:
            await state.update_data(day=day)
            await message.answer("День выбран. Выберите час.", reply_markup=create_hours_keyboard())
            await state.set_state(ReminderStates.time_hour)
        else:
            await message.answer("Введите день с 1 до 31. Попробуйте еще раз!")
    except ValueError:
        await message.answer("Ошибка, некоректно введен день.")

    @dp.message(ReminderStates.time_hour)
    async def process_hours(message: Message, state: FSMContext):
        try:
            hours = int(message.text)

            if 0 <= hours <= 23:
                await state.update_data(hours=hours)
                await message.answer("Час выбран. Выберите минуты.", reply_markup=create_minutes_keyboard())
                await state.set_state(ReminderStates.time_minute)
            else:
                await message.answer("Введите часы с 0 до 23. Попробуйте еще раз!")
        except ValueError:
            await message.answer("Ошибка, некоректно введен час. Попробуйте  еще раз!")


@dp.message(ReminderStates.time_minute)
async def process_minutes(message: Message, state: FSMContext):
    try:
        minutes = int(message.text)

        if 00 <= minutes <= 59:
            user_data = await state.get_data()
            current_datetime = user_data.get('datetime')
            text = message.text
            now = datetime.now()

            delay = (current_datetime - now).total_seconds()
            if current_datetime <= now:
                await message.answer("Время в прошлом. Начните сначала.")
                await state.clear()
                return
            await state.update_data(minutes=minutes)
            await message.answer("Отлично! Время выбрано, теперь напишите текст.", reply_markup=types.ReplyKeyboardRemove())
            await state.set_state(ReminderStates.text)
        else:
            await message.answer("Введите минуты с 0 до 59. Попробуйте еще раз!")
    except ValueError:
        await message.answer("Ошибка, некоректно введен месяц.")

@dp.message(ReminderStates.text)
async def process_text(message: Message, state: FSMContext):
            user_data = await state.get_data()
            current_datetime = user_data.get('datetime')
            text = message.text
            now = datetime.now()

            delay = (current_datetime - now).total_seconds()
            if delay <= 0:
                await message.answer("Напоминание в прошлом. Начните сначалa")
                await state.clear()
                return

            asyncio.create_task(send_reminder(bot, message.chat.id, text, delay))
            await message.answer(
                f"Напоминание установлено на: {current_datetime.strftime('%d.%m.%Y %H:%M')}!\n"
                f"Текст: {text}"
                )
            await state.clear()
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())