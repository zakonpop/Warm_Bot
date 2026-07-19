
import asyncio, aiosqlite
from config import file_name

async def seed():
	async with aiosqlite.connect(file_name) as db:
		data = [
			(1, 1, 0, "Цепочка 1, этап 1"),
			(1, 2, 1, "Цепочка 1, этап 2"),
			(1, 3, 1, "Цепочка 1, этап 3"),
			(2, 1, 0, "Цепочка 2, этап 1"),
			(2, 2, 1, "Цепочка 2, этап 2"),
			(2, 3, 1, "Цепочка 2, этап 3"),
			(3, 1, 0, "Цепочка 3, этап 1 (win-back)"),
			(3, 2, 1, "Цепочка 3, этап 2 (win-back)"),
			(3, 3, 1, "Цепочка 3, этап 3 (win-back)"),
		]
		await db.executemany(
			"INSERT INTO chains (chain_id, stage, delay_minutes, text) VALUES (?, ?, ?, ?)",
			data
		)
		await db.commit()

asyncio.run(seed())