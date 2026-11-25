from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    
    DB_CONNECTION : str = "mysql"
    DB_HOST : str
    DB_PORT : str
    DB_DATABASE : str
    DB_USERNAME : str
    DB_PASSWORD : str = ""

    REDIS_HOST: str = "127.0.0.1"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()    