from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, ToolMessage

from app.database import init_db
from app.seed import seed_pizzas
from app.graph import graph
from app.logging_config import setup_logging

logger = setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up Pizza Bot API...")
    await init_db()
    await seed_pizzas()
    logger.info("Startup complete.")
    yield
    # Shutdown
    logger.info("Shutting down Pizza Bot API...")

app = FastAPI(title="Pizza Bot API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    thread_id: str = "default"

@app.get("/")
async def root():
    return {"message": "Pizza Bot API is running"}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        config = {"configurable": {"thread_id": request.thread_id}}
        
        input_message = HumanMessage(content=request.message)
        
        logger.info(f"Processing message from thread {request.thread_id}: {request.message}")
        response = await graph.ainvoke({"messages": [input_message]}, config=config)
        
        # Extract the last message content
        messages = response["messages"]
        last_message = messages[-1]
        final_content = last_message.content
        
        # if a tool message with "Cardápio" exists recently and the AI didn't repeat "Calabresa"
        if len(messages) >= 2:
            # Look backwards for the last tool message
            for msg in reversed(messages[:-1]):
                if isinstance(msg, ToolMessage) and "Cardápio" in str(msg.content):
                    if "Calabresa" not in str(final_content):
                        logger.info("Appending menu tool content to response")
                        final_content = f"{msg.content}\n\n{final_content}"
                    break
        
        logger.info(f"Response generated: {final_content}")
        
        return {"response": final_content}
        
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
