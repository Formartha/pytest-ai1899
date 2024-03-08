import pytest
import requests


def pytest_addoption(parser):
    group = parser.getgroup('ai1899')

    def add_shared_option(name, help_str, default=None, action='store'):
        """
        Add an option to both the command line and the .ini file.
        This function modifies `parser` and `group` from the outer scope.

        :param name: name of the option
        :param help_str: help message
        :param default: default value
        :param action: `group.addoption` action
        """
        parser.addini(
            name=name,
            default=default,
            help=help_str,
        )

        group.addoption(
            '--{0}'.format(name.replace('_', '-')),
            action=action,
            dest=name,
            help='{help} (overrides {name} config option)'.format(
                help=help_str,
                name=name,
            ),
        )

    # registering options
    add_shared_option(
        name='ai1899_query',
        help_str='Phrase a term which will connect to AI1899 to fetch information from it',
    )

    add_shared_option(
        name='ai1899_limit',
        help_str='limit amount of tess to return back',
        default=5,
    )

    add_shared_option(
        name='ai1899_collection',
        help_str='Collection to query from, if set as None, will query from all collections',
        default="Tests",
    )

    add_shared_option(
        name='ai1899_endpoint',
        help_str='The ip address of the ai1899 stack',
        default='http://127.0.0.1/ai/',
    )


def find_option(pytest_config, option_name, default=None):

    value = (
            getattr(pytest_config.option, option_name, None) or
            pytest_config.getini(option_name)
    )
    if isinstance(value, bool):
        return value
    return value or default


class AiConnector(object):

    def __init__(self, url):
        self.url = url

    def query(self, query, collection=None, limit=5):
        """ creates a query term to ai1899 """
        try:
            body = {
                "query": query,
                "collection": collection,
                "limit": limit
            }

            if not collection:
                body.pop("collection")

            response = requests.post(url=f"{self.url}/query", json=body)
            return response.json()["hits"]

        except Exception as e:
            return e


def pytest_collection_modifyitems(config, items):
    aicon = AiConnector(find_option(config, "ai1899_endpoint"))

    resp = aicon.query(query=find_option(config, "ai1899_query"),
                       collection=find_option(config, "ai1899_collection"),
                       limit=int(find_option(config, "ai1899_limit")))

    for item in items:
        if item.name not in resp:
            item.add_marker("skip")
