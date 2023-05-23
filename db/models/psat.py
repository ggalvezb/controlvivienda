from pydantic import BaseModel
from typing import Optional

#Entidad psat
class Psat(BaseModel):
    id: Optional[str]
    username:Optional[str]
    email:str
    password: Optional[str]
    rut: str
    proyectos_asignados:Optional[list]
    token: Optional[str]
