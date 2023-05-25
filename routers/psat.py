from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from db.client import db_client
from db.models.psat import Psat
from db.schemas.psat import psat_schema, psats_schema
from bson import ObjectId
from routers.auth_user import oauth2



router=APIRouter(prefix="/psats",tags=["PSAT"])


#Retorno todos las Psats
@router.get("/", response_model=list[Psat])
async def psats(token:str = Depends(oauth2)):
    #Reviso Token
    pass_token(token)

    return psats_schema(db_client.psats.find())


#Retorno una PSAT en especifico
@router.get("/{id}")
async def psat(id:str,token:str = Depends(oauth2)):
    #Reviso Token
    pass_token(token)

    return search_psat("_id", ObjectId(id))


#Agrego una psat a la BD   
@router.post("/")
async def psat(psat:Psat,token:str = Depends(oauth2)):
    #Reviso Token
    pass_token(token)

    if type(search_psat("email",psat.email)) == Psat:
        return {"El usuario ya existe"}
    psat_dict=dict(psat)
    del psat_dict["id"]
    username = list(psat.email.split("@"))[0]
    psat_dict["username"]=username
    id = db_client.psats.insert_one(psat_dict).inserted_id  
    new_psat=psat_schema(db_client.psats.find_one({"_id":id}))
    return Psat(**new_psat)


#Edito un campo de una psat en la BD
@router.put("/", response_model=Psat)
async def psat(psat:Psat,token:str = Depends(oauth2)):
    #Reviso Token
    pass_token(token)

    user_dict=dict(psat)
    psat_find=search_psat("email", psat.email)
    username=psat_find.username
    del user_dict["id"]
    del user_dict["username"]
    try:
        user_dict["username"]=username
        db_client.psats.find_one_and_replace({"email": psat.email}, user_dict)
    except:
        return {"Error: No se a encontrado usuario"}
    return search_psat("email", psat.email)


#Elimino un psat de la BD
@router.delete("/{id}")
async def psat(id: str,token:str = Depends(oauth2)):
    #Reviso Token
    pass_token(token)

    found=db_client.psats.find_one_and_delete({"_id": ObjectId(id)})
    if not found:
        return {"Error: No se a encontrado usuario"}    


#Funcion para buscar psat
def search_psat(field:str, key):
    try:
        psat = db_client.psats.find_one({field:key})
        return Psat(**psat_schema(psat))
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
