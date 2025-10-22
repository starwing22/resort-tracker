from pydantic import Field
import sys
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",             
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    # Define the expected env vars (no default = must be in .env)
    SECRET_KEY: str = Field(..., alias="SECRET_KEY")
    JWT_ALGORITHM: str = Field(..., alias="JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(..., alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    DATABASE_URL: str = Field(..., alias="DATABASE_URL")
    CORS_ORIGINS: str = Field(..., alias="CORS_ORIGINS")
    ADMIN_SIGNUP_CODE: str = Field(..., alias="ADMIN_SIGNUP_CODE")

settings = Settings()
