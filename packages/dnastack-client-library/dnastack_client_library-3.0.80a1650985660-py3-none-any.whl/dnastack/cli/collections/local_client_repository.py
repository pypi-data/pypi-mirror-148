from typing import Optional

from imagination import container

from dnastack.client.collections_client import CollectionServiceClient
from dnastack.cli.client_factory import ConfigurationBasedClientFactory


class LocalClientRepository:
    # noinspection PyShadowingBuiltins
    @staticmethod
    def get(id: Optional[str] = None, url: Optional[str] = None) -> CollectionServiceClient:
        factory: ConfigurationBasedClientFactory = container.get(ConfigurationBasedClientFactory)
        return factory.get(CollectionServiceClient, id, url)