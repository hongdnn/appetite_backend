from fastapi import FastAPI
from controllers import api_router
from src.infrastructure.config import Config


app = FastAPI(
    title=Config.APP_NAME,
    debug=Config.DEBUG
)
app.include_router(api_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Appetite backend server is running!"}