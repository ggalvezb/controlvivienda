def token_schema(user) -> dict:
    return {"id": str(user["_id"]),
            "username": user["usuario"],
            "token": str(user["token"]),
            "perfil": user["perfil"],
            }


def tokens_schema(users) -> list:
    return [token_schema(user) for user in users]
