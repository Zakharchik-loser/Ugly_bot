from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

async def start_command(message: types.Message):
    subjects = ["algebra", "geometry", "physics", "chemistry", "history"]
    keyboard = InlineKeyboardMarkup(row_width=2,inline_keyboard=[[]])

    buttons = [InlineKeyboardButton(text=subject.capitalize(), callback_data=f"subject_{subject}") for subject in subjects]
    keyboard.inline_keyboard = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]

    await message.answer("Виберіть предмет для перевірки знань:", reply_markup=keyboard)

async def help_command(message: types.Message):
    help_text = (
        "Я бот для перевірки знань. Ось доступні команди:\n"
        "/start - Почати роботу\n"
        "/choice - Вибрати предмет\n"
        "/support - Отримати підтримку"
    )
    await message.answer(help_text)

async def choice_command(message: types.Message):
    await start_command(message)

def register_commands(dp: Dispatcher):
    dp.message.register(start_command, Command(commands=["start"]))
    dp.message.register(help_command, Command(commands=["help"]))
    dp.message.register(choice_command, Command(commands=["choice"]))
