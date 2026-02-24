from fastapi import APIRouter, Depends, status, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from api.pydantic.models import CreateUserSchema, UserRead
from infrastructure.repositories.postgresql.user.exceptions import UserIsExist
from api.v1.user.dependencies import create_user_use_case
from usecase.create_user.abstract import AbstractCreateUserUseCase
from usecase.create_user.fast_implementation import RedisFastCreateUserUseCase

router = APIRouter(tags=["User"])
security_scheme = HTTPBearer(scheme_name="Bearer")

@router.post("/users", response_model=UserRead)
async def create_user(
    payload: CreateUserSchema,
    usecase: AbstractCreateUserUseCase = Depends(create_user_use_case)
) -> JSONResponse:
    try:
        user = await usecase.execute(payload)
    except UserIsExist as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=user.model_dump())

@router.get("/users/me", response_model=UserRead)
async def get_user_me(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme)
) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_200_OK, content={})

@router.post("/users/fast")
async def create_user_highload(request: Request, schema: CreateUserSchema):
    redis_client = request.app.state.redis
    usecase = RedisFastCreateUserUseCase(redis_client)
    return await usecase.execute(schema)