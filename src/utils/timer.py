from aiogram.types import Message
import asyncio
import logging

async def display_timer(message: Message, seconds: int, user_id: int, user_states: dict):
    previous_message_content = ""
    for sec in range(seconds, 0, -1):
        try:
            await asyncio.sleep(1)
            new_message_content = f"Таймер: {sec} секунд"
            if new_message_content != previous_message_content:
                await message.edit_text(new_message_content)
                previous_message_content = new_message_content
        except Exception as e:
            if "message is not modified" in str(e):
                logging.info("Повідомлення не змінилося, пропускаємо оновлення.")
            else:
                logging.error(f"Помилка при оновленні таймера: {e}")
                break
    try:
        await message.edit_text("Час вийшов!")
        user_states[user_id]['time_expired'] = True
    except Exception as e:
        logging.error(f"Помилка при оновленні таймера: {e}")

async def stop_timer(message: Message, timer_message_id: int):
    try:
        await message.bot.edit_message_text(chat_id=message.chat.id, message_id=timer_message_id, text="Таймер зупинено")
    except Exception as e:
        logging.error(f"Помилка при зупинці таймера: {e}")
