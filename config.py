from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings from env."""

    # SMTP email settings for sending emails
    SMTP_EMAIL: str
    SMTP_PASSWORD: SecretStr
    SMTP_HOST: str
    SMTP_PORT: int


# Creating an instance of the Settings class to avoid env reprocessing
settings = Settings()  # type: ignore
