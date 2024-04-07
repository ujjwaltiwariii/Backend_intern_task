from pydantic_settings import BaseSettings
from functools import lru_cache
import os
import logging


logger = logging.getLogger('uvicorn.info')
logger.setLevel(logging.INFO)


class config(BaseSettings):
    app_name: str = "Backend Intern Hiring Task"
    version: str = "1.0.0"
    Admin_email: str = "admin@lms.com"

    class Config:
        extra = "allow"
        env_file = os.getenv('ENV_FILE', '.env')


settings = config()


@lru_cache
def get_settings():
    return settings
