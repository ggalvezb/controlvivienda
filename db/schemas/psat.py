def psat_schema(psat) -> dict:
    return {"id": str(psat["_id"]),
            "email": str(psat["email"]),
            "nombre":str(psat["nombre"]),
            "rut": str(psat["rut"]),
            "proyectos_asignados":list(psat["proyectos_asignados"]),
            "password": str(psat["password"])
    }

def psats_schema(psats) -> list:
    return [psat_schema(psat) for psat in psats]

