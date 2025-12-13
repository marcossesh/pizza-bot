from fastapi import FastAPI

app = FastAPI(title="Pizza Bot API")

@app.get("/")
async def root():
    return {"message": "Pizza Bot API is running"}

@app.get("/health")
async def health():
    return {"status": "ok"}
