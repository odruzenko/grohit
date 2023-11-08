import os
from pathlib import Path
from platformdirs import user_config_path

from typing import Optional, Any

from pydantic import Field
from pydantic.fields import FieldInfo
from pydantic_settings import BaseSettings, SettingsConfigDict, EnvSettingsSource


CONFIG_DIR = Path(os.getenv("GROHIT_CONFIG_DIR") or user_config_path("grohit"))


class ModifiedEnvSettingsSource(EnvSettingsSource):
    def prepare_field_value(
        self, field_name: str, field: FieldInfo, value: Any, value_is_complex: bool
    ) -> Any:
        try:
            print(field_name, field, value, value_is_complex)
            if value is None:
                return None

            return value
        except ValueError:
            return value.split(",")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="GROHIT_", env_file=".env")

    GRAFANA_URL: str = Field(
        description="Grafana URL", examples=["https://cloud.grafana.com"]
    )
    GRAFANA_API_KEY: Optional[str] = Field(description="Grafana API Key", default=None)
    GRAFANA_ORG_ID: Optional[str] = Field(
        description="Grafana Organization ID", default=None
    )
    GRAFANA_EXTRA_HEADERS: Optional[dict] = Field(
        description="Extra headers to include in requests to Grafana",
        default=None,
        examples=[],
    )

    # @classmethod
    # def settings_customise_sources(
    #    cls,
    #    settings_cls: type[BaseSettings],
    #    init_settings: PydanticBaseSettingsSource,
    #    env_settings: PydanticBaseSettingsSource,
    #    dotenv_settings: PydanticBaseSettingsSource,
    #    file_secret_settings: PydanticBaseSettingsSource,
    # ) -> tuple[PydanticBaseSettingsSource, ...]:
    #    return (init_settings, ModifiedEnvSettingsSource(settings_cls))


settings = Settings
