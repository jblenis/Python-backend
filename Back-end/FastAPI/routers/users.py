from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class User(BaseModel): #Creo este BaseModel para obtener usuarios si asi lo quisiese, usando POO
    id: int
    name: str
    surname: str
    url: str
    age: int

users_list = [User(id=1,name="Jonathan",surname="Lenis",url="https://wikipedia.com",age= 25),
            User(id=2,name="Sun",surname="Mad",url="https://google.com",age= 21)]

@router.get("/usersjson")
async def usersjson():
    return [{"name":"Jonathan","surname": "Lenis","url": "https://wikipedia.com","age": 30}]

@router.get("/users")
async def users():
    return users_list

#Path
@router.get("/user/{id}")
async def user(id: int):
    return search_user(id)
    
#Query
@router.get("/user/")
async def user(id: int):
    return search_user(id)
    
def search_user(id:int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error":"No se ha encontrado usuario"}
    

@router.post("/user/", response_model=User, status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail="El usuario ya existe")
    else:
        users_list.append(user)
        return user

@router.put("/user/")
async def user(user: User):
    
    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True

    if not found:
        return {"error":"No se ha actualizado usuario"}
    else:
        return user

@router.delete("/user/{id}")
async def user(id: int):

    found = True

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
    if not found:
        return {"error":"No se ha eliminado usuario"}



def search_user(id:int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error":"No se ha encontrado usuario"}