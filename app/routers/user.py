from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session # Сессия БД
from app.backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from app.models import *
from app.schemas.user import CreateUser, UpdateUser
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete
# Функция создания slug-строки
from slugify import slugify





router = APIRouter(prefix="/user", tags=["user"])

@router.get("/")
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users

@router.get("/user_id")
async def user_by_id(user_id: int,db: Annotated[Session, Depends(get_db)]):
    result = db.scalars(select(User).where(user_id == User.id)).first()

    if result is None:
            raise HTTPException(status_code=404, detail="User was not found")
    return result




@router.post("/create")
async def create_user(create_user: CreateUser, db: Annotated[Session, Depends(get_db)]):
    existing_user = db.execute(select(User).where(create_user.username == User.username)).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # Получаем все существующие id пользователей
    existing_ids = db.scalars(select(User.id)).all()

    # Находим первый доступный id
    new_id = 1
    while new_id in existing_ids:
        new_id += 1

    # Вставляем нового пользователя
    db.execute(insert(User).values(id=new_id,  # Указываем новый id
                                   username=create_user.username,
                                   slug=slugify(create_user.username),
                                   firstname=create_user.firstname,
                                   lastname=create_user.lastname,
                                   age=create_user.age))
    db.commit()

    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }

@router.put("/update")
async def update_user(db: Annotated[Session, Depends(get_db)], user_id: int, update_user: UpdateUser):
    update_user_result = db.execute(select(User).where(user_id == User.id )).fetchone()
    if update_user_result is None:
        raise HTTPException(
        status_code= status.HTTP_404_NOT_FOUND,
        detail="User was not found"
        )

    db.execute(update(User).where(user_id == User.id).values(
        firstname=update_user.firstname,
        slug=slugify(update_user.firstname),
        lastname=update_user.lastname,
        age=update_user.age
    ))
    db.commit()
    return {'status_code': status.HTTP_200_OK,
            'transaction': 'User update is successful!'}

@router.delete("/delete")
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    user_del = db.execute(select(User).where(user_id == User.id)).fetchone()
    if user_del is None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="User was not found"
        )
    else:
        db.execute(delete(User).where(user_id == User.id))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User update is successful!'
    }