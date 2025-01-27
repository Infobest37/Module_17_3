from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session # Сессия БД
from app.backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from app.models import *
from app.schemas.task import CreateTask
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
async def create_task(db: Annotated[Session, Depends(get_db)], create_task: CreateTask,
        user_id: int
):
    # Проверяем, существует ли пользователь
    existing_user = db.query(User).filter(user_id == User.id ).first()

    if not existing_user:
        raise HTTPException(status_code=404, detail="User was not found")

    # Получаем все существующие id задач
    existing_ids = db.scalars(select(Task.id)).all()
    new_id = 1

    # Находим первый доступный id для новой задачи
    while new_id in existing_ids:
        new_id += 1

    # Создаем новую задачу, связывая ее с пользователем
    db.execute(insert(Task).values(
        id=new_id,  # Новый id задачи
        title=create_task.title,
        content=create_task.content,
        priority=create_task.priority,
        completed=False,  # Можно установить по умолчанию
        user_id=user_id,  # Связываем с пользователем
        slug=slugify(create_task.title)  # Предполагается, что slugify доступна
    ))

    db.commit()

    return {
        'status_code': 201,  # Код ответа для успешного создания
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