import json

from aiohttp import web
from sqlalchemy.exc import IntegrityError

from db import Session, engine
from models import AdvertisementModel, Base
from schema import validate, CreateAdvertisementSchema, PutchAdvertisementSchema

app = web.Application()  # создание класса "Application"


# получение объявления по 'id'
async def get_advertisement(advertisement_id: int, session: Session):
    advertisement = await session.get(AdvertisementModel, advertisement_id)
    if advertisement is None:
        raise web.HTTPNotFound(  # HTTPNotFound - встроенная ошибка (может отправлять только 'text')
            text=json.dumps(
                {"status": "error", "description": "Advertisement not found"}
            ),
            content_type="application/json",  # необходимо прописать, что мы отправляем именно 'JSON'
        )
    return advertisement


class Advertisement(web.View):
    async def get(self):
        advertisement_id = int(
            self.request.match_info["advertisement_id"]
        )  # match_info - перебрасывает динамику в 'add_routes'
        async with Session() as session:  # открывает БД
            advertisement = await get_advertisement(
                advertisement_id, session
            )  # создаем объявлениe
            return web.json_response(
                {  # 'json_response' - возврат json-ответа
                    "id": advertisement.id,
                    "title": advertisement.title,
                    "description": advertisement.description,
                    "owner": advertisement.owner,
                    "create_time": advertisement.create_time.isoformat(),  # isoformat() - преобразование в строку
                }
            )

    async def post(self):
        advertisement_data = validate(await self.request.json(), CreateAdvertisementSchema)
          # получаем json-данные по объявлению
        async with Session() as session:  # открывает БД
            new_advertisement = AdvertisementModel(
                **advertisement_data
            )  # передаем в класс все поля, которые получили
            session.add(new_advertisement)
            try:
                await session.commit()
            except IntegrityError as er:  # проверка на уникальность
                raise web.HTTPConflict(  # HTTPNotFound - встроенная ошибка (может отправлять только 'text')
                    text=json.dumps(
                        {"status": "error", "description": "Advertisement olready exists"}
                    ),
                    content_type="application/json",  # необходимо прописать, что мы отправляем именно 'JSON'
                )
            return web.json_response(
                {
                    "status": "new advertisement successfully create",
                    "id": new_advertisement.id,
                }
            )

    async def patch(self):
        advertisement_id = int(
            self.request.match_info["advertisement_id"]
        )  # match_info - перебрасывает динамику в 'add_routes'
        advertisement_data = validate(
            await self.request.json(), PutchAdvertisementSchema
        )  # получаем json-данные объявления
        async with Session() as session:  # открывает БД
            advertisement = await get_advertisement(
                advertisement_id, session
            )  # создаем пользователя
            for field, value in advertisement_data.items():
                setattr(
                    advertisement, field, value
                )  # вставляем полученные данные в полученного пользователя 'user'
                session.add(advertisement)
                await session.commit()
            return web.json_response(
                {
                    "status": "advertisement {advertisement.title} successfully updated"                    
                }
            )

    async def delete(self):
        advertisement_id = int(
            self.request.match_info["advertisement_id"]
        )  # match_info - перебрасывает динамику в 'add_routes'
        async with Session() as session:  # открывает БД
            advertisement = await get_advertisement(
                advertisement_id, session
            )  # создаем пользователя
            await session.delete(advertisement)
            await session.commit()
            return web.json_response({"status": "advertisement successfully deleted"})


# создание 'контекста' работы приложений
async def orm_context(app: web.Application):
    async with engine.begin() as conn:  # подключение к БД
        await conn.run_sync(Base.metadata.create_all)  # миграции
        await conn.commit()
    yield  
    await engine.dispose()  # разрыв соединения с БД


# подключение 'контекста'
app.cleanup_ctx.append(orm_context)


# маршруты ('\d+'' - вместо 'int' ;  Users - класс)
app.add_routes(
    [
        web.get("/advertisements/{advertisement_id:\d+}", Advertisement),
        web.patch("/advertisements/{advertisement_id:\d+}", Advertisement),
        web.delete("/advertisements/{advertisement_id:\d+}", Advertisement),
        web.post("/advertisements/", Advertisement),
    ]
)

if __name__ == "__main__":
    web.run_app(app, port=8000)  # запуск сервера, port=8001 - # смена порта
