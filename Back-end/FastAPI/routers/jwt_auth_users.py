from fastapi import APIRouter,HTTPException, Depends, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt , JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM= "HS256"

ACCESS_TOKEN_DURATION= 1

SECRET= "8a5d7b5de04f84caa48f85cf1241a32173167b752eec995dd478f1cf47cde8df"

router= APIRouter()

oauth2= OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db ={
    "windu":{
        "username": "windu",
        "full_name": "Jonathan Lenis",
        "email": "jonathanlenis@gmail.com",
        "disabled": False,
        "password": "$2a$12$qNRSG.5.0uo1a8l8RB.bSOBwkMoBLQjOVBY66Mw1s994m1Gvrb.9a"
    },
    "windu2":{
        "username": "windu2",
        "full_name": "Jonathan Lenis 2",
        "email": "jonathanlenis2@gmail.com",
        "disabled": True,
        "password": "$2a$12$M/aP3AfTmO8id54xKOPHEug5mfF8pZXb0u398zXTW9qnmiMevS9lS"
    }
}

def search_user_db(username:str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username:str):
    if username in users_db:
        return UserDB(**users_db[username])
    
async def auth_user(token: str= Depends(oauth2)):
    
    exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED ,
                detail="Credenciales de autenticacion invalidas",
                headers={"WWW-Authenticate": "Bearer"})
            
    try:
        username =jwt.decode(token,SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception
    
    except JWTError:
        raise exception
    
    return search_user(username)
        

async def current_user(user:User =Depends(auth_user)): 
    if user.disabled:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")
    
    return user
    
@router.post("/login")
async def login(form:OAuth2PasswordRequestForm= Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario no es correcto"
        )
    
    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contrasena no es correcto"
        )
    
    access_token = {"sub": user.username, 
                    "exp": datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_DURATION)}

    return {"access_token": jwt.encode(access_token, SECRET, algorithm = ALGORITHM),"token_type" : "bearer"}


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
