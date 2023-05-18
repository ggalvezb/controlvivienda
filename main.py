from fastapi import FastAPI
#from fastapi.staticfiles import StaticFiles
from routers import supervisores,psat,administradores,proyectos,auth_user

# Inicia el servidor: uvicorn main:app --reload

app=FastAPI()

#routers
app.include_router(supervisores.router)
app.include_router(psat.router)
app.include_router(administradores.router)
app.include_router(proyectos.router)
app.include_router(auth_user.router)

#app.mount("/static", StaticFiles(directory="static"),name="static")

@app.get("/")
async def root():
    return{"message":"Hello World"}