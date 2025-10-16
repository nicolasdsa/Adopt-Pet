# Em api/app/main.py
from fastapi import FastAPI

app = FastAPI(
    title='Adopt Pet API',
    version='0.1.0',
)

@app.get('/', tags=['Root'])
def read_root():
    """Retorna uma mensagem de boas-vindas."""
    return {'message': 'Bem-vindo à API Adopt Pet!'}

@app.get('/health', tags=['Health Check'])
def health_check():
    """Verifica se a aplicação está funcionando."""
    return {'status': 'ok'}