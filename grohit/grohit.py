from grohit.config.config import Settings
from grohit.grafana.client import GrafanaClient
from grohit.registry.plugins import RegistryPluginManager
from grohit.registry.registry import GrohitRegistry
from grohit.grafana.uploader import GrafanaUploader


class Grohit:
    def __init__(self, config: Settings):
        self.config = config
        self._grafana_client = GrafanaClient(
            config.GRAFANA_URL, extra_headers=config.GRAFANA_EXTRA_HEADERS
        )
        self._grafana_uploader = GrafanaUploader(self._grafana_client)
        self._registry = GrohitRegistry()
        self._plugin_manager = RegistryPluginManager(self._registry)
        self._plugin_manager.load_plugins()

    @property
    def grafana_url(self) -> str:
        return self.config.GRAFANA_URL

    @property
    def grafana_client(self) -> GrafanaClient:
        return self._grafana_client

    @property
    def grafana_uploader(self) -> GrafanaUploader:
        return self._grafana_uploader

    @property
    def registry(self) -> GrohitRegistry:
        return self._registry
