from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt,JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from db.client import db_client
#Importo objetos de Supervisores
from db.models.supervisores import Supervisor
from db.schemas.supervisores import supervisor_schema, supervisores_schema
#Importo objetos de Psat
from db.models.psat import Psat
from db.schemas.psat import psat_schema, psats_schema
#Importo objetos de Administradores
from db.models.administradores import Admin
from db.schemas.administradores import administrador_schema, administradores_schema



ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 5
SECRET ="AASDASJFIMVIRNASOKDPOER"

#Dependencias a instalar
# pip install "python-jose[cryptography]"
# pip install "passlib[bcrypt]" (este es el algoritmo de encriptacion que usaremos)

router=APIRouter(prefix="/auth", tags=["auth"])
oauth2 = OAuth2PasswordBearer(tokenUrl="login")
crypt = CryptContext(schemes=["bcrypt"])


#Funcion para buscar usuario
def search_user_allDB(email:str):
        collections=db_client.list_collection_names()
        search_var=[]
        user=[]
        i=0
        while True:            
            collection=collections[i]
            try:
                if collection == "users":
                    user = db_client[collection].find_one({"email":email})
                    return [Supervisor(**supervisor_schema(user)),"Supervisor",collection]

                elif collection=="psats":
                    user = db_client[collection].find_one({"email":email})
                    return [Psat(**psat_schema(user)),"Psat",collection]
                    
                elif collection=="admin":
                    user = db_client[collection].find_one({"email":email})
                    return [Admin(**administrador_schema(user)),"Administrador",collection]
                else:
                    i+=1
            except:
                i+=1

            if i==5:
                return {"Usiario no esta registriado"}

#Endpoint de login
@router.post("/login")
async def login(form:OAuth2PasswordRequestForm = Depends()):
    user_found_list=search_user_allDB(form.username)
    user_found=user_found_list[0]
    user_type=user_found_list[1]
    user_collection=user_found_list[2]
    if not form.password==user_found.password:
        raise HTTPException(status_code=400, detail="La contraseña no es correcta")
    
    access_token_expiration=timedelta(minutes=ACCESS_TOKEN_DURATION)
    expire=datetime.utcnow() + access_token_expiration
    print(user_found)
    access_token={"sub":user_found.username, "exp":expire}

    #Actualizo token en registro de usuario
    db_client[user_collection].update_one(
        {"email": form.username},
        {"$set": {"token": str(jwt.encode(access_token,SECRET,algorithm=ALGORITHM)) }})
    
  #Actualizo token en registro de tokens
    db_client.tokens.find_one_and_delete({"usuario": form.username})
    token_dict={"usuario":user_found.email,"token":str(jwt.encode(access_token,SECRET,algorithm=ALGORITHM)),"perfil":user_type}
    db_client.tokens.insert_one(token_dict)

    return {"access_token": jwt.encode(access_token,SECRET,algorithm=ALGORITHM),"usuario":user_found.email,"perfil":user_type}
