from traceback import format_exc
from typing import List, Any, Dict, Optional, Iterable, Type

from dnastack.client.base_client import BaseServiceClient
from dnastack.client.constants import SERVICE_CLIENT_CLASS
from dnastack.client.service_registry.client import ServiceRegistry
from dnastack.client.service_registry.models import ServiceType, Service
from dnastack.configuration.models import ServiceEndpoint
from dnastack.helpers.logger import get_logger


class UnsupportedClientClassError(RuntimeError):
    """ Raised when the given client class is not supported """

    def __init__(self, cls: Type):
        super(UnsupportedClientClassError, self).__init__(f'{cls.__module__}.{cls.__name__} is not supported')


class UnregisteredServiceEndpointError(RuntimeError):
    """ Raised when the requested service endpoint is not registered """
    def __init__(self, services: Iterable[Service]):
        alternative_endpoint_urls = ', '.join(sorted([
            f'{service.url} ({service.type.group}:{service.type.artifact}:{service.version})'
            for service in services
        ]))
        super(UnregisteredServiceEndpointError, self).__init__(
            f'Try alternative(s): {alternative_endpoint_urls}'
            if alternative_endpoint_urls
            else 'No alternatives'
        )


class ClientFactory:
    def __init__(self, registries: List[ServiceRegistry]):
        self.__logger = get_logger(type(self).__name__)
        self.__registries = registries

    def find_services(self,
                      url: Optional[str] = None,
                      types: Optional[List[ServiceType]] = None,
                      exact_match: bool = True) -> Iterable[Service]:
        """ Find GA4GH services """
        assert url or types, 'Either url or types must be defined.'

        self.__logger.debug(f'find_services: [url: {url}] [types: {types}] [exact_match: {exact_match}]')

        for registry in self.__registries:
            try:
                for service in registry.list_services():
                    if url:
                        if exact_match:
                            if service.url != url:
                                continue
                        else:
                            if not service.url.startswith(url):
                                continue

                    if types and not self._contain_type(service.type, types, exact_match):
                        continue

                    yield service
                # END FOR: registry.list_services()
            except Exception:
                self.__logger.warning(format_exc())
                self.__logger.warning(f'Due to unexpected error above, failed to list services from the registry at {registry.url}. Skipped.')
                continue
        # END FOR: self.__registries

    def find_one_service_info(self,
                              client_class: Type[SERVICE_CLIENT_CLASS],
                              service_endpoint_url: str) -> ServiceEndpoint:
        if issubclass(client_class, BaseServiceClient):
            types = client_class.get_supported_service_types()

            # Return the client of the first matched service endpoint.
            for service in self.find_services(service_endpoint_url, types):
                return self._parse_ga4gh_service_info(
                    client_class,
                    service
                )

            self.__logger.info(f'The service ({service_endpoint_url}) is not found in any known service registries.')
            self.__logger.debug(f'Failed to match types ({types})')

            # At this point, no service endpoints are exactly matched. Compile information for the error feedback.
            raise UnregisteredServiceEndpointError(self.find_services(service_endpoint_url, types, exact_match=False))
        else:
            raise UnsupportedClientClassError(client_class)

    def create(self, client_class: Type[SERVICE_CLIENT_CLASS], service_endpoint_url: str) -> SERVICE_CLIENT_CLASS:
        if issubclass(client_class, BaseServiceClient):
            return client_class.make(self.find_one_service_info(client_class, service_endpoint_url))
        else:
            raise UnsupportedClientClassError(client_class)

    @staticmethod
    def _contain_type(anchor: ServiceType, types: List[ServiceType], exact_match: bool) -> bool:
        if exact_match:
            return anchor in types
        else:
            for given_type in types:
                if anchor.group == given_type.group and anchor.artifact == given_type.artifact:
                    return True
            return False

    def _parse_ga4gh_service_info(self, client_class: Type, service: Service) -> ServiceEndpoint:
        if issubclass(client_class, BaseServiceClient):
            authentications = [
                self._parse_authentication_info(auth_info)
                for auth_info in (service.authentication or list())
            ]

            return ServiceEndpoint(
                model_version=2.0,
                id=service.id,
                adapter_type=client_class.get_adapter_type(),  # DEPRECATED in 3.0.66
                fallback_authentications=authentications,
                type=client_class.get_supported_service_types()[0],
                url=service.url,
            )
        else:
            raise UnsupportedClientClassError(client_class)

    @staticmethod
    def _parse_authentication_info(auth_info: Dict[str, Any]) -> Dict[str, Any]:
        return dict(
            type='oauth2',
            authorization_endpoint=auth_info.get('authorizationUrl'),
            client_id=auth_info.get('clientId'),
            client_secret=auth_info.get('clientSecret'),
            device_code_endpoint=auth_info.get('deviceCodeUrl'),
            grant_type=auth_info.get('grantType'),
            redirect_url=auth_info.get('redirectUrl'),
            resource_url=auth_info.get('resource'),
            scope=auth_info.get('scope'),
            token_endpoint=auth_info.get('accessTokenUrl'),
        )

    @classmethod
    def use(cls, *service_registry_urls: str):
        """
        .. note:: This only works with public registries.
        """
        return cls([ServiceRegistry(ServiceEndpoint(url=url)) for url in service_registry_urls])
