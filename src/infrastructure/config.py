import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    APP_NAME = os.getenv('APP_NAME')
    DATABASE_URL = os.getenv('DATABASE_URL')
    DEBUG = os.getenv('ENV', 'dev') == 'dev'
    FOOD_DATASET_PATH = os.getenv('FOOD_DATASET_PATH')
    SECRET_KEY = os.getenv('SECRET_KEY')
    ALGORITHM = os.getenv('ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
    BUCKET_URL = os.getenv('BUCKET_URL')
    API_BASE_URL = os.getenv('API_BASE_URL')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    AGENT_AUTH_TOKEN = os.getenv('AGENT_AUTH_TOKEN')