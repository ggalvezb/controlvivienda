from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from db.client import db_client
from db.models.token import Token
from db.schemas.token import token_schema, tokens_schema
from bson import ObjectId
from routers.auth_user import oauth2

router=APIRouter(prefix="/token",tags=["Tokens"])

#Funcion para buscar usuario
def search_token(field:str, key):
    try:
        user = db_client.tokens.find_one({field:key})
        return Token(**token_schema(user))
    except:
        return {"Error: No se a encontrado usuario"}

#Retorno un usuario en especifico
@router.get("/{token}")
async def user(token:str):

    return search_token("token", token)
