"""General configuration.

Config: Bot Config
"""

# ruff: noqa: ARG003
import logging
import sys
from pathlib import Path
from typing import Annotated

from pydantic import ValidationError, field_validator
from pydantic.networks import UrlConstraints
from pydantic_core import MultiHostUrl
from pydantic_settings import (
    BaseSettings,
    DotEnvSettingsSource,
    EnvSettingsSource,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)
from pydantic_settings.sources import SettingsError
from typing_extensions import TypedDict

MongoSRVDsn = Annotated[MultiHostUrl, UrlConstraints(allowed_schemes=["mongodb+srv"])]
BASE_PATH = Path(__file__).parent.parent


class ChannelInfo(TypedDict):
    is_private: bool
    invite_link: str
    channel_id: int


class Config(BaseSettings):
    """A general configuration setup to read either .env or environment keys."""

    # Bot deploy config
    PORT: int = 8080
    HOSTNAME: str = "0.0.0.0"  # noqa: S104
    HTTP_SERVER: bool = True

    API_ID: int = "22012880"
    API_HASH: str = "5b0e07f5a96d48b704eb9850d274fe1d"
    BOT_TOKEN: str = "7879292880:AAH1xJPBet9uBwhnI8o-AZzynRpzIjVwatY"
    BOT_WORKER: int = 8
    BOT_SESSION: str = "Zaws-File-Share"
    BOT_MAX_MESSAGE_CACHE_SIZE: int = 100

    MONGO_DB_URL: MongoSRVDsn = "mongodb+srv://uramit0001:EZ1u5bfKYZ52XeGT@cluster0.qnbzn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    MONGO_DB_NAME: str = "Zaws-File-Share-testing"

    # Bot main config
    RATE_LIMITER: bool = True
    BACKUP_CHANNEL: int = "-1002439464108"
    ROOT_ADMINS_ID: list[int] = [6803505727,827932553]
    PRIVATE_REQUEST: bool = True
    PROTECT_CONTENT: bool = True
    FORCE_SUB_CHANNELS: list[int] = [-1002468887113,-1002452444734]
    AUTO_GENERATE_LINK: bool = True

    # Injected Config
    channels_n_invite: dict[str, ChannelInfo] = {}

    model_config = SettingsConfigDict(
        env_file=f"{BASE_PATH}/.env",
    )

    @field_validator("ROOT_ADMINS_ID", "FORCE_SUB_CHANNELS", mode="before")
    @classmethod
    def convert_int_to_list(cls, value: int | list[int]) -> list[int]:
        if isinstance(value, int):
            return [value]
        return value

    @field_validator("channels_n_invite", mode="before")
    @classmethod
    def ignore_keys(cls, value: dict[str, ChannelInfo]) -> dict[str, ChannelInfo]:
        return {}

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            DotEnvSettingsSource(settings_cls),
            EnvSettingsSource(settings_cls),
        )


try:
    config = Config()  # type: ignore[reportCallIssue]
except (ValidationError, SettingsError):
    logging.exception("Configuration Error")
    sys.exit(1)
