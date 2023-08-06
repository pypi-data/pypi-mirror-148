from typing import Iterable, List, TypeVar
from urllib.parse import urljoin

from dnastack.client.base_client import BaseServiceClient
from dnastack.client.collections_client import CollectionServiceClient
from dnastack.client.dataconnect_client import DataConnectClient
from dnastack.client.files_client import DrsClient
from dnastack.client.service_registry.models import Service, ServiceType
from dnastack.configuration.models import ServiceEndpoint

SERVICE_CLIENT_CLASS = TypeVar('SERVICE_CLIENT_CLASS', CollectionServiceClient, DataConnectClient, DrsClient)
STANDARD_SERVICE_REGISTRY_TYPE_V1_0 = ServiceType(group='org.ga4gh', artifact='service-registry', version='1.0.0')


class ServiceListingError(RuntimeError):
    """ Raised when the service listing encounters error """


class ServiceRegistry(BaseServiceClient):
    def __init__(self, endpoint: ServiceEndpoint):
        if not endpoint.url.endswith('/'):
            endpoint.url = endpoint.url + r'/'

        super().__init__(endpoint)

    @staticmethod
    def get_adapter_type() -> str:
        return 'registry'

    @staticmethod
    def get_supported_service_types() -> List[ServiceType]:
        return [
            STANDARD_SERVICE_REGISTRY_TYPE_V1_0,
        ]

    def list_services(self) -> Iterable[Service]:
        with self.create_http_session() as session:
            response = session.get(urljoin(self._endpoint.url, 'services'))
            if response.ok:
                for raw_service in response.json():
                    yield Service(**raw_service)
            else:
                raise ServiceListingError(response)
