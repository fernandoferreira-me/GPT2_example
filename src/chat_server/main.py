from fastapi import FastAPI
from .routers.chat import router as chat_router

app = FastAPI()

app.include_router(chat_router, prefix="/chat")

@app.get("/")
async def root():
    return {"message": "Hello World"}