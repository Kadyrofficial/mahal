from pydantic_settings import BaseSettings
from pydantic import BaseModel
from pathlib import Path
import os
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent


env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)


def str_to_bool(s: str | None) -> bool:
    return s is not None and s.lower() in ("true", "1", "yes", "y")


class DbSettings(BaseModel):
    user: str = os.getenv("DB_USER")
    password: str = os.getenv("DB_PASS")
    name: str = os.getenv("DB_NAME")
    port: str = os.getenv("DB_PORT")
    host: str = os.getenv("DB_HOST")
    echo: bool = str_to_bool(os.getenv("DB_ECHO"))
    
    @property
    def url(self):
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class EmailSettings(BaseModel):
    user: str = os.getenv("EMAIL_USER")
    password: str = os.getenv("EMAIL_PASS")
    port: int = os.getenv("EMAIL_PORT", 587)
    host: str = os.getenv("EMAIL_HOST")


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "public.pem"
    secret_key: str = str(os.getenv("TOKEN_SECRET_KEY"))
    algorithm: str = "HS256"
    otp_validity: int = 5 # in minutes
    token_validity: int = 365 # in days


class Settings(BaseSettings):
    db: DbSettings = DbSettings()
    email: EmailSettings = EmailSettings()
    auth_jwt: AuthJWT = AuthJWT()

settings = Settings()
