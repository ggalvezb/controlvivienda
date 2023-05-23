from pydantic import BaseModel
from typing import Optional

#Entidad users
class Supervisor(BaseModel):
    id: Optional[str]
    username: Optional[str]
    nombre:str
    password: Optional[str]
    email:str
    rut: str
    psat_asignadas:list
    token: Optional[str]
