from typing import List, Annotated
from datetime import datetime
import uuid
from fastapi import APIRouter, HTTPException, Depends, Response, Cookie
from fastapi.exceptions import RequestValidationError
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import ValidationError

from src.dependencies import get_db
from src import schemas, models
from src.core.hash import get_password_hash, verify_password
from src.core.jwt import (
    create_token_pair,
    decode_access_token,
    add_refresh_token_cookie,
    SUB,
    JTI,
    EXP,
)
from src.exceptions import BadRequestException, NotFoundException, ForbiddenException

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/register", response_model=schemas.User)
async def register(
    data: schemas.UserRegister,
    db: AsyncSession = Depends(get_db),
):
    user = await models.User.find_by_email(db=db, email=data.email)
    if user:
        raise HTTPException(status_code=400, detail="Email has already registered")

    # hashing password
    user_data = data.dict(exclude={"confirm_password"})
    user_data["password"] = get_password_hash(user_data["password"])

    # save user to db
    user = models.User(**user_data)
    user.is_active = False
    await user.save(db=db)

    # send verify email
    user_schema = schemas.User.from_orm(user)
    return user_schema

@router.post("/login")
async def login(
    data: schemas.UserLogin,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    user = await models.User.authenticate(
        db=db, email=data.email, password=data.password
    )

    if not user:
        raise BadRequestException(detail="Incorrect email or password")

    user = schemas.User.from_orm(user)

    token_pair = create_token_pair(user=user)

    add_refresh_token_cookie(response=response, token=token_pair.refresh.token)

    return {"token": token_pair.access.token}

@router.post("/logout", response_model=schemas.SuccessResponseScheme)
async def logout(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncSession = Depends(get_db),
):
    payload = await decode_access_token(token=token, db=db)
    black_listed = models.BlackListToken(
        id=payload[JTI], expire=datetime.utcfromtimestamp(payload[EXP])
    )
    await black_listed.save(db=db)

    return {"msg": "Successfully logged out"}

@router.get("/hello", response_model=schemas.SuccessResponseScheme) 
async def hello():
    return {"msg": "hello"}

@router.post("/password-update", response_model=schemas.SuccessResponseScheme)
async def password_update(
    token: Annotated[str, Depends(oauth2_scheme)],
    data: schemas.PasswordUpdateSchema,
    db: AsyncSession = Depends(get_db),
):
    payload = await decode_access_token(token=token, db=db)
    user = await models.User.find_by_id(db=db, id=payload[SUB])
    if not user:
        raise NotFoundException(detail="User not found")

    # raise Validation error
    if not verify_password(data.old_password, user.password):
        try:
            schemas.OldPasswordErrorSchema(old_password=False)
        except ValidationError as e:
            raise RequestValidationError(e.raw_errors)
    user.password = get_password_hash(data.password)
    await user.save(db=db)

    return {"msg": "Successfully updated"}

# User Management Endpoints

@router.get("/users", response_model=List[schemas.User])
async def list_users(token: Annotated[str, Depends(oauth2_scheme)], db: AsyncSession = Depends(get_db)):
    payload = await decode_access_token(token=token, db=db)
    user = await models.User.find_by_id(db=db, id=payload[SUB])
    if not user:
        raise NotFoundException(detail="User not found")
    users = await models.User.get_all_users(db=db)
    return users

@router.post("/users", response_model=schemas.User)
async def create_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    data: schemas.UserCreate,
    db: AsyncSession = Depends(get_db),
):
    payload = await decode_access_token(token=token, db=db)
    user = await models.User.find_by_id(db=db, id=payload[SUB])
    if not user:
        raise NotFoundException(detail="User not found")
    
    user = await models.User.find_by_email(db=db, email=data.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_data = data.dict()
    user_data["password"] = get_password_hash(user_data["password"])

    user = models.User(**user_data)
    await user.save(db=db)

    return schemas.User.from_orm(user)

# Task Management Endpoints

@router.get("/tasks")
async def tasks(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncSession = Depends(get_db),
):
    payload = await decode_access_token(token=token, db=db)
    user = await models.User.find_by_id(db=db, id=payload[SUB])
    if not user:
        raise NotFoundException(detail="User not found")

    print(user)
    tasks = await models.Task.find_by_author(db=db, author=user)

    return [schemas.TaskListScheme.from_orm(task) for task in tasks]

@router.get("/tasks/{task_id}", response_model=schemas.TaskListScheme)
async def find_task_by_id(
    task_id: str,
    token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncSession = Depends(get_db),
):
    payload = await decode_access_token(token=token, db=db)
    user = await models.User.find_by_id(db=db, id=payload[SUB])
    if not user:
        raise NotFoundException(detail="User not found")

    task = await models.Task.find_by_id(db=db, task_id=uuid.UUID(task_id))
    if not task or task.author_id != user.id:
        raise NotFoundException(detail="Task not found or you do not have permission to view this task")

    return task


@router.post("/tasks", response_model=schemas.SuccessResponseScheme, status_code=201)
async def create_task(
    token: Annotated[str, Depends(oauth2_scheme)],
    data: schemas.TaskCreateSchema,
    db: AsyncSession = Depends(get_db),
):
    payload = await decode_access_token(token=token, db=db)
    user = await models.User.find_by_id(db=db, id=payload[SUB])
    if not user:
        raise NotFoundException(detail="User not found")

    task = models.Task(**data.dict())
    task.author = user

    await task.save(db=db)

    return {"msg": "Task successfully created"}

@router.put("/tasks/{task_id}", response_model=schemas.SuccessResponseScheme)
async def update_task(
    task_id: str,
    token: Annotated[str, Depends(oauth2_scheme)],
    task_update: schemas.TaskCreateSchema,
    db: AsyncSession = Depends(get_db),
):
    payload = await decode_access_token(token=token, db=db)
    user = await models.User.find_by_id(db=db, id=payload[SUB])
    if not user:
        raise NotFoundException(detail="User not found")

    task = await models.Task.find_by_id(db=db, task_id=uuid.UUID(task_id))
    if not task or task.author_id != user.id:
        raise NotFoundException(detail="Task not found or you do not have permission to update this task")

    for key, value in task_update.dict(exclude_unset=True).items():
        setattr(task, key, value)
    await db.commit()

    return {"msg": "Task successfully updated"}


@router.delete("/tasks/{task_id}", response_model=schemas.SuccessResponseScheme)
async def delete_task(
    task_id: str,
    token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncSession = Depends(get_db),
):
    payload = await decode_access_token(token=token, db=db)
    user = await models.User.find_by_id(db=db, id=payload[SUB])
    if not user:
        raise NotFoundException(detail="User not found")

    task = await models.Task.find_by_id(db=db, task_id=uuid.UUID(task_id))
    if not task or task.author_id != user.id:
        raise NotFoundException(detail="Task not found or you do not have permission to delete this task")

    await db.delete(task)
    await db.commit()
    return {"msg": "Task successfully deleted"}

