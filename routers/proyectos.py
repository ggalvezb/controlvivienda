from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from db.client import db_client
from db.models.proyectos import Proyecto
from db.schemas.proyectos import proyecto_schema, proyectos_schema
from bson import ObjectId
from routers.auth_user import oauth2

router=APIRouter(prefix="/proyectos",tags=["Proyectos"])


#Retorno todos los Usuarios
@router.get("/", response_model=list[Proyecto])
async def proyectos(token:str = Depends(oauth2)):
    #Reviso Token
    pass_token(token)
    return proyectos_schema(db_client.proyectos.find())


#Retorno un usuario en especifico
@router.get("/{id}")
async def proyecto(id:str,token:str = Depends(oauth2)):
    #Reviso Token
    pass_token(token)

    return search_proyecto("_id", ObjectId(id))

#Agrego un proyecto a la BD
@router.post("/")
async def proyecto(proyecto:Proyecto,token:str = Depends(oauth2)):
    #Reviso Token
    pass_token(token)

    if type(search_proyecto("CODIGO_PROYECTO",proyecto.CODIGO_PROYECTO)) == Proyecto:
        return {"El proyecto ya existe"}
    user_dict=dict(proyecto)
    del user_dict["id"]
    id = db_client.proyectos.insert_one(user_dict).inserted_id
    new_user=proyecto_schema(db_client.proyectos.find_one({"_id":id}))
    return Proyecto(**new_user)


#Edito un campo de un usuario en la BD
@router.put("/", response_model=Proyecto)
async def proyecto(proyecto:Proyecto,token:str = Depends(oauth2)):
    #Reviso Token
    pass_token(token)

    user_dict=dict(proyecto)
    del user_dict["id"]
    try:
        db_client.proyectos.find_one_and_replace({"_id": ObjectId(proyecto.id)}, user_dict)
    except:
        return {"Error: No se a encontrado usuario"}
    
    return search_proyecto("_id", ObjectId(proyecto.id))

#Elimino un usuario de la BD
@router.delete("/{id}")
async def proyecto(id: str,token:str = Depends(oauth2)):
    #Reviso Token
    pass_token(token)

    found=db_client.proyectos.find_one_and_delete({"_id": ObjectId(id)})
    if not found:
        return {"Error: No se a encontrado usuario"}    

#Funcion para buscar usuario
def search_proyecto(field:str, key):
    try:
        proyecto = db_client.proyectos.find_one({field:key})
        return Proyecto(**proyecto_schema(proyecto))
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