from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.database import crear_tablas
from app.routes import chat, perfil, conceptos, juego, racha, goals, challenges, streak
import jwt
from app.config import SECRET_KEY, ALGORITHM

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

# Middleware para validar JWT en rutas protegidas
# @app.middleware("http")
# async def jwt_middleware(request: Request, call_next):
#     print(f"Request path: {request.url.path}")
#     # Definir rutas protegidas (todas bajo /api/)
#     if request.url.path.startswith("/api/"):
#         print("Protected route")
#         authorization = request.headers.get("Authorization")
#         if not authorization:
#             print("No authorization header")
#             raise HTTPException(status_code=401, detail="Token de autorización faltante")
#         try:
#             scheme, token = authorization.split()
#             if scheme.lower() != "bearer":
#                 raise HTTPException(status_code=401, detail="Esquema de autorización inválido")
#             payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#             # Opcional: agregar el usuario al request.state
#             request.state.user = payload.get("sub")
#         except jwt.PyJWTError as e:
#             print(f"JWT Error: {e}")
#             raise HTTPException(status_code=401, detail="Token inválido o expirado")
#         except ValueError as e:
#             print(f"Value Error: {e}")
#             raise HTTPException(status_code=401, detail="Formato de autorización inválido")
#         except Exception as e:
#             print(f"Unexpected Error: {e}")
#             raise HTTPException(status_code=500, detail="Error interno")
#     
#     response = await call_next(request)
#     return response

# Crear las tablas de la base de datos al iniciar
@app.on_event("startup")
async def startup():
    crear_tablas()
    print("Base de datos inicializada")

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
            "/api/rachas",
            "/api/streaks",
            "/api/goals",
            "/api/challenges"
        ],
        "chat_endpoints": [
            "GET /api/chat/ - Información del chat",
            "POST /api/chat/mensaje - Enviar mensaje (con historial)",
            "GET /api/chat/historial - Obtener historial",
            "DELETE /api/chat/historial - Limpiar historial"
        ],
        "goals_endpoints": [
            "POST /api/goals - Crear meta",
            "GET /api/goals - Listar metas",
            "GET /api/goals/{id} - Obtener meta",
            "PUT /api/goals/{id} - Actualizar meta",
            "DELETE /api/goals/{id} - Eliminar meta",
            "POST /api/goals/{id}/complete - Completar meta"
        ],
        "challenges_endpoints": [
            "POST /api/challenges - Crear desafío",
            "GET /api/challenges - Listar desafíos",
            "GET /api/challenges/{id} - Obtener desafío",
            "PUT /api/challenges/{id} - Actualizar desafío",
            "DELETE /api/challenges/{id} - Eliminar desafío",
            "POST /api/challenges/generate-personalized - Generar retos personalizados"
        ],
        "streaks_endpoints": [
            "GET /api/streaks - Obtener racha del usuario",
            "POST /api/streaks/update - Actualizar racha (acción completada)",
            "POST /api/streaks/track - Registrar interacción diaria",
            "PUT /api/streaks/update - Actualizar racha manualmente",
            "POST /api/streaks/reset - Reiniciar racha",
            "GET /api/streaks/stats - Obtener estadísticas detalladas"
        ]
    }

# Incluir las rutas de cada módulo
app.include_router(chat, prefix="/api/chat", tags=["Chat"])
app.include_router(perfil, prefix="/api/perfil", tags=["Perfil"])
app.include_router(conceptos, prefix="/api/conceptos", tags=["Conceptos"])
app.include_router(juego, prefix="/api/juego", tags=["Juego"])
app.include_router(racha, prefix="/api/rachas", tags=["Rachas"])
app.include_router(streak, prefix="/api/streaks", tags=["Streaks"])
app.include_router(goals, prefix="/api/goals", tags=["Goals"])
app.include_router(challenges, prefix="/api/challenges", tags=["Challenges"])

# Para ejecutar: uvicorn app.main:app --reload
