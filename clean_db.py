from sqlalchemy import text
from dotenv import load_dotenv
import os
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

# Configurações
DB_USER = "libris"
DB_PASSWORD = "8486"
# DB_HOST = "localhost"
DB_NAME = "libris_db"
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+asyncmy://appuser:secret@localhost:3306/libris_db")

engine = create_async_engine(DATABASE_URL, isolation_level="AUTOCOMMIT")

async def recreate_database():
    async with engine.begin() as conn:
        print(f"🔸 Excluindo banco de dados '{DB_NAME}' se existir...")
        await conn.execute(text(f"DROP DATABASE IF EXISTS {DB_NAME}"))
        print(f"🔹 Criando banco de dados '{DB_NAME}'...")
        await conn.execute(text(f"CREATE DATABASE {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci"))
        print("✅ Banco recriado com sucesso!")
        
asyncio.run(recreate_database())