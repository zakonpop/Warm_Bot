from aiogram import F
from aiogram.types import  Message, ChatMemberUpdated
from aiogram.filters import Command, CommandStart
from database import get_user, create_user, get_chain_message, switch_chain, mark_sent
from subscription import check_sub_status, apply_sub_status
from config import  owner_id, chat_id
from bot_instance import  bot, router



@router.message(CommandStart())
async def  cmd_start(message: Message):
	
	user_id = message.from_user.id
	user = await get_user(user_id)
	
	sub = await check_sub_status(user_id)
	if sub is None:
		await bot.send_message(owner_id,"Чтоб бот работал, ему нужно, чтоб он работал, находиться и быть админом в канале/чате.")
		await message.answer("Извините, но похоже  бот пока что не работает, попробуйте еще раз  через пару минут...")
		return
	
	if not user:
		await create_user(user_id)
		chain_id = 2 if sub else 1
		stage = 1
		await mark_sent(user_id)
	else:
		stage = user["stage"]
		chain_id = user["chain_id"]

	text = await get_chain_message(chain_id=chain_id, stage=stage)
	if text is None:
		print("текста нет")
		return 
	await message.answer(text)

@router.chat_member()
async def on_chat_member_update(event: ChatMemberUpdated):
	if event.chat.id != chat_id:
		return

	user_id = event.new_chat_member.user.id
	new_status = event.new_chat_member.status in {"member", "administrator", "creator"}

	await apply_sub_status(user_id, new_status)
	

