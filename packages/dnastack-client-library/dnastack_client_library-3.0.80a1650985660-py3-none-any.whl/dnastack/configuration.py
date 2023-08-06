import hashlib
import json
import os
import shutil
from typing import List, Optional, Dict, Union, Any
from uuid import uuid4

import yaml
from imagination.decorator import service, EnvironmentVariable
from pydantic import BaseModel

from dnastack.constants import CLI_DIRECTORY
from dnastack.helpers.logger import get_logger


class ConfigurationModelMixin:
    def get_content_hash(self):
        # noinspection PyUnresolvedReferences
        return ConfigurationModelMixin.hash(self.dict(exclude_none=True))

    @staticmethod
    def hash(content):
        raw_config = json.dumps(content, sort_keys=True)
        h = hashlib.new('sha256')
        h.update(raw_config.encode('utf-8'))
        return h.hexdigest()


class OAuth2Authentication(BaseModel, ConfigurationModelMixin):
    """OAuth2 Authentication Information"""
    authorization_endpoint: Optional[str]
    client_id: Optional[str]
    client_secret: Optional[str]
    device_code_endpoint: Optional[str]
    grant_type: str
    personal_access_endpoint: Optional[str]
    personal_access_email: Optional[str]
    personal_access_token: Optional[str]
    redirect_url: Optional[str]
    resource_url: str
    scope: Optional[str]
    token_endpoint: Optional[str]
    type: str = 'oauth2'


# This is an alias for alternative spelling.
Oauth2Authentication = OAuth2Authentication


class AwsAuthentication(BaseModel, ConfigurationModelMixin):
    """Authentication Information with AWS"""
    access_key_id: str
    access_key_secret: str
    host: str
    region: str
    service: str = "execute-api"
    token: Optional[str]
    type: str = 'aws-sigv4'

    @classmethod
    def make(cls, **kwargs):
        ...  # Preparation for the change to generalize Authentication.


class Authentication(BaseModel, ConfigurationModelMixin):
    """Authentication Information"""
    aws: Optional[AwsAuthentication]
    oauth2: Optional[Oauth2Authentication]


class ServiceEndpoint(BaseModel, ConfigurationModelMixin):
    """API Service Endpoint"""
    model_version = 1.0
    """
    Service Endpoint Configuration Specification Version
    
    Changelogs in model version 2.0:
    - authentication and fallback_authentications will be now mapped as dictionary.
    """

    id: str = str(uuid4())
    """ Local Unique ID"""

    adapter_type: Optional[str] = None
    """ Adapter type (only used with ClientManager)"""

    authentication: Optional[Dict[str, Any]] = None
    """ (Primary) authentication information """

    fallback_authentications: Optional[List[Dict[str, Any]]] = None
    """ The list of fallback Authentication information
    
        This is in junction with GA4GH Service Information.
    """

    url: str
    """ Base URL """

    mode: str = 'explorer'
    """ Client mode ("standard" or "explorer") - only applicable if the client supports. """

    def get_authentications(self) -> List[Dict[str, Any]]:
        """ Get the list of authentication information """
        raw_auths = []

        if self.authentication:
            raw_auths.append(self.authentication)
        if self.fallback_authentications:
            raw_auths.extend(self.fallback_authentications)

        return [self.__convert_to_dict(raw_auth) for raw_auth in raw_auths]

    def __convert_to_dict(self, model: Union[Dict[str, Any], BaseModel]) -> Dict[str, Any]:
        converted_model: Dict[str, Any] = dict()

        if isinstance(model, dict):
            converted_model.update(model)
        elif isinstance(model, BaseModel):
            converted_model.update(model.dict())
        else:
            raise NotImplementedError(f'No interpretation for {model}')

        # Short-term backward-compatibility until May 2022
        if 'oauth2' in converted_model:
            converted_model = converted_model['oauth2']
            converted_model['type'] = 'oauth2'

        return converted_model


class ConfigurationError(RuntimeError):
    """ General Error. """


class MissingEndpointError(ConfigurationError):
    """ Raised when a request endpoint is not registered. """


_LIST_OF_ADAPTER_TYPE_WITHOUT_DEFAULT_ENDPOINT = {'registry'}


class Configuration(BaseModel):
    """Configuration (v3)"""
    __logger = get_logger('Configuration')

    version: int = 3
    defaults: Dict[str, str] = dict()  # adapter-type-to-service-id
    endpoints: List[ServiceEndpoint] = list()

    def set_default(self, adapter_type: str, endpoint_id: str):
        self.__logger.debug(f'adapter_type = {adapter_type}, endpoint_id = {id}')

        if not endpoint_id or endpoint_id.lower() in ('none', 'null'):
            # Remove the default endpoint of that client type
            del self.defaults[adapter_type]
        else:
            try:
                endpoint = self.get_endpoint(adapter_type, endpoint_id)
            except MissingEndpointError:
                raise ConfigurationError(f"Could not set default, not {adapter_type} adapter with id {endpoint_id}")

            self.defaults[adapter_type] = endpoint.id

    def remove_endpoint(self, adapter_type: str, endpoint_id: str):
        self.__logger.debug(f'endpoint_id = {endpoint_id}')
        self.endpoints = [endpoint for endpoint in self.endpoints if
                          endpoint.id != endpoint_id and endpoint.adapter_type != adapter_type]

        if adapter_type in self.defaults and self.defaults[adapter_type] == endpoint_id:
            del self.defaults[adapter_type]

    def add_endpoint(self, endpoint_id: str, adapter_type: str, url: str = None):
        self.__logger.debug(f'adapter_type = {adapter_type}, url = {url}')

        if self._get_all_endpoints_by(adapter_type, endpoint_id):
            raise ConfigurationError(f"Could not add endpoint, found existing one with id {endpoint_id}")

        endpoint = ServiceEndpoint(id=endpoint_id, adapter_type=adapter_type, url=url or '')
        self.endpoints.append(endpoint)

        if adapter_type in self.defaults and not self.defaults[adapter_type]:
            self.defaults[adapter_type] = endpoint_id

        return endpoint

    def _get_all_endpoints_by(self,
                              adapter_type: Optional[str] = None,
                              endpoint_id: Optional[str] = None) -> List[ServiceEndpoint]:
        return [
            endpoint for endpoint in self.endpoints
            if (
                    (adapter_type is not None and endpoint.adapter_type == adapter_type)
                    or (endpoint_id is not None and endpoint.id == endpoint_id)
            )
        ]

    def get_default_endpoint(self,
                             adapter_type: str,
                             create_if_missing: bool = False) -> Optional[ServiceEndpoint]:
        if self._adapter_type_can_have_default_endpoint(adapter_type) and adapter_type in self.defaults:
            try:
                return self.get_endpoint(adapter_type,
                                         endpoint_id=self.defaults[adapter_type],
                                         create_if_missing=False)
            except MissingEndpointError:
                raise MissingEndpointError(f'No default endpoint for "{adapter_type}"')
        else:
            if create_if_missing:
                return self.get_endpoint(adapter_type,
                                         create_if_missing=create_if_missing)
            else:
                raise MissingEndpointError(f'No default endpoint for "{adapter_type}"')

    def get_endpoint(self,
                     adapter_type: str,
                     endpoint_id: Optional[str] = None,
                     create_if_missing: bool = False) -> ServiceEndpoint:
        endpoints: List[ServiceEndpoint] = self._get_all_endpoints_by(adapter_type, endpoint_id)
        endpoint: Optional[ServiceEndpoint] = endpoints[0] if endpoints else None

        # When the endpoint is not available...
        if endpoint is None:
            if create_if_missing:
                endpoint = ServiceEndpoint(id=str(uuid4()), adapter_type=adapter_type, url='')  # Leave to an empty URL
                self.endpoints.append(endpoint)
                if self._adapter_type_can_have_default_endpoint(adapter_type):
                    self.defaults[adapter_type] = endpoint.id
            else:
                raise MissingEndpointError(f'The "{adapter_type}" endpoint #{endpoint_id or "?"} is not defined.')

        return endpoint

    @staticmethod
    def _adapter_type_can_have_default_endpoint(adapter_type: str) -> bool:
        return adapter_type not in {'registry'}


@service.registered(
    params=[
        EnvironmentVariable('DNASTACK_CONFIG_FILE', default=os.path.join(CLI_DIRECTORY, 'config.yaml'),
                            allow_default=True)
    ]
)
class ConfigurationManager:
    def __init__(self, file_path: str):
        self.__logger = get_logger(f'{type(self).__name__}')
        self.__file_path = file_path
        self.__swap_file_path = f'{self.__file_path}.swp'

    def load_raw(self):
        if not os.path.exists(self.__file_path):
            return '{}'
        with open(self.__file_path, 'r') as f:
            return f.read()

    def load(self):
        raw_config = self.load_raw()
        if not raw_config:
            return Configuration()
        config = Configuration(**yaml.load(raw_config, Loader=yaml.SafeLoader))
        return config

    def save(self, configuration: Configuration):
        # Note (1): This is designed to have file operation done as quickly as possible to reduce race conditions.
        # Note (2): Instead of interfering with the main file directly, the new content is written to a temp file before
        #           swapping with the real file to minimize the I/O block.
        new_content = yaml.dump(configuration.dict(exclude_none=True), Dumper=yaml.SafeDumper)
        if not os.path.exists(os.path.dirname(self.__swap_file_path)):
            os.makedirs(os.path.dirname(self.__swap_file_path), exist_ok=True)
        with open(self.__swap_file_path, 'w') as f:
            f.write(new_content)
        shutil.copyfile(self.__swap_file_path, self.__file_path)
        os.unlink(self.__swap_file_path)
