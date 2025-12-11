from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "mongodb://localhost:27017"
    MONGO_INITDB_DATABASE: str = "assignment_master_db"
    SECRET_KEY: str = "supersecretkey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
