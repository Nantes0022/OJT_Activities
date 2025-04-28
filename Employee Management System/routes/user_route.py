from fastapi import APIRouter,Depends,Header,Request
from Models.models import User
from Controller.user_controller import createUser,check_if_admin_role
from fastapi.security import OAuth2PasswordRequestForm
from Controller.user_controller import authenticate_user,create_token, verify_token,refresh_token,generate_refresh_token, generate_access_tokens
from ErrorHandling.errorHandling import clientErrorHandling,credentials_exception,serverErrorHandling
from datetime import timedelta
from jose import JWTError

router = APIRouter()

@router.post("/api/v1/users")
async def add_project(user: User,request:Request):
    try:
        Authorization = request.headers.get("Authorization")
        token = Authorization[7:]
        is_admin = check_if_admin_role(token)
        print(is_admin)
        if not is_admin:
            print("if condition")
            raise credentials_exception()
        userResult = await createUser(user)
        return userResult
    except JWTError as e:
        raise serverErrorHandling(e)

@router.post("/api/v1/users/auth")
async def login(username: str = Header(...), password: str = Header(...)):
    try:
        return await authenticate_user(username,password)
    except JWTError as e:
        raise serverErrorHandling(e)

@router.get("/api/v1/users/token")
def check_token(token:str=Header(...)):
    return verify_token(token)

@router.post("/api/v1/users/token/refresh")
async def get_new_token(request:Request):
    Authorization = request.headers.get("Authorization")
    token = Authorization[7:]
    return await refresh_token(token)


