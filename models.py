from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.orm import declarative_base  # базовый клас

Base = declarative_base()  # базовый класс


class AdvertisementModel(Base):
    __tablename__ = "advertisement"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, unique=True, nullable=False, index=True)
    description = Column(String, nullable=False)
    create_time = Column(
        DateTime, server_default=func.now()
    )  # server_default=func.now() - подставляется время БД, а не клиента
    owner = Column(String, unique=True, nullable=False, index=True)
