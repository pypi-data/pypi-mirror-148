from typing import Optional

from imagination import container

from dnastack.client.dataconnect_client import DataConnectClient
from dnastack.cli.client_factory import ConfigurationBasedClientFactory


class LocalClientRepository:
    # noinspection PyShadowingBuiltins
    @staticmethod
    def get(id: Optional[str] = None, url: Optional[str] = None) -> DataConnectClient:
        factory: ConfigurationBasedClientFactory = container.get(ConfigurationBasedClientFactory)
        return factory.get(DataConnectClient, id, url)