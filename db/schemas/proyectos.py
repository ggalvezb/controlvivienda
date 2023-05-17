def proyecto_schema(user) -> dict:
    return {
        "id": str(user["_id"]),
        "AÑO_LLAMADO": str(user["AÑO_LLAMADO"]),
        "CAPITULO": str(user["CAPITULO"]),
        "TIPOLOGIA": str(user["TIPOLOGIA"]),
        "CODIGO_PROYECTO": str(user["CODIGO_PROYECTO"]),
        "COMUNA": str(user["COMUNA"]),
        "NOMBRE_PROYECTO": str(user["NOMBRE_PROYECTO"]),
        "NUMERO_FAMILIAS": str(user["NUMERO_FAMILIAS"]),
        "PSAT": str(user["PSAT"]),
        "RUT_PSAT": str(user["RUT_PSAT"]),
        "CONSTRUCTORA": str(user["CONSTRUCTORA"]),
        "RUT_CONSTRUCTORA": str(user["RUT_CONSTRUCTORA"]),
        "SUPERVISOR": str(user["SUPERVISOR"]),
        "ESTADO_DE_PROYECTO": str(user["ESTADO_DE_PROYECTO"]),
        "AVANCE": str(user["AVANCE"]),
        "FECHA_INICIO_REAL": str(user["FECHA_INICIO_REAL"]),
        "FECHA_TERMINO_REAL": str(user["FECHA_TERMINO_REAL"]),
        "MONTO_CONTRATO": str(user["MONTO_CONTRATO"]),
        "MONTO_SUBSIDIO": str(user["MONTO_SUBSIDIO"]),
        "MONTO_AHORRO": str(user["MONTO_AHORRO"]),
        "OBSERVACIONES_SUPERVISOR": str(user["OBSERVACIONES_SUPERVISOR"]),
        "INICIO_PROGRAMADO": str(user["INICIO_PROGRAMADO"]),
        "TERMINO_PROGRAMADO": str(user["TERMINO_PROGRAMADO"])
    }

def proyectos_schema(users) -> list:
    return [proyecto_schema(user) for user in users]