from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import get_settings
from routers import api_router

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/", tags=["Root"])
def read_root():
    """Retorna uma mensagem de boas-vindas."""
    return {"message": "Bem-vindo à API Adopt Pet!"}


@app.get("/health", tags=["Health Check"])
def health_check():
    """Verifica se a aplicação está funcionando."""
    return {"status": "ok"}
