from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session # Сессия БД
from app.backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from app.models import *
from app.schemas.task import *
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete
# Функция создания slug-строки
from slugify import slugify


router = APIRouter(prefix="/task", tags=["task"])

@router.get("/")
async def all_task(db: Annotated[Session, Depends(get_db)]):
    tasks = db.query(Task).all()
    return tasks
@router.get("/task_id")
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id: int):
    result = db.query(Task).filter(task_id == Task.id).first()
    if result is None:
            raise HTTPException(status_code=404, detail="User was not found")
    return result


@router.post("/create")
async def create_task(db: Annotated[Session, Depends(get_db)], create_task: CreateTask, user_id: int):
    # Ищем пользователя по user_id
    existing_user = db.query(User).filter(user_id == User.id) .first()

    if existing_user:
        existing_ids = db.scalars(select(Task.id)).all()  # Получаем все существующие id задач
        new_id = 1

        # Находим первый доступный id для новой задачи
        while new_id in existing_ids:
            new_id += 1

        # Создаем новую задачу, связывая ее с пользователем
        db.execute(insert(Task).values( title = create_task.title,
                                        slug = slugify(create_task.title),
                                        content = create_task.content,
                                        priority = create_task.priority,
                                        user_id = user_id))
    else:
        raise HTTPException(status_code=404, detail="User was not found")

    db.commit()

    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }




@router.get("/user_id/task")
async def tasks_dy_user_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    result = db.query(Task).filter(user_id == Task.id).first()
    if result is None:
        raise HTTPException(status_code=404, detail="User was not found")
    return result
@router.put("/update")
async def update_task(db: Annotated[Session, Depends(get_db)], task_id: int, update_task: UpdateTask):
    update_task_result = db.execute(select(Task).where(task_id == Task.id )).fetchone()
    if update_task_result is None:
        raise HTTPException(
        status_code= status.HTTP_404_NOT_FOUND,
        detail="User was not found"
        )

    db.execute(update(Task).where(task_id == Task.id).values(
        title=update_task.title,
        content=update_task.content,
        priority=update_task.priority
    ))
    db.commit()
    return {'status_code': status.HTTP_200_OK,
            'transaction': 'User update is successful!'}

@router.delete("/delete")
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    task_del = db.execute(select(User).where(task_id == Task.id)).fetchone()
    if task_del is None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="Task was not found"
        )
    else:
        db.execute(delete(User).where(task_id == Task.id))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Task update is successful!'
    }