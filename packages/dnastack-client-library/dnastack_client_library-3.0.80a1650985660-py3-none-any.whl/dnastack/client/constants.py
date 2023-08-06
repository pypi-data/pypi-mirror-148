from typing import TypeVar

from dnastack.client.collections_client import CollectionServiceClient
from dnastack.client.dataconnect_client import DataConnectClient
from dnastack.client.files_client import DrsClient
from dnastack.client.service_registry.client import ServiceRegistry

# All known client classes
ALL_SERVICE_CLIENT_CLASSES = (CollectionServiceClient, DataConnectClient, DrsClient, ServiceRegistry)

# All client classes for data access
DATA_SERVICE_CLIENT_CLASSES = (CollectionServiceClient, DataConnectClient, DrsClient)


SERVICE_CLIENT_CLASS = TypeVar('SERVICE_CLIENT_CLASS', CollectionServiceClient, DataConnectClient, DrsClient,
                               ServiceRegistry)