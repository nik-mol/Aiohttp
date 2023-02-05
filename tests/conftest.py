#  conftest.py - выполняется один раз
# pip install psycopg2-binary  - для работы с синхронной sqlalchemy

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DB_BASE, DB_HOST, DB_PASSWORD, DB_PORT, DB_USER
from models import AdvertisementModel, Base

PG_DSN = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_BASE}"
engine = create_engine(PG_DSN)  # синхронный движок
Session = sessionmaker(bind=engine)  # синхронная сессия


# фикстура для инициализации БД (запускается автоматически)
@pytest.fixture(
    scope="session", autouse=True
)  # scope='session' - запускается один раз за сессию, autouse=True - запускается автоматически
def init_database():
    Base.metadata.drop_all(bind=engine)  # удаление всех таблиц с БД
    Base.metadata.create_all(bind=engine)  # создание всех таблиц с БД


# фикстура для создания пользователя (запускается вручную)
@pytest.fixture()
def create_advertisement():
    with Session() as session:
        new_advertisement = AdvertisementModel(
            title="test_advertisement",
            description="test_description",
            owner="test_owner",
        )  # создание объявления
        session.add(new_advertisement)  # добавление объявление в commit
        session.commit()  # сохранение объявление в БД
        return {
            "id": new_advertisement.id,
            "title": new_advertisement.title,
            "description": new_advertisement.description,
            "owner": new_advertisement.owner,
        }
