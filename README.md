# Pizza Bot

## Visão Geral do Projeto

O Pizza Bot é um assistente virtual inteligente projetado para gerenciar pedidos de pizza. Ele utiliza uma stack moderna combinando um backend em FastAPI, um agente de IA baseado em LangGraph e um frontend em React. O sistema oferece uma interface de conversação persistente, consultas de cardápio em tempo real e gerenciamento de pedidos sensível ao contexto.

### Principais Funcionalidades

-   **Agente Inteligente**: Alimentado por LangGraph e Llama 3.3 (via Groq), capaz de entender linguagem natural, inferir contexto (ex: "adicione uma" refere-se à última pizza mencionada) e gerenciar o estado da conversa.
-   **Backend Robusto**: Construído com FastAPI, apresentando operações de banco de dados assíncronas com SQLModel e asyncpg.
-   **Frontend Interativo**: Uma interface de chat baseada em React com atualizações em tempo real, indicadores de digitação e persistência de mensagens.
-   **Gerenciamento de Estado**: Persistência de estado em memória garante a continuidade da conversa dentro de uma sessão.
-   **Dockerizado**: Ambiente totalmente containerizado para implantação consistente.

## Arquitetura

O projeto segue uma arquitetura limpa e modular:

-   **Frontend**: React + Vite. Gerencia a interação do usuário, exibe o histórico do chat e comunica-se com o backend via API REST.
-   **Backend**: FastAPI. Expõe o endpoint `/chat`.
    -   **Graph**: Define o fluxo de trabalho do agente de IA usando LangGraph (StateGraph).
    -   **Tools**: Funções especializadas (`get_menu`, `add_to_order`, `get_pizza_price`) que o agente pode invocar.
    -   **Database**: PostgreSQL. Armazena dados de pizzas e potencialmente histórico de pedidos (extensível).
-   **Infraestrutura**: Docker Compose orquestra os serviços `frontend`, `backend` e `db`.

## Pré-requisitos

Certifique-se de que os seguintes itens estejam instalados em seu sistema:

-   **Docker**: v20.10+
-   **Docker Compose**: v2.0+
-   **Chave de API Groq**: Necessária para o LLM. Obtenha uma em [console.groq.com](https://console.groq.com).

## Início Rápido

Fornecemos um script de configuração automatizado para você começar rapidamente.

1.  **Clone o repositório**:
    ```bash
    git clone https://github.com/marcossesh/pizza-bot
    cd pizza-bot
    ```

2.  **Execute o script de configuração**:
    ```bash
    ./setup.sh
    ```
    Este script irá:
    -   Verificar dependências.
    -   Criar o arquivo `.env` a partir do `.env.example` (se estiver faltando).
    -   Construir e iniciar os containers.

3.  **Configure a Chave de API**:
    Abra o arquivo `.env` e cole sua chave de API Groq:
    ```env
    GROQ_API_KEY=sua_chave_api_aqui
    ```

4.  **Reinicie**:
    Se você modificou o `.env` após a execução do script, reinicie os containers:
    ```bash
    docker-compose restart backend
    ```

5.  **Acesse a Aplicação**:
    Abra [http://localhost:3000](http://localhost:3000) no seu navegador.

## Instalação Manual

Se preferir configurar o ambiente manualmente:

1.  **Configuração de Ambiente**:
    Copie o arquivo de exemplo de ambiente:
    ```bash
    cp .env.example .env
    ```
    Edite o `.env` e defina sua `GROQ_API_KEY`.

2.  **Construir e Executar**:
    ```bash
    docker-compose up --build
    ```

## Solução de Problemas (Troubleshooting)

### Erros de Conexão com o Banco de Dados
Se o backend falhar ao conectar ao banco de dados na inicialização:
-   Certifique-se de que o container `db` esteja saudável (`docker-compose ps`).
-   Verifique os logs: `docker-compose logs db`.
-   O backend está configurado para aguardar o banco de dados, mas latência extrema pode causar timeouts. Reiniciar o backend geralmente resolve isso.

### LLM Não Responde
-   Verifique sua `GROQ_API_KEY` no `.env`.
-   Verifique os logs do backend para erros de API: `docker-compose logs backend`.

### Conexão Recusada no Frontend
-   Certifique-se de que o backend esteja rodando na porta 8000.
-   Verifique se o container do frontend consegue alcançar o backend (a configuração de rede no `docker-compose.yml` cuida disso automaticamente).

## Desenvolvimento

-   **Logs do Backend**: `docker-compose logs -f backend`
-   **Logs do Frontend**: `docker-compose logs -f frontend`
-   **Acesso ao Banco de Dados**: Conecte via `localhost:5432` (Usuário: `postgres`, Senha: `password`, DB: `pizzabot`).

---
*Marcos Vinicius Ramos da Luz*

*Desenvolvido como parte do Desafio de Desenvolvedor Python.*
