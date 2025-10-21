from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "change-me"  # set in env for prod
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ADMIN_SIGNUP_CODE: str = "letmein"  # simple bootstrap for manager user
    CORS_ORIGINS: str = "*"  # comma-separated in prod

    model_config = {"env_file": ".env"}  # pydantic v2 style


settings = Settings()
