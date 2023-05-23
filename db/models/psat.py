from pydantic import BaseModel
from typing import Optional

#Entidad psat
class Psat(BaseModel):
    id: Optional[str]
    nombre:str
    email:str
    password: Optional[str]
    rut: str
    proyectos_asignados:list
    token: Optional[str]
