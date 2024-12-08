from typing import Annotated

from app.backend.db_depends import get_db
from app.models import User, Task
from app.schemas import CreateUser, UpdateUser
from fastapi import APIRouter, Depends, status, HTTPException
from slugify import slugify
from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import Session

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/")
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    if users is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no users found"
        )
    return users


@router.get("/user_id")
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no user found"
        )
    return user


@router.get("/user_id/tasks")
async def tasks_by_user_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no user found"
        )
    tasks = db.scalars(select(Task).where(Task.user_id == user_id)).all()
    if tasks is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This user has not tasks"
        )
    return tasks


@router.post("/create")
async def create_user(db: Annotated[Session, Depends(get_db)], create_new_user: CreateUser):
    db.execute(insert(User).values(username=create_new_user.username,
                                   firstname=create_new_user.firstname,
                                   lastname=create_new_user.lastname,
                                   age=create_new_user.age,
                                   slug=slugify(create_new_user.username)))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


@router.put("/update")
async def update_user(db: Annotated[Session, Depends(get_db)], user_id: int, user_update: UpdateUser):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no user found"
        )
    db.execute(update(User).where(User.id == user_id).values(
                                                            firstname=user_update.firstname,
                                                            lastname=user_update.lastname,
                                                            age=user_update.age))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User update is successful'
    }


@router.delete("/delete")
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    user_delete = db.scalar(select(User).where(User.id == user_id))
    if user_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no user found"
        )
    db.execute(delete(User).where(User.id == user_id))

    task_delete = db.scalar(select(Task).where(Task.user_id == user_id))
    if task_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This user has not tasks"
        )
    db.execute(delete(Task).where(Task.user_id == user_id))

    db.commit()
    return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'User delete is successful'
    }
