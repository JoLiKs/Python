import logging
import os
import asyncio
from aiogram import Bot, Dispatcher, executor, types

f = open('/home/worker/PYTHON_BOT/bot/words.txt', 'r', encoding='utf-8')
bad_words = f.read().split()

logging.basicConfig(level=logging.INFO)

async def delmsg_delay(message: types.Message, sleep_time: int = 0):
	await asyncio.sleep(sleep_time)
	await message.delete()

async def on_user_joined(message: types.Message):
	await message.delete()

async def filter_message(message: types.Message):
	for s in bad_words:
		if s in message.text.lower():
			await message.delete()
			msg = await message.answer("Ругаться нехорошо!")
			asyncio.create_task(delmsg_delay(msg, 3))
			return


async def register_handlers(dp: Dispatcher):

	dp.register_message_handler(on_user_joined, content_types=['new_chat_members'])
	dp.register_message_handler(filter_message)

async def process_event(update, dp: Dispatcher):

	Bot.set_current(dp.bot)
	await dp.process_update(update)

# Selectel serverless entry point
async def main(**kwargs):
	bot = Bot(os.environ.get("TOKEN"))
	dp = Dispatcher(bot)

	await register_handlers(dp)

	update = types.Update.to_object(kwargs)
	await process_event(update, dp)

	return 'ok'

