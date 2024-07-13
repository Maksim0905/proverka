import aiosqlite
import asyncio
from bot.config import db

async def first_join(user_id):
    async with aiosqlite.connect(db) as connection:
        async with connection.cursor() as cursor:
            await cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            row = await cursor.fetchone()
            if row is None:
                await cursor.execute("INSERT INTO users (user_id, name) VALUES (?, ?)", (user_id, f'museum-{user_id}'))
                await cursor.execute("INSERT INTO filters (chat_id) VALUES (?)", (int(user_id),))
            await connection.commit()


async def get_exponats(chat_id):
    async with aiosqlite.connect(db) as connection:
        async with connection.cursor() as cursor:
            await cursor.execute('SELECT * FROM artifacts WHERE owner = ?', (chat_id, ))
            row = await cursor.fetchall()
            return row
        

async def add_expo(chat_id, name, about, era, country, photo):
    async with aiosqlite.connect(db) as connection:
        async with connection.cursor() as cursor:
            await cursor.execute("INSERT INTO artifacts (owner, name, about, era, country, photo) VALUES (?, ?, ?, ?, ?, ?)", (f'museum-{chat_id}', name, about, era, country, photo))
            await connection.commit()


async def add_artefact_trash(id, data):
    async with aiosqlite.connect(db) as connection:
        async with connection.cursor() as cursor:
            await cursor.execute("INSERT INTO trash (id, data) VALUES (?, ?)", (id, data))
            await connection.commit()


async def get_artefact_trash(id):
    async with aiosqlite.connect(db) as connection:
        async with connection.cursor() as cursor:
            await cursor.execute('SELECT data FROM trash WHERE id = ?', (id,))
            row = await cursor.fetchone()
            return row
        

async def get_all_names_of_artefacts():
    async with aiosqlite.connect(db) as connection:
        async with connection.cursor() as cursor:
            await cursor.execute('SELECT id, name FROM artifacts')
            row = await cursor.fetchall()
            return row
        

async def get_filtered_artifacts(chat_id):
    async with aiosqlite.connect(db) as connection:
        async with connection.cursor() as cursor:
            await cursor.execute("SELECT era, country, about FROM filters WHERE chat_id = ?", (chat_id,))
            filters = await cursor.fetchone()
            print(filters)
            era_filter, country_filter, about_filter = filters
            print(era_filter, country_filter, about_filter)
            
            query = "SELECT id, name FROM artifacts WHERE 1=1"
            params = []

            if era_filter:
                query += " AND era = ?"
                params.append(era_filter)
            if country_filter:
                query += " AND country = ?"
                params.append(country_filter)
            if about_filter:
                query += " AND LOWER(about) LIKE LOWER(?)"
                params.append(f"%{about_filter}%")

            print(query)

            await cursor.execute(query, params)
            artifacts = await cursor.fetchall()
            
            return artifacts
        

async def get_artefact(artefact_id):
    async with aiosqlite.connect(db) as connection:
        async with connection.cursor() as cursor:
            await cursor.execute('SELECT * FROM artifacts WHERE id = ?', (artefact_id, ))
            row = await cursor.fetchone()
            return row
        

async def delete_filters(chat_id):
    async with aiosqlite.connect(db) as connection:
        async with connection.cursor() as cursor:
            await cursor.execute("UPDATE filters SET era = NULL, country = NULL, about = NULL WHERE chat_id = ?", (chat_id,))
            await connection.commit()


async def filter_era(chat_id, era):
    async with aiosqlite.connect(db) as connection:
        async with connection.cursor() as cursor:
            await cursor.execute("UPDATE filters SET era = ? WHERE chat_id = ?", (era, chat_id))
            await connection.commit()


async def filter_country(chat_id, country):
    async with aiosqlite.connect(db) as connection:
        async with connection.cursor() as cursor:
            await cursor.execute("UPDATE filters SET country = ? WHERE chat_id = ?", (country, chat_id))
            await connection.commit()

async def filter_about(chat_id, about):
    async with aiosqlite.connect(db) as connection:
        async with connection.cursor() as cursor:
            await cursor.execute("UPDATE filters SET about = ? WHERE chat_id = ?", (about, chat_id))
            await connection.commit()