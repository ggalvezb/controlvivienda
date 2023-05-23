from fastapi import FastAPI
#from fastapi.staticfiles import StaticFiles
from routers import supervisores,psat,administradores,proyectos,auth_user,token
from fastapi.middleware.cors import CORSMiddleware

# Inicia el servidor: uvicorn main:app --reload

app=FastAPI()


#routers
app.include_router(supervisores.router)
app.include_router(psat.router)
app.include_router(administradores.router)
app.include_router(proyectos.router)
app.include_router(auth_user.router)
app.include_router(token.router)

#app.mount("/static", StaticFiles(directory="static"),name="static")

# Configurar los orígenes permitidos como '*'
origins = ["*"]

# Agregar el middleware CORS a la aplicación
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def root():
    return{"message":"Hello World"}