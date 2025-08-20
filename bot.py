from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = "7948321256:AAE2VxKHA4NaER0N3z7gtw6s5vFUDXc70aY"  # bu yerga o'zingning BotFather bergan tokenni qo'yasan

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)

if name == "main":
    executor.start_polling(dp, skip_updates=True)
