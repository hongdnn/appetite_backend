import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from controllers import api_router
from src.infrastructure.config import Config
from src.llm_model.agent_manager import chat_agent_manager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    asyncio.create_task(chat_agent_manager.start_cleanup_task())
    yield
    # Optional shutdown logic (e.g. await cleanup)

app = FastAPI(
    title=Config.APP_NAME,
    debug=Config.DEBUG,
    lifespan=lifespan
)

app.include_router(api_router, prefix="/api")

@app.get("/")
def root(): 
    return {"message": "Appetite backend server is running!"}
