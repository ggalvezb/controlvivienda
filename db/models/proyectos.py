from pydantic import BaseModel
from typing import Optional

#Entidad users
class Proyecto(BaseModel):
        id: Optional[str]
        AÑO_LLAMADO: str
        CAPITULO: str
        TIPOLOGIA: str
        CODIGO_PROYECTO: str
        COMUNA: str
        NOMBRE_PROYECTO: str
        NUMERO_FAMILIAS: str
        PSAT: str
        RUT_PSAT: str
        CONSTRUCTORA: str
        RUT_CONSTRUCTORA: str
        SUPERVISOR: str
        ESTADO_DE_PROYECTO: str
        AVANCE: str
        FECHA_INICIO_REAL: str
        FECHA_TERMINO_REAL: str
        MONTO_CONTRATO: str 
        MONTO_SUBSIDIO: str
        MONTO_AHORRO: str
        OBSERVACIONES_SUPERVISOR: str
        INICIO_PROGRAMADO: str
        TERMINO_PROGRAMADO: str

