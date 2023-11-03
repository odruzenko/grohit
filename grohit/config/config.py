import os
from pathlib import Path
from platformdirs import user_config_path

from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


CONFIG_DIR = Path(os.getenv("GROHIT_CONFIG_DIR") or user_config_path("grohit"))


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="GROHIT_", env_file=".env")

    GRAFANA_URL: Optional[str] = Field(
        description="Grafana URL", examples=["https://cloud.grafana.com"]
    )
    GRAFANA_API_KEY: str = Field("Grafana API Key")
    GRAFANA_ORG_ID: str = Field("Grafana Organization ID")
    GRAFANA_EXTRA_HEADERS: str = Field(
        "Extra headers to include in requests to Grafana", examples=[]
    )


settings = Settings
