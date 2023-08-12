import os
from pydantic import BaseSettings, SecretStr

class Settings(BaseSettings):
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: SecretStr
    DATABASE_HOSTNAME: str
    DATABASE_PORT: str
    DATABASE_NAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    PROJECT_NAME: str
    DEBUG: bool

    class Config:
        env_file = ".env"

    def __init__(self):
        super().__init__()
        if os.path.exists(self.Config.env_file):
            with open(self.Config.env_file) as f:
                for line in f:
                    key, value = line.split("=")
                    setattr(self, key.strip(), value.strip())
