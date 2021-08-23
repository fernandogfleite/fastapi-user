from fast_api_app import (
    schemas,
    models
)
from sqlalchemy.orm import Session
from fast_api_app.database import database

items = models.Item.__table__
users = models.UserTable.__table__


async def get_user(user_id: int):
    query = users.select().where(models.UserTable.id == user_id)
    resultset = await database.fetch_one(query)
    return dict(resultset)


async def create_user_item(item: schemas.ItemCreate, user_id: int):
    query = items.insert().values(title=item.title, description=item.description,
                                  price=item.price, owner_id=user_id)
    last_record_id = await database.execute(query)
    return {"id": last_record_id, **item.dict(), "owner_id": user_id}


async def get_items(user_id: int):
    query = items.select().where(models.Item.owner_id == user_id)
    resultset = await database.fetch_all(query)
    items_list = list()
    for item in resultset:
        items_list.append(dict(item))

    return items_list
