from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import auth, models, database

app = FastAPI()

# Habilitar CORS (útil para el frontend React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear tablas si no existen
models.Base.metadata.create_all(bind=database.engine)

# Incluir las rutas de login/register/protegidas
app.include_router(auth.router, prefix="/api")
