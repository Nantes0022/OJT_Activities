from fastapi import APIRouter,Depends,Header,Request
from Models.models import User
from Controller.user_controller import createUser
from fastapi.security import OAuth2PasswordRequestForm
from Controller.user_controller import authenticate_user,create_token, verify_token,refresh_token,generate_refresh_token, generate_access_tokens
from ErrorHandling.errorHandling import clientErrorHandling
from datetime import timedelta

router = APIRouter()

@router.post("/api/v1/users")
async def add_project(user: User):
    userResult = await createUser(user)
    return userResult

@router.post("/api/v1/users/auth")
async def login(username: str = Header(...), password: str = Header(...)):
    return await authenticate_user(username,password)

@router.post("/api/v1/users/token")
def check_token(token:str=Header(...)):
    return verify_token(token)

@router.post("/api/v1/users/token/refresh")
async def get_new_token(request:Request):
    Authorization = request.headers.get("Authorization")
    token = Authorization[7:]
    return await refresh_token(token)


