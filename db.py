from sqlalchemy.ext.asyncio import (  # класс асинхронных сессий и движок
    AsyncSession, create_async_engine)
from sqlalchemy.orm import sessionmaker  # сессия

from config import PG_DSN

engine = create_async_engine(PG_DSN)  # асинхронный движок
Session = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)  # 'class_=AsyncSession' - в качестве базового класса использовать 'AsyncSession' ; 'expire_on_commit=False' - завершение сессии после коммита
