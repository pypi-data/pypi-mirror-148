import json
from typing import Dict, List, Optional, Any

import click
from click import BadParameter, Abort
from imagination import container
from pydantic import BaseModel

from ..utils import handle_error_gracefully
from ...client.collections_client import CollectionServiceClient
from ...client.dataconnect_client import DataConnectClient
from ...client.files_client import DrsClient
from dnastack.client.service_registry.client import ServiceRegistry
from ...configuration import Configuration, ConfigurationManager, MissingEndpointError, OAuth2Authentication
from ...feature_flags import in_global_debug_mode
from ...helpers.logger import get_logger
from ...json_path import JsonPath, BrokenPropertyPathError

_full_schema = Configuration.schema()
_adapter_to_property_paths: Dict[str, List[str]] = dict()
_logger = get_logger('config')

service_adapter_types = [
    CollectionServiceClient.get_adapter_type(),
    DataConnectClient.get_adapter_type(),
    DrsClient.get_adapter_type(),
    ServiceRegistry.get_adapter_type(),
]


@click.group("config")
def config_command_group():
    pass


@config_command_group.command("schema", help="Show the schema of the configuration file")
@handle_error_gracefully
def config_schema():
    click.echo(json.dumps(_full_schema, indent=2, sort_keys=True))


@config_command_group.command("available-properties", help="List all available configuration properties")
@click.option("--type", "-t", required=False, default=None)
@handle_error_gracefully
def config_list_available_properties(type: Optional[str] = None):
    __show_available_properties(type)


def __show_available_properties(adapter_type: Optional[str] = None):
    print()

    click.secho('                                          ', bold=True, bg='blue')
    click.secho('  All available configuration properties  ', bold=True, bg='blue')
    click.secho('                                          ', bold=True, bg='blue')

    click.echo('\nPlease check out https://docs.viral.ai/analytics for more information.')

    adapter_to_property_paths = __get_known_adapter_to_property_paths()

    for service_adapter_name, service_property_paths in adapter_to_property_paths.items():
        if adapter_type and adapter_type != service_adapter_name:
            continue
        click.secho(f'\n{service_adapter_name}\n', bold=True)
        for service_property_path in service_property_paths:
            if service_property_path == 'adapter_type':
                continue  # This is an internal property. Permanently skip.
            if service_property_path == 'default':
                continue  # This is temporarily skipped until the CLI support multiple endpoint.
            click.secho(f'  · {service_adapter_name}.{service_property_path}')

    print()


def __get_known_adapter_to_property_paths() -> Dict[str, List[str]]:
    if not _adapter_to_property_paths:
        __resolve_reference(_full_schema)
        service_property_paths = __list_all_json_path(_full_schema['properties']['endpoints']['items'])

        for service_adapter_name in service_adapter_types:
            _adapter_to_property_paths[service_adapter_name] = list()
            for service_property_path in service_property_paths:
                if service_property_path in ['id', 'adapter_type']:
                    continue  # This is an internal property. Permanently skip.
                _adapter_to_property_paths[service_adapter_name].append(service_property_path)

    return _adapter_to_property_paths


def __list_all_json_path(obj: Dict[str, Any], prefix_path: List[str] = None) -> List[str]:
    properties = obj.get('properties') or dict()
    paths = []

    prefix_path = prefix_path or list()

    if len(prefix_path) == 1 and prefix_path[0] == 'authentication':
        return [
            f'{prefix_path[0]}.{oauth2_path}'
            for oauth2_path in __list_all_json_path(OAuth2Authentication.schema())
        ]
    else:
        if obj['type'] == 'object':
            for property_name, obj_property in properties.items():
                if 'anyOf' in obj_property:
                    for property_to_resolve in obj_property['anyOf']:
                        paths.extend(__list_all_json_path(__fetch_reference(property_to_resolve['$ref'], _full_schema),
                                                          prefix_path + [property_name]))
                elif obj_property['type'] == 'object':
                    paths.extend(__list_all_json_path(obj_property, prefix_path + [property_name]))
                elif obj_property['type'] == 'array':
                    paths.extend(__list_all_json_path(obj_property['items'], prefix_path + [property_name]))
                    paths.extend(__list_all_json_path(obj_property['items'], prefix_path + [property_name + '[i]']))
                else:
                    prefix_path_string = '.'.join(prefix_path)
                    paths.append(f'{prefix_path_string}{"." if prefix_path_string else ""}{property_name}')

    return sorted(paths)


def __fetch_reference(reference_url: str, root: Dict[str, Any]):
    if reference_url.startswith('#/'):
        ref_path = reference_url[2:].split(r'/')
        local_reference = root
        try:
            while ref_path:
                property_name = ref_path.pop(0)
                local_reference = local_reference[property_name]
        except KeyError as e:
            raise RuntimeError(f'The reference {reference_url} for the configuration is undefined.')
        return __resolve_reference(local_reference, root)
    raise NotImplementedError('Resolving an external reference is not supported.')


def __resolve_reference(obj: Dict[str, Any], root: Optional[Dict[str, Any]] = None):
    root = root or obj
    properties = obj.get('properties') or dict()
    for property_name, obj_property in properties.items():
        if obj_property.get('$ref'):
            properties[property_name] = __fetch_reference(obj_property.get('$ref'), root)
        # Deal with array
        if obj_property.get('items') and obj_property.get('items').get('$ref'):
            obj_property['items'] = __fetch_reference(obj_property.get('items').get('$ref'), root)

    return obj


@config_command_group.command("set-default")
@click.argument("adapter_type", required=True)
@click.argument("endpoint_id", required=False, default=None)
@handle_error_gracefully
def set_default(adapter_type: str, endpoint_id: Optional[str] = None):
    config_manager: ConfigurationManager = container.get(ConfigurationManager)
    configuration: Configuration = config_manager.load()
    configuration.set_default(adapter_type=adapter_type, endpoint_id=endpoint_id)
    config_manager.save(configuration)


@config_command_group.command("remove-endpoint")
@click.argument("adapter_type", required=True)
@click.argument("endpoint_id", required=True)
@handle_error_gracefully
def remove_endpoint(adapter_type: str, endpoint_id: str):
    config_manager: ConfigurationManager = container.get(ConfigurationManager)
    configuration: Configuration = config_manager.load()
    configuration.remove_endpoint(adapter_type=adapter_type, endpoint_id=endpoint_id)
    config_manager.save(configuration)


@config_command_group.command("add-endpoint")
@click.argument("adapter-type", required=True)
@click.argument("endpoint-id", required=True)
@click.argument("url", required=False, default=None)
@handle_error_gracefully
def add_endpoint(adapter_type: str, endpoint_id: str, url: str):
    config_manager: ConfigurationManager = container.get(ConfigurationManager)
    configuration: Configuration = config_manager.load()
    configuration.add_endpoint(adapter_type=adapter_type, endpoint_id=endpoint_id, url=url)
    config_manager.save(configuration)


@config_command_group.command("list")
@click.pass_context
def config_list(ctx: click.Context):
    config_manager: ConfigurationManager = container.get(ConfigurationManager)
    click.secho(config_manager.load_raw() or '{}', dim=True)


@config_command_group.command("get")
@click.argument("key")
@click.option("--endpoint-id", "-i", required=False, type=str, default=None)
@handle_error_gracefully
def config_get(key: str, endpoint_id: str):
    _logger.debug(f'GET {key}')
    adapter_type, path = __parse_configuration_key(key)
    config_manager: ConfigurationManager = container.get(ConfigurationManager)
    configuration: Configuration = config_manager.load()

    try:
        endpoint = (
            configuration.get_endpoint(adapter_type,
                                       endpoint_id=endpoint_id,
                                       create_if_missing=False)
            if endpoint_id
            else configuration.get_default_endpoint(adapter_type)
        )

        try:
            result = JsonPath.get(endpoint, path)
        except BrokenPropertyPathError as broken_path_error:
            if in_global_debug_mode:
                raise broken_path_error
            else:
                raise Abort(f'The configuration {key} does not exist.')
    except MissingEndpointError:
        result = None

    if result is None:
        click.secho('null', dim=True)
    elif isinstance(result, bool):
        click.secho(str(result).lower(), dim=True)
    elif isinstance(result, BaseModel):
        click.secho(result.json(indent=2), dim=True)
    else:
        click.secho(result, dim=True)


@config_command_group.command("set")
@click.argument("key")
@click.argument("value")
@click.option("--endpoint-id", "-i", required=False, type=str, default=None)
@handle_error_gracefully
def config_set(key: str, value: str, endpoint_id: str):
    _logger.debug(f'SET {key} {value}')
    adapter_type, path = __parse_configuration_key(key)
    config_manager: ConfigurationManager = container.get(ConfigurationManager)
    configuration = config_manager.load()

    endpoint = (
        configuration.get_endpoint(adapter_type,
                                   endpoint_id=endpoint_id,
                                   create_if_missing=True)
        if endpoint_id
        else configuration.get_default_endpoint(adapter_type, create_if_missing=True)
    )

    try:
        JsonPath.set(endpoint, path, value)
    except BrokenPropertyPathError as __:
        # Attempt to repair the broken path.
        __repair_path(endpoint, '.'.join(path.split('.')[:-1]))

        # Then, try again.
        try:
            JsonPath.set(endpoint, path, value)
        except BrokenPropertyPathError as e:
            if in_global_debug_mode:
                raise e
            else:
                raise Abort(f'The configuration {key} does not exist.')

    config_manager.save(configuration)


@config_command_group.command("unset")
@click.argument("key")
@click.option("--endpoint-id", "-i", required=False, type=str, default=None)
def config_unset(key: str, endpoint_id: str):
    adapter_type, path = __parse_configuration_key(key)
    config_manager: ConfigurationManager = container.get(ConfigurationManager)
    configuration = config_manager.load()

    endpoint = (
        configuration.get_endpoint(adapter_type,
                                   endpoint_id=endpoint_id,
                                   create_if_missing=False)
        if endpoint_id
        else configuration.get_default_endpoint(adapter_type)
    )

    try:
        JsonPath.set(endpoint, path, None)
        __repair_path(endpoint, path)  # This is to ensure that the required properties are set to the default value.
    except BrokenPropertyPathError as __:
        # The path does not exist. Nothing to unset.
        return

    config_manager.save(configuration)


def __repair_path(obj, path: str):
    selectors = path.split(r'.')
    visited = []

    _logger.debug(f'__repair_path: ENTER: type(obj) => {type(obj).__name__}')
    _logger.debug(f'__repair_path: ENTER: obj => {obj}')
    _logger.debug(f'__repair_path: ENTER: path => {path}')

    for selector in selectors:
        visited.append(selector)
        route = '.'.join(visited)

        _logger.debug(f'__repair_path: LOOP: route = {route}')

        try:
            JsonPath.get(obj, route, raise_error_on_null=True)
            break
        except BrokenPropertyPathError as e:
            visited_nodes = e.visited_path.split(r'.')
            last_visited_node = visited_nodes[-1]

            node = e.parent or obj

            _logger.debug(f'__repair_path: LOOP: ***** Broken Path Detected *****')
            _logger.debug(f'__repair_path: LOOP: type(e.parent) => {type(e.parent).__name__}')
            _logger.debug(f'__repair_path: LOOP: e.parent => {e.parent}')
            _logger.debug(f'__repair_path: LOOP: last_visited_node => {last_visited_node}')

            annotation = node.__annotations__[last_visited_node]

            if str(annotation).startswith('typing.Union[') or str(annotation).startswith("typing.Optional["):
                # Dealing with Union/Optional
                _logger.debug(f'__repair_path: LOOP: Handling union and optional')
                _logger.debug(f'__repair_path: LOOP: annotation.__args__ => {annotation.__args__}')
                __initialize_default_value(node, last_visited_node, annotation.__args__[0])
            else:
                __initialize_default_value(node, last_visited_node, annotation)

            _logger.debug(f'__repair_path: LOOP: node = {getattr(node, last_visited_node)}')

    _logger.debug(f'__repair_path: EXIT: obj => {obj}')


def __initialize_default_value(node, property_name: str, annotation):
    if str(annotation).startswith('typing.Dict['):
        setattr(node, property_name, dict())
    elif str(annotation).startswith('typing.List['):
        setattr(node, property_name, list())
    elif issubclass(annotation, BaseModel):
        required_properties = annotation.schema().get('required') or []
        placeholders = {
            p: __get_place_holder(annotation.__annotations__[p])
            for p in required_properties
        }
        setattr(node, property_name, annotation(**placeholders))
    else:
        setattr(node, property_name, annotation())


def __get_place_holder(cls):
    if cls == str:
        return ''
    elif cls == int or cls == float:
        return 0
    elif cls == bool:
        return False
    else:
        raise NotImplementedError(cls)


def __parse_configuration_key(key: str):
    nodes = key.split(r'.')

    adapter_type = nodes[0]
    path = '.'.join(nodes[1:])

    adapter_to_property_paths = __get_known_adapter_to_property_paths()

    if adapter_type not in adapter_to_property_paths:
        __show_available_properties()
        _logger.debug(f'Unknown adapter type: {adapter_type}')
        raise BadParameter(f'Unknown configuration key: {key}')

    if path and path not in adapter_to_property_paths[adapter_type]:
        __show_available_properties(adapter_type)
        _logger.debug(f'A/{adapter_type}: Unknown Path: {path}')
        _logger.debug(f'A/{adapter_type}: Available Paths: {adapter_to_property_paths[adapter_type]}')
        raise BadParameter(f'Unknown configuration key: {key}')

    return adapter_type, path
