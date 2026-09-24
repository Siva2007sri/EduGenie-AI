import os
from functools import lru_cache

from dotenv import load_dotenv


load_dotenv()


class Settings:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv(
        "GEMINI_MODEL",
        "gemini-2.5-flash"
    )

    EXPLANATION_PROVIDER: str = os.getenv(
        "EXPLANATION_PROVIDER",
        "gemini"
    )

    LOCAL_EXPLANATION_MODEL: str = os.getenv(
        "LOCAL_EXPLANATION_MODEL",
        "MBZUAI/LaMini-Flan-T5-783M"
    )

    APP_NAME: str = os.getenv(
        "APP_NAME",
        "EduGenie"
    )

    MAX_INPUT_CHARS: int = int(
        os.getenv("MAX_INPUT_CHARS", "30000")
    )

    HOST: str = os.getenv(
        "HOST",
        "127.0.0.1"
    )

    PORT: int = int(
        os.getenv("PORT", "8000")
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()