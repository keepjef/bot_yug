from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message, FSInputFile, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
import asyncio
API_TOKEN = '7993581763:AAGP25aKKc6HGBfKQVUntF_iYZhS5r9wA1c'
bot = Bot(token = API_TOKEN)
dp = Dispatcher()
router = Router()
photo = FSInputFile('kolokol.jpg')
buttons = [InlineKeyboardButton(text='Create task', callback_data="button_click"),
            InlineKeyboardButton(text='Change task', callback_data="button_click2"),
            InlineKeyboardButton(text='Delete task', callback_data="button_click3")
          ]
keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])

@router.message(Command("start"))
async def start_sendwelcome(message: Message):
    await message.answer('Здравствуйте, вас приветствует бот-напоминалка! Чтобы узнать подробнее, нажмите команду /help. Выберите опцию ниже', reply_markup=keyboard)

@router.message(Command("help"))
async def start_command_handler(message: Message):
    await message.answer('Бот-напоминалка — это виртуальный помощник, который помогает пользователям не забывать о важных делах и событиях.🎀 \nОн может отправлять уведомления, устанавливать напоминания и следить за их выполнением. \n Бот-напоминалка облегчает жизнь пользователей, помогая им быть более организованными и эффективными.☭')


async  def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())