def administrador_schema(admin) -> dict:
    return {"id": str(admin["_id"]),
            "username": str(admin["username"]),
            "email": str(admin["email"]),
            "password": str(admin["password"]),
            "token": str(admin["token"]),
            "disable":bool(admin["disable"]),
            "proyectos_asignados":list(admin["proyectos_asignados"]),
    }

def administradores_schema(admins) -> list:
    return [administrador_schema(admin) for admin in admins]

