from pydantic import BaseModel
from typing import Optional

#Entidad users
class Token(BaseModel):
    id: Optional[str]
    username: Optional[str]
    token:str
    perfil: Optional[str]



