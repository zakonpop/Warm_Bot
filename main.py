from database import init_db
from scheduler import worker_loop
from bot_instance import dp, bot, router 
import asyncio 
import handlers

async def main():
	await init_db()
	dp.include_router(router)
	print("бот запущен ✅ ")
	await asyncio.gather(
		dp.start_polling(bot),
		worker_loop()
	)
if __name__ == "__main__":
	asyncio.run(main())