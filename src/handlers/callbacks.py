from aiogram import Dispatcher, types
from aiogram.types import CallbackQuery
from src.utils.questions import questions, answers, show_levels
from src.utils.timer import display_timer, stop_timer
import logging

logging.basicConfig(level=logging.INFO)
user_states = {}

async def handle_our_subject(callback_query: CallbackQuery):
    subject = callback_query.data.split("_")[1]
    user_id = callback_query.from_user.id
    user_states[user_id] = {'subject': subject, 'level': None, 'question_index': 0, 'last_question_id': None, 'timer_message_id': None, 'time_expired': False}
    logging.info(f"user_states[{user_id}] ініціалізовано з предметом {subject}")
    await callback_query.message.answer(f"Ви обрали {subject.capitalize()}")
    await show_levels(callback_query.message, subject)
    await callback_query.answer()

async def handle_level(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    level = callback_query.data.split("_")[1]

    if user_id not in user_states:
        await callback_query.message.answer("Будь ласка, спочатку оберіть предмет.")
        return

    subject = user_states[user_id]['subject']
    user_states[user_id]['level'] = level
    user_states[user_id]['question_index'] = 0
    user_states[user_id]['last_question_id'] = None
    user_states[user_id]['timer_message_id'] = None
    user_states[user_id]['time_expired'] = False
    logging.info(f"user_states[{user_id}] оновлено з рівнем {level} та предметом {subject}")

    await send_question(callback_query.message, user_id)

async def send_question(message: types.Message, user_id: int):
    subject = user_states[user_id]['subject']
    level = user_states[user_id]['level']
    question_index = user_states[user_id]['question_index']

    question_key = f"{subject}_{level}"
    questions_list = questions.get(question_key, [])

    if question_index < len(questions_list):
        question = questions_list[question_index]
        logging.info(f"Відправляється питання {question_index + 1}: {question} користувачу {user_id}")
        sent_message = await message.answer(f"Питання {question_index + 1}: {question}")
        user_states[user_id]['last_question_id'] = sent_message.message_id
        logging.info(f"Останній ID питання для користувача {user_id}: {sent_message.message_id}")
        timer_message = await message.answer("Таймер: 15 секунд")
        user_states[user_id]['timer_message_id'] = timer_message.message_id
        await display_timer(timer_message, 15, user_id, user_states)
    else:
        await message.answer("Всі питання завершені. Вітаємо!")

async def message_handler(message: types.Message):
    user_id = message.from_user.id

    logging.info(f"Отримано повідомлення від користувача: {user_id} з текстом: {message.text}")

    if user_id in user_states:
        logging.info(f"user_states[{user_id}]: {user_states[user_id]}")

    if message.text:
        logging.info(f"Повідомлення є відповіддю на: {message.text}")
        user_answer = message.text.strip().lower()
        question_index = user_states[user_id]['question_index']
        subject = user_states[user_id]['subject']
        level = user_states[user_id]['level']
        question_key = f"{subject}_{level}"
        answers_list = answers.get(question_key, [])

        if user_states[user_id]['time_expired']:
            await message.answer("Час вийшов! Ви не можете більше відповідати на це питання.")
            return

        if question_index < len(answers_list):
            correct_answer = answers_list[question_index].strip().lower()
            logging.info(f"Правильна відповідь: {correct_answer}, Відповідь користувача: {user_answer}")

            if 'timer_message_id' in user_states[user_id] and user_states[user_id]['timer_message_id']:
                await stop_timer(message, user_states[user_id]['timer_message_id'])

            if user_answer == correct_answer:
                await message.answer("Ваша відповідь правильна! Переходимо до наступного питання.")
                user_states[user_id]['question_index'] += 1
                await send_question(message, user_id)
            else:
                await message.answer("Ваша відповідь неправильна. Ви не пройшли перевірку.")
                user_states[user_id]['timer_message_id'] = None
        else:
            logging.info("Індекс відповіді за межами списку відповідей")
    else:
        logging.info(f"Повідомлення не є відповіддю на запитання або не відповідає останньому питанню для користувача {user_id}")

async def show_commands(callback_query: CallbackQuery):
    commands_text = (
        "/start - Почати роботу з ботом\n"
        "/choice - Вибрати предмет для перевірки знань\n"
        "/support - Підтримка\n"
        # Додати інші команди тут
    )
    await callback_query.message.answer(commands_text)
    await callback_query.answer()

def register_callbacks(dp: Dispatcher):
    dp.callback_query.register(handle_our_subject, lambda c: c.data.startswith("subject_"))
    dp.callback_query.register(handle_level, lambda c: c.data.startswith("level_"))
    dp.callback_query.register(show_commands, lambda c: c.data == "show_commands")
    dp.message.register(message_handler)
