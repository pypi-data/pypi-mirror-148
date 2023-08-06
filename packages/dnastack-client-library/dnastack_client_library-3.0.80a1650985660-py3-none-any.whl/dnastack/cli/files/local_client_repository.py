from typing import Optional

from imagination import container

from dnastack.client.files_client import DrsClient
from dnastack.cli.client_factory import ConfigurationBasedClientFactory


class LocalClientRepository:
    # noinspection PyShadowingBuiltins
    @staticmethod
    def get(id: Optional[str] = None, url: Optional[str] = None) -> DrsClient:
        factory: ConfigurationBasedClientFactory = container.get(ConfigurationBasedClientFactory)
        return factory.get(DrsClient, id, url)