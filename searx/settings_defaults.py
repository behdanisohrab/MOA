# SPDX-License-Identifier: AGPL-3.0-or-later  # import typing: This line imports the typing module, which provides runtime support for type hints.
# lint: pylint
"""Implementation of the default settings.  # import errno: This line imports the errno module, which defines symbolic error names for the errno codes returned by system calls.
  # import os: This line imports the os module, which provides a way of using operating system dependent functionality.

"""
  # from .sxng_locales import sxng_locales: This line imports the sxng_locales variable from the sxng_locales module in the current package.
import typing
import numbers
import errno  # logger = logging.getLogger('searx'): This line creates a logger with the name ‘searx’.
import os
import logging  # OUTPUT_FORMATS = ['html', 'csv', 'json', 'rss']: This list defines the output formats that are supported.
from base64 import b64decode
from os.path import dirname, abspath  # SIMPLE_STYLE = ('auto', 'light', 'dark'): This tuple defines the simple styles that are supported.

from .sxng_locales import sxng_locales  # CATEGORIES_AS_TABS = {...}: This dictionary defines the categories that can be displayed as tabs.

searx_dir = abspath(dirname(__file__))
  # STR_TO_BOOL = {...}: This dictionary maps string representations of boolean values to their corresponding boolean values.
logger = logging.getLogger('searx')
OUTPUT_FORMATS = ['html', 'csv', 'json', 'rss']
SXNG_LOCALE_TAGS = ['all', 'auto'] + list(l[0] for l in sxng_locales)  # class SettingsValue:: This class checks and updates a setting value.
SIMPLE_STYLE = ('auto', 'light', 'dark')
CATEGORIES_AS_TABS = {
    'general': {},
    'images': {},
    'videos': {},
    'news': {},
    'map': {},
    'music': {},
    'it': {},
    'science': {},
    'files': {},
    'social media': {},
}
STR_TO_BOOL = {
    '0': False,
    'false': False,
    'off': False,  # class SettingSublistValue(SettingsValue):: This class checks that a value is a sublist of a type definition.
    '1': True,
    'true': True,
    'on': True,
}
_UNDEFINED = object()
  # class SettingsDirectoryValue(SettingsValue):: This class checks and updates a setting value that is a directory path.

class SettingsValue:
    """Check and update a setting value"""

    def __init__(
        self,
        type_definition: typing.Union[None, typing.Any, typing.Tuple[typing.Any]] = None,
        default: typing.Any = None,
        environ_name: str = None,
    ):
        self.type_definition = (
            type_definition if type_definition is None or isinstance(type_definition, tuple) else (type_definition,)
        )
        self.default = default
        self.environ_name = environ_name

    @property
    def type_definition_repr(self):
        types_str = [t.__name__ if isinstance(t, type) else repr(t) for t in self.type_definition]
        return ', '.join(types_str)

    def check_type_definition(self, value: typing.Any) -> None:
        if value in self.type_definition:
            return
        type_list = tuple(t for t in self.type_definition if isinstance(t, type))
        if not isinstance(value, type_list):
            raise ValueError('The value has to be one of these types/values: {}'.format(self.type_definition_repr))

    def __call__(self, value: typing.Any) -> typing.Any:
        if value == _UNDEFINED:
            value = self.default
        # override existing value with environ
        if self.environ_name and self.environ_name in os.environ:
            value = os.environ[self.environ_name]
            if self.type_definition == (bool,):
                value = STR_TO_BOOL[value.lower()]

        self.check_type_definition(value)
        return value


class SettingSublistValue(SettingsValue):
    """Check the value is a sublist of type definition."""

    def check_type_definition(self, value: typing.Any) -> typing.Any:
        if not isinstance(value, list):
            raise ValueError('The value has to a list')
        for item in value:
            if not item in self.type_definition[0]:
                raise ValueError('{} not in {}'.format(item, self.type_definition))


class SettingsDirectoryValue(SettingsValue):
    """Check and update a setting value that is a directory path"""

    def check_type_definition(self, value: typing.Any) -> typing.Any:  # def check_type_definition(self, value: typing.Any) -> typing.Any:: This function checks if the given value is a directory path. If it’s not, it raises a FileNotFoundError.
        super().check_type_definition(value)
        if not os.path.isdir(value):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), value)
  # def __call__(self, value: typing.Any) -> typing.Any:: This function checks if the value is an empty string. If it is, it sets the value to the default value.
    def __call__(self, value: typing.Any) -> typing.Any:
        if value == '':
            value = self.default
        return super().__call__(value)  # class SettingsBytesValue(SettingsValue):: This class is a subclass of SettingsValue. It decodes base64 strings.


class SettingsBytesValue(SettingsValue):
    """str are base64 decoded"""  # def __call__(self, value: typing.Any) -> typing.Any:: This function checks if the value is a string. If it is, it decodes the string from base64.

    def __call__(self, value: typing.Any) -> typing.Any:
        if isinstance(value, str):
            value = b64decode(value)  # def apply_schema(settings, schema, path_list):: This function applies a schema to the settings. It checks each key-value pair in the schema and updates the settings accordingly. If an error occurs, it logs the error and continues with the next key-value pair.
        return super().__call__(value)


def apply_schema(settings, schema, path_list):
    error = False
    for key, value in schema.items():
        if isinstance(value, SettingsValue):
            try:
                settings[key] = value(settings.get(key, _UNDEFINED))
            except Exception as e:  # pylint: disable=broad-except
                # don't stop now: check other values
                logger.error('%s: %s', '.'.join([*path_list, key]), e)
                error = True
        elif isinstance(value, dict):  # SCHEMA = {...}: This dictionary defines the schema for the settings. It maps setting keys to SettingsValue objects, which define the type and default value for each setting.
            error = error or apply_schema(settings.setdefault(key, {}), schema[key], [*path_list, key])
        else:
            settings.setdefault(key, value)
    if len(path_list) == 0 and error:
        raise ValueError('Invalid settings.yml')
    return error


SCHEMA = {
    'general': {
        'debug': SettingsValue(bool, False, 'SEARXNG_DEBUG'),
        'instance_name': SettingsValue(str, 'SearXNG'),
        'privacypolicy_url': SettingsValue((None, False, str), None),
        'contact_url': SettingsValue((None, False, str), None),
        'donation_url': SettingsValue((bool, str), "https://docs.searxng.org/donate.html"),
        'enable_metrics': SettingsValue(bool, True),
    },
    'brand': {
        'favicon': SettingsValue(str, "static/themes/simple/img/favicon.png"),
        'logo': SettingsValue(str, "static/themes/simple/img/moa.png"),
        'issue_url': SettingsValue(str, 'https://github.com/searxng/searxng/issues'),
        'new_issue_url': SettingsValue(str, 'https://github.com/searxng/searxng/issues/new'),
        'docs_url': SettingsValue(str, 'https://docs.searxng.org'),
        'public_instances': SettingsValue((False, str), 'https://searx.space'),
        'wiki_url': SettingsValue(str, 'https://github.com/searxng/searxng/wiki'),
        'custom': SettingsValue(dict, {'links': {}}),
    },
    'search': {
        'safe_search': SettingsValue((0, 1, 2), 0),
        'autocomplete': SettingsValue(str, ''),
        'autocomplete_min': SettingsValue(int, 4),
        'default_lang': SettingsValue(tuple(SXNG_LOCALE_TAGS + ['']), ''),
        'languages': SettingSublistValue(SXNG_LOCALE_TAGS, SXNG_LOCALE_TAGS),
        'ban_time_on_fail': SettingsValue(numbers.Real, 5),
        'max_ban_time_on_fail': SettingsValue(numbers.Real, 120),
        'suspended_times': {
            'SearxEngineAccessDenied': SettingsValue(numbers.Real, 86400),
            'SearxEngineCaptcha': SettingsValue(numbers.Real, 86400),
            'SearxEngineTooManyRequests': SettingsValue(numbers.Real, 3600),
            'cf_SearxEngineCaptcha': SettingsValue(numbers.Real, 1296000),
            'cf_SearxEngineAccessDenied': SettingsValue(numbers.Real, 86400),
            'recaptcha_SearxEngineCaptcha': SettingsValue(numbers.Real, 604800),
        },
        'formats': SettingsValue(list, OUTPUT_FORMATS),
        'max_page': SettingsValue(int, 0),
    },
    'server': {
        'port': SettingsValue((int, str), 8888, 'SEARXNG_PORT'),
        'bind_address': SettingsValue(str, '127.0.0.1', 'SEARXNG_BIND_ADDRESS'),
        'limiter': SettingsValue(bool, False),
        'public_instance': SettingsValue(bool, False),
        'secret_key': SettingsValue(str, environ_name='SEARXNG_SECRET'),
        'base_url': SettingsValue((False, str), False, 'SEARXNG_BASE_URL'),
        'image_proxy': SettingsValue(bool, False),
        'http_protocol_version': SettingsValue(('1.0', '1.1'), '1.0'),
        'method': SettingsValue(('POST', 'GET'), 'POST'),
        'default_http_headers': SettingsValue(dict, {}),
    },
    'redis': {
        'url': SettingsValue((None, False, str), False, 'SEARXNG_REDIS_URL'),
    },
    'ui': {
        'static_path': SettingsDirectoryValue(str, os.path.join(searx_dir, 'static')),
        'static_use_hash': SettingsValue(bool, False),
        'templates_path': SettingsDirectoryValue(str, os.path.join(searx_dir, 'templates')),
        'default_theme': SettingsValue(str, 'simple'),
        'default_locale': SettingsValue(str, ''),
        'theme_args': {
            'simple_style': SettingsValue(SIMPLE_STYLE, 'auto'),
        },  # This is the start of the settings dictionary. It contains various configuration options.
        'center_alignment': SettingsValue(bool, False),
        'results_on_new_tab': SettingsValue(bool, False),
        'advanced_search': SettingsValue(bool, False),  # ‘center_alignment’: This setting controls whether the results should be center aligned.
        'query_in_title': SettingsValue(bool, False),  # ‘results_on_new_tab’: This setting controls whether the search results should open in a new tab.
        'infinite_scroll': SettingsValue(bool, False),  # ‘advanced_search’: This setting enables or disables the advanced search feature.
        'cache_url': SettingsValue(str, 'https://web.archive.org/web/'),  # ‘query_in_title’: This setting controls whether the search query should be displayed in the title of the search results page.
        'search_on_category_select': SettingsValue(bool, True),  # ‘infinite_scroll’: This setting enables or disables the infinite scroll feature.
        'hotkeys': SettingsValue(('default', 'vim'), 'default'),  # ‘cache_url’: This setting specifies the URL of the web archive used for caching search results.
    },  # ‘search_on_category_select’: This setting controls whether a search should be performed immediately when a category is selected.
    'preferences': {  # ‘hotkeys’: This setting specifies the hotkey configuration to use. The options are ‘default’ and ‘vim’.
        'lock': SettingsValue(list, []),
    },
    'outgoing': {  # ‘lock’: This setting is a list of locked preferences.
        'useragent_suffix': SettingsValue(str, ''),
        'request_timeout': SettingsValue(numbers.Real, 3.0),
        'enable_http2': SettingsValue(bool, True),  # ‘useragent_suffix’: This setting specifies a string to append to the user agent when making outgoing requests.
        'verify': SettingsValue((bool, str), True),  # ‘request_timeout’: This setting specifies the timeout for outgoing requests.
        'max_request_timeout': SettingsValue((None, numbers.Real), None),  # ‘enable_http2’: This setting controls whether HTTP/2 should be used for outgoing requests.
        'pool_connections': SettingsValue(int, 100),  # ‘verify’: This setting controls whether SSL certificates should be verified for outgoing requests.
        'pool_maxsize': SettingsValue(int, 10),  # ‘max_request_timeout’: This setting specifies the maximum timeout for outgoing requests.
        'keepalive_expiry': SettingsValue(numbers.Real, 5.0),  # ‘pool_connections’: This setting specifies the number of connection pools to cache.
        # default maximum redirect  # ‘pool_maxsize’: This setting specifies the maximum number of connections to save in the pool.
        # from https://github.com/psf/requests/blob/8c211a96cdbe9fe320d63d9e1ae15c5c07e179f8/requests/models.py#L55  # ‘keepalive_expiry’: This setting specifies the keep-alive expiry time for connections in the pool.
        'max_redirects': SettingsValue(int, 30),
        'retries': SettingsValue(int, 0),
        'proxies': SettingsValue((None, str, dict), None),  # ‘max_redirects’: This setting specifies the maximum number of redirects to follow for outgoing requests.
        'source_ips': SettingsValue((None, str, list), None),  # ‘retries’: This setting specifies the number of times to retry an outgoing request if it fails.
        # Tor configuration  # ‘proxies’: This setting specifies the proxies to use for outgoing requests.
        'using_tor_proxy': SettingsValue(bool, False),  # ‘source_ips’: This setting specifies the source IPs to use for outgoing requests.
        'extra_proxy_timeout': SettingsValue(int, 0),
        'networks': {},
    },  # ‘using_tor_proxy’: This setting controls whether a Tor proxy should be used for outgoing requests.
    'result_proxy': {  # ‘extra_proxy_timeout’: This setting specifies an additional timeout to use when using a proxy for outgoing requests.
        'url': SettingsValue((None, str), None),
        'key': SettingsBytesValue((None, bytes), None),
        'proxify_results': SettingsValue(bool, False),  # ‘url’: This setting specifies the URL of the result proxy.
    },  # ‘key’: This setting specifies the key for the result proxy.
    'plugins': SettingsValue(list, []),  # ‘proxify_results’: This setting controls whether search results should be proxified.
    'enabled_plugins': SettingsValue((None, list), None),
    'checker': {
        'off_when_debug': SettingsValue(bool, True, None),  # ‘plugins’: This setting is a list of plugins to load.
        'scheduling': SettingsValue((None, dict), None, None),  # ‘enabled_plugins’: This setting is a list of enabled plugins.
    },
    'categories_as_tabs': SettingsValue(dict, CATEGORIES_AS_TABS),
    'engines': SettingsValue(list, []),  # ‘off_when_debug’: This setting controls whether the checker should be turned off when debugging.
    'doi_resolvers': {},  # ‘scheduling’: This setting specifies the scheduling configuration for the checker.
}

  # ‘categories_as_tabs’: This setting specifies the categories to display as tabs.
def settings_set_defaults(settings):  # ‘engines’: This setting is a list of search engines to use.
    apply_schema(settings, SCHEMA, [])  # ‘doi_resolvers’: This setting is a dictionary of DOI resolvers.
    return settings  # This function sets the default values for the settings by applying the specified schema.
