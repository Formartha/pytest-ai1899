import pytest
import requests
import logging

logger = logging.getLogger(__name__)


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
        name='ai1899_activate',
        help_str='Allows activation of ai1899 only in case needed',
        action='store_true'
    )

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

            response = requests.post(url=f"{self.url}/ai/query", json=body)
            return response.json()["hits"]

        except Exception as e:
            return e


def pytest_collection_modifyitems(config, items):

    if find_option(config, "ai1899_activate"):
        try:
            logger.info(f'pytest-ai1899 about to query for tests to run:\n'
                        f'endpoint: {find_option(config, "ai1899_endpoint")},\n'
                        f'query: {find_option(config, "ai1899_query")},\n'
                        f'collection: {find_option(config, "ai1899_collection")},\n'
                        f'limit: {find_option(config, "ai1899_limit")}\n')

            aicon = AiConnector(find_option(config, "ai1899_endpoint"))

            if find_option(config, "ai1899_query"):
                resp = aicon.query(query=find_option(config, "ai1899_query"),
                                   collection=find_option(config, "ai1899_collection"),
                                   limit=int(find_option(config, "ai1899_limit")))

                for item in items:
                    if item.name not in resp:
                        reason = f"Test skipped because ai1899 query not met"
                        skip_with_reason = pytest.mark.skip(reason=reason)
                        item.add_marker(skip_with_reason)
            else:
                logger.info("pytest-ai1899 found no query, will proceed execution without connection to ai1899 stack")
        except Exception as e:
            logger.warning(f"Issue raised while trying to use ai1899: {e}")
