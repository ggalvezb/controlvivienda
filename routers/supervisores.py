from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from db.client import db_client
from db.models.supervisores import Supervisor
from db.schemas.supervisores import supervisor_schema, supervisores_schema
from bson import ObjectId
from routers.auth_user import oauth2

router=APIRouter(prefix="/supervisores",tags=["Supervisores"])



#Retorno todos los Usuarios
@router.get("/", response_model=list[Supervisor])
async def users(token:str = Depends(oauth2)):
    #Reviso Token
    pass_token(token)

    return supervisores_schema(db_client.users.find())

#Retorno un usuario en especifico
@router.get("/{id}")
async def user(id:str,token:str = Depends(oauth2)):
    #Reviso Token
    pass_token(token)

    return search_user("_id", ObjectId(id))

#Agrego un usuario a la BD
@router.post("/")
async def user(user:Supervisor,token:str = Depends(oauth2)):
    #Reviso Token
    pass_token(token)

    if type(search_user("email",user.email)) == Supervisor:
        return {"El usuario ya existe"}

    user_dict=dict(user)
    del user_dict["id"]
    username = list(user.email.split("@"))[0]
    user_dict["username"]=username
    id = db_client.users.insert_one(user_dict).inserted_id
    new_user=supervisor_schema(db_client.users.find_one({"_id":id}))
    return Supervisor(**new_user)

#Edito un campo de un usuario en la BD
@router.put("/", response_model=Supervisor)
async def user(user:Supervisor,token:str = Depends(oauth2)):
    #Reviso Token
    pass_token(token)

    user_dict=dict(user)
    user_find=search_user("_id", ObjectId(user.id))
    username=user_find.username
    try:
        del user_dict["username"]
    except:
        pass
    del user_dict["id"]
    try:
        user_dict["username"]=username
        db_client.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
    except:
        return {"Error: No se a encontrado usuario"}
    
    return search_user("_id", ObjectId(user.id))

#Elimino un usuario de la BD
@router.delete("/{id}")
async def user(id: str,token:str = Depends(oauth2)):
    #Reviso Token
    pass_token(token)
    
    found=db_client.users.find_one_and_delete({"_id": ObjectId(id)})
    if not found:
        return {"Error: No se a encontrado usuario"}    

#Funcion para buscar usuario
def search_user(field:str, key):
    try:
        user = db_client.users.find_one({field:key})
        return Supervisor(**supervisor_schema(user))
    except:
        return {"Error: No se a encontrado usuario"}

#Funcion para ratificar token
def pass_token(token,correct_token=False):
    #Autentificacion token
    if not token:
        raise HTTPException(status_code=401, detail="Falta Token")
    search_token=db_client.tokens.find_one({"token":token})
    if search_token == None:
        raise HTTPException(status_code=401, detail="Token Incorrecto")
    correct_token=True
    return(correct_token)