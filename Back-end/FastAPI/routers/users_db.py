from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema,users_schema
from db.client import db_client
from bson import ObjectId

router = APIRouter(prefix="/userdb",
                    tags=["userdb"],
                    responses={status.HTTP_404_NOT_FOUND: {"message":"No encontrado"}})


users_list = []



@router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.users.find())

#Path
@router.get("/{id}")
async def user(id: str):
    return search_user("_id", ObjectId(id))
    
#Query
@router.get("/")
async def user(id: str):
    return search_user("_id", ObjectId(id))


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    if type(search_user("email", user.email)) == User:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")

    user_dict = dict(user)
    del user_dict["id"]

    id = db_client.users.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.users.find_one({"_id": id}))


    return User(**new_user)

from bson import ObjectId

@router.put("/", response_model=User)
async def update_user(user: User):
    user_dict = dict(user)
    user_id = user_dict.get("id")  # Obtener el valor del ID del usuario

    if not user_id:
        return {"error": "El usuario no tiene un ID válido"}

    try:
        result = db_client.users.find_one_and_replace({"_id": ObjectId(user_id)}, user_dict, return_document=True)

        if not result:
            return {"error": "Usuario no encontrado"}

        return result

    except Exception as e:
        return {"error": f"No se ha podido actualizar el usuario: {str(e)}"}
    

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):

    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        return {"error":"No se ha eliminado usuario"}



def search_user(field:str, key):
    
    try:
        user = db_client.users.find_one({field:key})
        return User(**user_schema(user))
    except:
        return {"error":"No se ha encontrado usuario"}
    
