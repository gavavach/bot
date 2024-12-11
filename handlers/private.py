from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command, or_f
from keybords.for_navigate import keyboard

private_router = Router()


@private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.reply('Привiт', reply_markup=keyboard)


@private_router.message((F.text == 'про бота'))
async def about(message: types.Message):
    await message.answer('Цей бот був створений для облегчення життя')


@private_router.message((F.text.lower() == 'привiт') | (F.text.lower() == 'здоровеньки були'))
async def options(message: types.Message):
    await message.answer('Привiт')


# @private_router.message()
# async def echo(message: types.Message):
#     await message.answer(message.text)