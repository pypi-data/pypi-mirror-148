import os
from typing import Union, List, Any, Optional

from imagination import container

from .collections_client import CollectionServiceClient
from .constants import DATA_SERVICE_CLIENT_CLASSES
from .dataconnect_client import DataConnectClient
from .files_client import DrsClient
from ..configuration import ConfigurationManager, MissingEndpointError, Configuration
from ..helpers.logger import get_logger


class PublisherClient:
    """
    A consolidated client for a suite of APIs (Data Connect API, WES API, DRS API, and Collection Service API)

    All sub-clients are automatically initiated with the configuration of the default service endpoint of each
    sub-client type (as known as "adapter type"), defined in the configuration file.

    .. deprecatedVersion:: 3.0
    """

    def __init__(self):
        config_manager = container.get(ConfigurationManager)
        config: Configuration = config_manager.load()

        self._logger = get_logger(type(self).__name__)

        for cls in DATA_SERVICE_CLIENT_CLASSES:
            adapter_type = cls.get_adapter_type()
            property_name = f'_{adapter_type}'

            try:
                default_endpoint = config.get_default_endpoint(adapter_type) \
                                   or config.get_endpoint(adapter_type, create_if_missing=True)
                setattr(self, property_name, cls.make(default_endpoint))
            except MissingEndpointError:
                self._logger.debug(f'There exists no default {adapter_type} endpoint configured and the client is '
                                   f'not available for this type of service.')
                setattr(self, property_name, None)

    @property
    def dataconnect(self) -> Optional[DataConnectClient]:
        """
        ..deprecated: v3.1
        """
        return self._data_connect

    @dataconnect.setter
    def dataconnect(self, client: DataConnectClient):
        """
        ..deprecated: v3.1
        """
        assert client is None or isinstance(client, DataConnectClient)
        self._data_connect = client

    @property
    def data_connect(self) -> Optional[DataConnectClient]:
        """ The client for the default data connect endpoint """
        return self._data_connect

    @data_connect.setter
    def data_connect(self, client: DataConnectClient):
        assert client is None or isinstance(client, DataConnectClient)
        self._data_connect = client

    @property
    def collections(self) -> Optional[CollectionServiceClient]:
        """ The client for the default collection API endpoint """
        return self._collections

    @collections.setter
    def collections(self, client: CollectionServiceClient):
        assert client is None or isinstance(client, CollectionServiceClient)
        self._collections = client

    @property
    def files(self) -> DrsClient:
        """ The client for the default data repository service (DRS) endpoint """
        return self._drs

    @files.setter
    def files(self, client: DrsClient):
        assert client is None or isinstance(client, DrsClient)
        self._drs = client

    def load(self, urls: Union[str, List[str]]) -> Any:
        """
        Return the raw output of one or more DRS resources

        :param urls: One or a list of DRS urls (drs://...)
        :return: The raw output of the specified DRS resource
        """
        if isinstance(urls, str):
            urls = [urls]

        download_content = []

        self.files.download_files(
            urls=urls,
            display_progress_bar=False,
            out=download_content,
        )
        return download_content

    def download(
            self,
            urls: Union[str, List[str]],
            output_dir: str = os.getcwd(),
            display_progress_bar: bool = False,
    ) -> None:
        """
        Download one or more DRS resources from the specified urls

        :param urls: One or a list of DRS urls (drs://...)
        :param output_dir: The directory to output the downloaded files to.
        :param display_progress_bar: Display the progress of the downloads. This is False by default
        :return:
        """
        if isinstance(urls, str):
            urls = [urls]

        self.files.download_files(
            urls=urls,
            output_dir=output_dir,
            display_progress_bar=display_progress_bar,
        )

    def __repr__(self):
        return f'<{type(self).__name__} collections={self.collections} data_connect={self._data_connect} files={self.files} wes={self.wes}>'
