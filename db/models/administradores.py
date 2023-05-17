from pydantic import BaseModel
from typing import Optional

#Entidad admin
class Admin(BaseModel):
    id: Optional[str]
    username:Optional[str]
    email:str
    password: Optional[str]
    token: Optional[str]
    disable:Optional[bool]
    proyectos_asignados:list

