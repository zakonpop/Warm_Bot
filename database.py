import aiosqlite
from config import file_name, chat_id
from datetime import datetime, timezone


async def init_db():
	async with aiosqlite.connect(file_name) as db:
		await db.execute("""
			CREATE TABLE IF NOT EXISTS users(
				user_id INTEGER PRIMARY KEY,
				subscribed INTEGER DEFAULT 0,
				chain_id INTEGER DEFAULT 1,
				stage INTEGER DEFAULT 1,
				last_sent_at TEXT,
				joined_at TEXT
			)
		""")
		
		await db.execute('''
			CREATE TABLE IF NOT EXISTS chains(
				id INTEGER PRIMARY  KEY,
				chain_id INTEGER DEFAULT 0,
				stage INTEGER DEFAULT 0,
				delay_minutes INTEGER DEFAULT 0,
				text TEXT
			)
		''')
		
		await db.commit()

async def get_user(user_id: int):
	async with aiosqlite.connect(file_name) as db:
		db.row_factory = aiosqlite.Row
		cursor = await db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
		row = await cursor.fetchone()
		return row


async def create_user(user_id: int):
	async with aiosqlite.connect(file_name) as db:
		await db.execute(
		"INSERT INTO users (user_id, joined_at) VALUES (?, ?)",
		(user_id, datetime.now(timezone.utc).isoformat(sep=' ', timespec='seconds'))
		)
		await db.commit()

async def update_sub_status(user_id: int, sub: bool):
	async with aiosqlite.connect(file_name) as db:
		await db.execute("UPDATE users SET subscribed = ? WHERE user_id = ?", (int(sub), user_id))
		await db.commit()


async def switch_chain(user_id: int, chain_id: int, stage: int = 1):
	async with aiosqlite.connect(file_name) as db:
		await db.execute(
			"UPDATE users SET chain_id = ?, stage = ?, last_sent_at = ? WHERE user_id = ?",
			(chain_id, stage, datetime.now(timezone.utc).isoformat(sep=' ', timespec='seconds'), user_id)
		)
		await db.commit()
		

async def get_all_active_users() -> dict:
	async with aiosqlite.connect(file_name) as db:
		db.row_factory = aiosqlite.Row
		
		cursor = await db.execute('''
			SELECT users.user_id, users.chain_id, users.stage
			FROM users
			JOIN chains ON chains.chain_id = users.chain_id AND chains.stage = users.stage +1
			WHERE datetime(users.last_sent_at, "+" || chains.delay_minutes || " minutes") <= datetime('now')
		''')
		rows = await cursor.fetchall()
		return rows


async def advance_stage(user_id: int):
	async with aiosqlite.connect(file_name) as db:
		await db.execute(
			"UPDATE users SET stage = stage + 1, last_sent_at = ? WHERE user_id = ?",
			(datetime.now(timezone.utc).isoformat(sep=' ', timespec='seconds'), user_id)
		)
		await db.commit()
		
async def get_chain_message(chain_id: int, stage: int) -> str:
	async with aiosqlite.connect(file_name) as db:
		db.row_factory = aiosqlite.Row
		
		cursor  = await db.execute("SELECT text FROM chains WHERE chain_id = ? AND stage = ?",
		(chain_id, stage)
		)
		row = await cursor.fetchone()
		return  row["text"] if row else None

async def mark_sent(user_id: int):
	async with aiosqlite.connect(file_name) as db:
		await db.execute(
			"UPDATE users SET last_sent_at = ? WHERE user_id = ?",
			(datetime.now(timezone.utc).isoformat(sep=' ', timespec='seconds'), user_id)
		)
		await db.commit()		