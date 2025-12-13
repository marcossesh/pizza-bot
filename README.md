# Pizza Bot 🍕

Assistente virtual para pizzaria utilizando FastAPI, LangGraph, React e PostgreSQL.

## Pré-requisitos

- Docker e Docker Compose
- Chave de API Groq (ou compatível)

## Como Rodar

1. **Configuração**
   Copie o arquivo de exemplo e configure suas variáveis de ambiente:
   ```bash
   cp .env.example .env
   ```
   Edite o arquivo `.env` e adicione sua `GROQ_API_KEY`.

2. **Execução**
   Suba os containers:
   ```bash
   docker-compose up --build
   ```

3. **Acesso**
   - Frontend: [http://localhost:3000](http://localhost:3000)
   - Backend Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## Estrutura

- **Backend**: FastAPI + LangGraph (Python)
- **Frontend**: React + Vite (TypeScript)
- **Database**: PostgreSQL

## Funcionalidades

- Chat interativo
- Consulta de preços e ingredientes no banco de dados
- Simulação de pedido
