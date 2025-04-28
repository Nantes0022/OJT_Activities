from connection.database import db
from Models.models import User,AuthToken
from ErrorHandling.errorHandling import clientErrorHandling,serverErrorHandling,successHTTP
from fastapi import HTTPException,Depends,Header
import json
from fastapi.security import OAuth2PasswordBearer
from traceback import format_exc
from passlib.context import CryptContext
from datetime import datetime,timedelta,timezone
import os
from jose import JWTError, jwt
from ErrorHandling.errorHandling import token_exception, credentials_exception


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
userCollection = db['userList']
tokenCollection = db['tokenList']

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 5
REFRESH_TOKEN_EXPIRE_DAYS=7

#Creating User
def hash_password(password:str) -> str:
    return pwd_context.hash(password)

async def createUser(user: User):
    print("TRY BLOCK EXECUTING") 
    userDict = user.model_dump()
        
    req_Fields = ['username','password']
    miss_Fields = [field for field in req_Fields if not userDict.get(field)]
    employeeCheck = await userCollection.find_one({"username": userDict["username"]},{"_id":0})
    password = userDict["password"]
    if password != None:
        userDict["password"] = hash_password(userDict["password"])

    if miss_Fields:
        raise clientErrorHandling(400, "Bad Request", f"Missing required fields: {', '.join(miss_Fields)}",userDict)  
    elif employeeCheck:
        raise clientErrorHandling(409, "Conflict", f"Username {userDict['username']} already exists.",userDict)
            
    users = await userCollection.insert_one(userDict)
    if users.acknowledged:
        print("EMPLOYEE INSERTED SUCCESSFULLY")  
        userDict.pop("_id", None)
        return successHTTP( "Created", f"User Information Inserted",userDict)
    else:
        clientErrorHandling(200,"OK","An Error has been occured on updating information",user.model_dump(mode="json"))
#Login Function

async def authenticate_user(username: str, password: str):
    user = await userCollection.find_one({"username": username})
    if user is None or not verify_password(password, user["password"]):
        return clientErrorHandling(404,"Not Found","Password Incorrect","")
    access_token= await generate_access_tokens(user)
    refresh_token,expire = await generate_refresh_token(user)
    await add_value(refresh_token,user["userId"],datetime.now(timezone.utc),expire,user["role"])
    return {"access_token":access_token,"refresh_token":refresh_token}

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def create_token(data:dict, expires_delta: timedelta = None, role:str = None):
    try:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"token_type":"bearer","role":role,"exp": expire})
        token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        
        return token,to_encode,expire
    except JWTError as e:
        print(e)
        raise token_exception
    except Exception as e:
        return e
    
async def generate_access_tokens(data: dict):
    token,data,expire = await create_token({"sub": data["username"]}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),data["role"])
    return token

async def generate_refresh_token(data: dict):
    token,data,expire = await create_token({"sub": data["username"]}, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),data["role"])
    return token,expire

async def add_value(token:str,username:str,createdAt:datetime,expiresAt:datetime,role:str):
    tokenModel = AuthToken
    
    gen_token = tokenModel(
        token=token,
        username=username,
        createdAt=createdAt,
        expiresAt=expiresAt,
        role=role,
        isActive=True
    )
    data = gen_token.model_dump()
    tokens = await tokenCollection.insert_one(data)


    

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        expire_timestamp = payload.get("exp")
            
        if expire_timestamp is None:
            raise HTTPException(status_code=401, detail="Token has no expiration")

        expire_datetime = datetime.fromtimestamp(expire_timestamp)

        if expire_datetime < datetime.now():
            raise HTTPException(status_code=401, detail="Token expired")

        print("Token expires at:", expire_datetime)

        return {
            "sub": payload.get("sub"),
            "expires_at": expire_datetime,
            "payload": payload,
        }

    except JWTError as e:
        print(e)
        raise token_exception()


def check_if_admin_role(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    role = payload.get("role")
    print("Role from token:", role)
    if role == "Administrator":
        return True
    return False

#refresh token
async def refresh_token(token):
    try:
        print(token)
        checkUser = await tokenCollection.find_one({"token":token})
        print(checkUser)
        if checkUser is None:
            raise clientErrorHandling(404,"Not Found","No token found. Not authorized to refresh Token","")
        
        access_token= await generate_access_tokens(checkUser)
        return {"new_access_token":access_token}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")