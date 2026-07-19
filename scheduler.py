import asyncio
from database import get_all_active_users, get_chain_message, advance_stage, get_user
from subscription import process_sub_check
from bot_instance import bot

async def worker_loop():
	while True:
		users = await get_all_active_users()
		
		for user in users:
			await process_sub_check(user["user_id"])
			
			
			update_user =  await get_user(user["user_id"])
			text = await get_chain_message(update_user["chain_id"], update_user["stage"] +1)
			if text is None:
				continue
			await bot.send_message(update_user["user_id"], text)
			await advance_stage(update_user["user_id"])
		await asyncio.sleep(60)

			
		