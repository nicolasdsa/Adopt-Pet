# Em api/Dockerfile

# --- base com python + deps do sistema ---
FROM python:3.14-slim AS base
# A variável POETRY_VERSION não é usada se você instala com "pip install poetry"
# Vamos remover para evitar confusão.
ENV POETRY_VIRTUALENVS_IN_PROJECT=true \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends build-essential curl libpq-dev git \
  && rm -rf /var/lib/apt/lists/*

# Instala a versão mais recente do Poetry
RUN pip install --no-cache-dir poetry

WORKDIR /app

# Copie os arquivos de dependência, incluindo o lock file
COPY pyproject.toml poetry.lock ./

# Instala as dependências EXATAS do lock file, otimizando o cache do Docker
RUN poetry install --no-interaction --no-ansi --no-root

# Adiciona o venv do poetry ao PATH
ENV PATH="/app/.venv/bin:$PATH"

# Agora copie o código da aplicação
COPY . .

# A porta que a aplicação vai ouvir dentro do contêiner
EXPOSE 8000

# O CMD é um fallback, mas o comando do docker-compose tem prioridade
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]