DB_USER = "nikolay"
DB_PASSWORD = "310585"
DB_HOST = "127.0.0.1"
DB_PORT = "5431"
DB_BASE = "aiohttp_lecture"


PG_DSN = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_BASE}"  # имя пользователя, пароль, адрес, имя БД
