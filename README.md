# Adopt-Pet 🐾

Sistema de auxílio para ONGs de animais, com:
- **Frontend**: Next.js (App Router, TypeScript opcional, Tailwind)
- **Backend**: FastAPI (Python 3.14+, Poetry), SQLAlchemy, Alembic
- **Banco**: PostgreSQL
- **Containerização**: Docker Compose

## Sumário
- [Arquitetura](#arquitetura)
- [Pré-requisitos](#pré-requisitos)
- [Primeira execução (Docker)](#primeira-execução-docker)

## Arquitetura
- `web` (Next.js): UI, páginas, componentes e chamadas à API.
- `api` (FastAPI): rotas REST, regras de negócio, ORM, migrações.
- `db` (Postgres): persistência de dados.

---

## Comunicação:
- web (http://localhost:3000) → api (http://localhost:8000) → db (postgres://)

---

## Pré-requisitos
- **Docker** e **Docker Compose** instalados.
- (Opcional, para rodar localmente sem Docker)
  - **Node.js** LTS (18/20/22) + **npm**.
  - **Python 3.14+** e **Poetry**.
- (Se estiver no Windows) Use **WSL2** e rode os comandos **dentro do WSL**.

---

## Primeira execução (Docker)

1. **Clone** o repositório e entre na raiz:
   ```bash
   git clone <URL_DO_REPO>
   cd <PASTA_DO_REPO>
   ```
2. Crie o arquivo .env na raiz (ou copie de .env.example, se existir):
   ```bash
   # FRONTEND
    NEXT_PUBLIC_API_URL=http://localhost:8000
   # BACKEND (exemplos)
    JWT_SECRET=change-me
    JWT_EXPIRE_MINUTES=60
   ```
3. Suba os serviços:
   ```bash
   docker compose up --build
   ```

4. Acesse:
<ul>
<li>Frontend: http://localhost:3000</li>
<li>API Health: http://localhost:8000/health</li>
</ul>

