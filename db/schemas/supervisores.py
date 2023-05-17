def supervisor_schema(user) -> dict:
    return {"id": str(user["_id"]),
            "username": user["username"],
            "password": str(user["password"]),
            "email": user["email"],
            "nombre":str(user["nombre"]),
            "rut": str(user["rut"]),
            "psat_asignadas":list(user["psat_asignadas"]),
    }

def supervisores_schema(users) -> list:
    return [supervisor_schema(user) for user in users]