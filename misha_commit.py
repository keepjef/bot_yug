import asyncio
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
API_TOKEN = "7987943271:AAETUsmA52NKgg2_9X511ovuDtB8k4VwIbY"
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()
button1=[InlineKeyboardButton(text="Список_задач",callback_data="button_click"),
InlineKeyboardButton(text="Измененить_задачу",callback_data="button_click2"),]
keyboard=InlineKeyboardMarkup(inline_keyboard=[button1])
storage=MemoryStorage()
dp=Dispatcher(storage=storage)
class ReminderStates(StatesGroup):
    id=State()
    tasks=State()
tasks={
       1:{
            "id": 1,
            "task": "aaaa",
            "date": "aaaa",

        },
        2:{
            "id": 2,
            "task": "aaa",
            "date": "bbb0",

        },
        3:{
            "id": 3,
            "task": "ggg",
            "date": "ddd",

        },
        4:{
            "id": 4,
            "task": "ffff",
            "date": "ccc",

        },
        5:{
            "id": 5,
            "task": "qqq",
            "date": "rrr",

        }

    }




'''@router.callback_query(lambda callback: callback.data=="button_click")
async def button (callback_query: CallbackQuery):
 await callback_query.message.answer("Привет")
 for i in tasks:
        for key, value in i.items():
            await callback_query.message.answer(str(value))'''

def create_buttons_task():
    global tasks
    buttons = []
    for task in tasks.keys():
        button = KeyboardButton(text=str(task))
        buttons.append(button)
    return ReplyKeyboardMarkup(keyboard=[buttons])
def info_buttons(id):
    global tasks
    stroka=""
    for key, value in tasks[id].items():
      stroka+="{0}:{1}".format(key, value)
    return stroka
def del_buttons(id):
    global tasks
    del tasks[id]


@dp.message(Command("start"))
async def send_hello(message: Message, state: FSMContext):
    keyboard = create_buttons_task()
    await message.answer("Нажмите на кнопку",reply_markup=keyboard)
    await state.set_state(ReminderStates.id)

@dp.message(ReminderStates.id)
async def process_id(message: Message, state: FSMContext):
    id = int(message.text)
    await state.update_data(id=id)
    await state.set_state(ReminderStates.tasks)
    info_task=info_buttons(id)
    #info_task=del_buttons(id)

    await message.answer(info_task)


@dp.message(ReminderStates.tasks)
async def process_id(message: Message, state: FSMContext):
    data = await state.get_data()
    info = info_buttons(data["id"])
    await message.answer(str(info))

async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

