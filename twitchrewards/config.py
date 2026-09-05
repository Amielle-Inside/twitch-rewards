"""Reads configuration from files at the project's (e,g, '.env.local').'"""

import os

from pydantic_settings import BaseSettings, SettingsConfigDict


def get_config_dict(env_file: str) -> SettingsConfigDict:
    """
    Return settings set in a given file.

    Parameters:
        env_file (str): Path to the configuration file.

    Returns:
        SettingsConfigDict: Dictionary with the settings in the configuration file.

    Raises:
        ValueError: If the environment is invalid.
    """

    return SettingsConfigDict(
        env_file=env_file, env_file_encoding="utf-8", case_sensitive=True
    )


class Settings(BaseSettings):
    """Base class for environment specific settings."""

    model_config = get_config_dict(".env")

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: str
    POSTGRES_HOST: str
    POSTGRES_DB: str

    SSL_KEY_PATH: str
    SSL_CERTIFICATE_PATH: str

    JWT_ENCODING_KEY: str
    JWT_ENCODING_ALGORITHM: str
    JWT_EXPIRATION_TIME_IN_SECONDS: int

    TWITCH_APP_CLIENT_ID: str
    TWITCH_APP_CLIENT_SECRET: str

    APP_HOST: str
    APP_PORT: int


class LocalSettings(Settings):
    """Settings for the local environment."""

    ENV: str = "local"


class ProdSettings(Settings):
    """Settings for the prod environment."""

    ENV: str = "prod"


def get_settings(env: str = "local") -> Settings:
    """
    Return the settings object based on the environment.

    Parameters:
        env (str): The environment to retrieve the settings for. Defaults to "dev".

    Returns:
        Settings: The settings object based on the environment.

    Raises:
        ValueError: If the environment is invalid.
    """
    if env.lower() == "local":
        return LocalSettings()  # type: ignore
    if env.lower() == "prod":
        return ProdSettings()  # type: ignore
    raise ValueError("Invalid environment. Must be 'dev' or 'test' ,'local'.")


_env = os.environ.get("ENV", "local")

settings = get_settings(_env)
