from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from db.client import db_client
from db.models.administradores import Admin
from db.schemas.administradores import administrador_schema, administradores_schema
from bson import ObjectId
from routers.auth_user import oauth2

router=APIRouter(prefix="/administradores",tags=["Administradores"])


#Solo prueba para conexión
@router.get("/test")
async def admin():
    return({"Hola Mundo!"})

#Retorno todos los Administradores
@router.get("/", response_model=list[Admin])
async def admin(token:str = Depends(oauth2)):
    #Autentificacion token
    if not token:
        raise HTTPException(status_code=401, detail="Falta Token")
    search_token=db_client.tokens.find_one({"token":token})
    if search_token == None:
        raise HTTPException(status_code=401, detail="Token Incorrecto")
    
    return administradores_schema(db_client.admin.find())

#Retorno un administrador en especifico
@router.get("/{id}")
async def admin(id:str,token:str = Depends(oauth2)):
    #Autentificacion token
    if not token:
        raise HTTPException(status_code=401, detail="Falta Token")
    search_token=db_client.tokens.find_one({"token":token})
    if search_token == None:
        raise HTTPException(status_code=401, detail="Token Incorrecto")

    return search_admin("_id", ObjectId(id))


#Agrego un administrador a la BD
@router.post("/")
async def admin(admin:Admin,token:str = Depends(oauth2)):
    #Autentificacion token
    if not token:
        raise HTTPException(status_code=401, detail="Falta Token")
    search_token=db_client.tokens.find_one({"token":token})
    if search_token == None:
        raise HTTPException(status_code=401, detail="Token Incorrecto")

    if type(search_admin("email",admin.email)) == Admin:
        return {"El usuario ya existe"}

    admin_dict=dict(admin)
    del admin_dict["id"]
    username = list(admin.email.split("@"))[0]
    admin_dict["username"]=username
    id = db_client.admin.insert_one(admin_dict).inserted_id
    new_user=administrador_schema(db_client.admin.find_one({"_id":id}))
    return Admin(**new_user)


#Edito un campo de un admin en la BD ##############
@router.put("/", response_model=Admin)
async def admin(admin:Admin,token:str = Depends(oauth2)):
    #Autentificacion token
    if not token:
        raise HTTPException(status_code=401, detail="Falta Token")
    search_token=db_client.tokens.find_one({"token":token})
    if search_token == None:
        raise HTTPException(status_code=401, detail="Token Incorrecto")
    
    admin_dict=dict(admin)
    admin_found=search_admin("_id", ObjectId(admin.id))
    username=admin_found.username
    password=admin_found.password
    try:
        del admin_dict["username"]
    except:
        pass
    del admin_dict["id"]

    try:
        admin_dict["username"]=username
        db_client.admin.find_one_and_replace({"_id": ObjectId(admin.id)}, admin_dict)
    except:
        return {"Error: No se a encontrado usuario"}
    
    return search_admin("_id", ObjectId(admin.id))


#Elimino un admin de la BD
@router.delete("/{id}")
async def admin(id: str,token:str = Depends(oauth2)):
    #Autentificacion token
    if not token:
        raise HTTPException(status_code=401, detail="Falta Token")
    search_token=db_client.tokens.find_one({"token":token})
    if search_token == None:
        raise HTTPException(status_code=401, detail="Token Incorrecto")
    
    found=db_client.admin.find_one_and_delete({"_id": ObjectId(id)})
    if not found:
        return {"Error: No se a encontrado usuario"}    



#Funcion para buscar usuario
def search_admin(field:str, key):
    try:
        admin = db_client.admin.find_one({field:key})
        return Admin(**administrador_schema(admin))
    except:
        return {"Error: No se a encontrado usuario"}