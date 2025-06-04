from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DB_PORT: str
    DB_HOST: str
    DB_ECHO: bool
    
    TOKEN_SECRET_KEY: str
    TOKEN_VALIDITY: int
    ALGORITHM: str

    EMAIL_HOST: str
    EMAIL_PORT: str
    EMAIL_USER: str
    EMAIL_PASS: str

    PAGINATION_LIMIT: int = 20

    OTP_VALIDITY: int = 5

    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    

    class Config:
        env_file = Path(__file__).resolve().parent.parent.parent / ".env"
        env_file_encoding = 'utf-8'


settings = Settings()
