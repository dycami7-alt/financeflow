from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import crear_tablas
from app.routes import chat, perfil, conceptos, juego, racha

# Crear la aplicación FastAPI
app = FastAPI(
    title="FinanceFlow API",
    description="API para tu asistente financiero inteligente",
    version="1.0.0"
)

# Configurar CORS para que el frontend pueda conectarse
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar el dominio exacto
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear las tablas de la base de datos al iniciar
@app.on_event("startup")
async def startup():
    crear_tablas()
    print("✅ Base de datos inicializada")

# Ruta de bienvenida
@app.get("/")
async def inicio():
    return {
        "mensaje": "¡Bienvenido a FinanceFlow API! 🚀",
        "version": "1.0.0",
        "endpoints": [
            "/api/chat",
            "/api/perfil",
            "/api/conceptos",
            "/api/juego",
            "/api/rachas"
        ]
    }

# Incluir las rutas de cada módulo
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(perfil.router, prefix="/api/perfil", tags=["Perfil"])
app.include_router(conceptos.router, prefix="/api/conceptos", tags=["Conceptos"])
app.include_router(juego.router, prefix="/api/juego", tags=["Juego"])
app.include_router(racha.router, prefix="/api/rachas", tags=["Rachas"])

# Para ejecutar: uvicorn app.main:app --reloads
