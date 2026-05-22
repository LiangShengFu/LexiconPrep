from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "LexiconPrep API"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = True

    DATABASE_URL: str = "postgresql+asyncpg://taylor566@localhost:5432/lexiconprep"
    REDIS_URL: str = ""

    JWT_SECRET_KEY: str = "change-me-in-production-use-a-real-secret"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    RATE_LIMIT_PER_MINUTE: int = 100
    ALLOWED_ORIGINS: str = ""

    model_config = {"env_file": ".env", "case_sensitive": True}


settings = Settings()
