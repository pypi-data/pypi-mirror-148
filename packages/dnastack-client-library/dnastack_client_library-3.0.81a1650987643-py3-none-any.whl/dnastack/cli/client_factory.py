from imagination.decorator import service
from typing import Optional, Type

from dnastack.client.constants import SERVICE_CLIENT_CLASS, ALL_SERVICE_CLIENT_CLASSES
from dnastack.client.service_registry.client import ServiceRegistry
from dnastack.client.service_registry.factory import ClientFactory
from dnastack.configuration import ConfigurationManager, ServiceEndpoint, Configuration
from dnastack.helpers.logger import get_logger


class UnknownAdapterTypeError(RuntimeError):
    pass


class NoServiceRegistryError(RuntimeError):
    def __init__(self):
        super(NoServiceRegistryError, self).__init__('No service registry defined in the configuration')


@service.registered()
class ConfigurationBasedClientFactory:
    """
    Configuration-based Client Factory

    This class will provide a service client based on the CLI configuration.
    """

    def __init__(self, config_manager: ConfigurationManager):
        self._config_manager = config_manager
        self._logger = get_logger(type(self).__name__)

    def get(self,
            cls: Type[SERVICE_CLIENT_CLASS],
            endpoint_id: Optional[str] = None,
            endpoint_url: Optional[str] = None) -> SERVICE_CLIENT_CLASS:
        configuration = self._config_manager.load()
        endpoint = self.get_endpoint(configuration, cls, endpoint_id, endpoint_url)
        return cls.make(endpoint)

    def get_service_registry_client_factory(self) -> ClientFactory:
        clients = [
            ServiceRegistry.make(endpoint)
            for endpoint in self._config_manager.load().endpoints
            if endpoint.adapter_type == ServiceRegistry.get_adapter_type()
        ]

        if not clients:
            raise NoServiceRegistryError()

        return ClientFactory(clients)

    def get_endpoint(self,
                     configuration: Configuration,
                     cls: Type[SERVICE_CLIENT_CLASS],
                     endpoint_id: Optional[str] = None,
                     endpoint_url: Optional[str] = None,
                     create_default_if_missing: bool = False) -> ServiceEndpoint:
        adapter_type = cls.get_adapter_type()

        if endpoint_id:
            return configuration.get_endpoint(adapter_type,
                                              endpoint_id=endpoint_id,
                                              create_if_missing=create_default_if_missing)
        elif endpoint_url:
            return self.get_service_registry_client_factory().find_one_service_info(cls, endpoint_url)
        else:
            return configuration.get_default_endpoint(adapter_type)

    def get_client_class(self, adapter_type: str) -> Type[SERVICE_CLIENT_CLASS]:
        for cls in ALL_SERVICE_CLIENT_CLASSES:
            if adapter_type == cls.get_adapter_type():
                return cls
        raise UnknownAdapterTypeError(adapter_type)
