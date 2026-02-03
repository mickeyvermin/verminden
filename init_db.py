from sqlalchemy.ext.asyncio import create_async_engine
from config import get_settings
from utils.db import Base

config = get_settings()
engine = create_async_engine(config.SQLALCHEMY_DATABASE_URL)

async def create_db_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



# async def init_models() -> None:
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)


# asyncio.run(init_models())
