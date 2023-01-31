import logging

from aiogram import Bot, Dispatcher, executor, types
TOKEN = "6144966883:AAEFn-cgyOzNoyJWBVZHcFvuzRtuZlAoGsY"
logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler()
async def echo(message: types.Message):
	await message.answer(message.text)

if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=False)
