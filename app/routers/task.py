from typing import Annotated

from app.backend.db_depends import get_db
from app.models import User, Task
from app.schemas import CreateTask, UpdateTask
from fastapi import APIRouter, Depends, status, HTTPException
from slugify import slugify
from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import Session

router = APIRouter(prefix="/task", tags=["task"])


@router.get("/")
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    if tasks is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no tasks found"
        )
    return tasks


@router.get("/task_id")
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no task found"
        )
    return task


@router.post("/create")
async def create_task(db: Annotated[Session, Depends(get_db)], user_id: int, create_new_task: CreateTask):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found"
        )
    db.execute(insert(Task).values(
                                    user_id=user_id,
                                    title=create_new_task.title,
                                    content=create_new_task.content,
                                    priority=create_new_task.priority,
                                    slug=slugify(create_new_task.title)))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


@router.put("/update")
async def update_task(db: Annotated[Session, Depends(get_db)], task_id: int, task_update: UpdateTask):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no task found"
        )
    db.execute(update(Task).where(Task.id == task_id).values(
                                                            title=task_update.title,
                                                            content=task_update.content,
                                                            priority=task_update.priority))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User update is successful'
    }


@router.delete("/delete")
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    task_delete = db.scalar(select(Task).where(Task.id == task_id))
    if task_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no task found"
        )
    db.execute(delete(Task).where(Task.id == task_id))
    db.commit()
    return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'Task delete is successful'
    }
