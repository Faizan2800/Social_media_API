from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str = "localhost"
    database_port: int = 5432
    database_password: str
    database_username: str = "postgres"
    database_name: str = "fastapi"
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    
    class Config:
        env_file = ".env"
        extra = "ignore"  # Critical to ignore system env vars like PATH

# Instantiate settings
settings = Settings()