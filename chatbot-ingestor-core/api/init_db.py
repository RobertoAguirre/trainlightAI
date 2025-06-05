import asyncio
from api.database import engine
from api.models.db_models import Base

async def init_db():
    """Inicializar la base de datos creando todas las tablas"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    print("Base de datos inicializada correctamente")

if __name__ == "__main__":
    asyncio.run(init_db()) 