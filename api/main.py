from fastapi import FastAPI

from core.config import get_settings
from routers import api_router

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
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
