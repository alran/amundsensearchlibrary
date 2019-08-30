import unittest

from http import HTTPStatus
from unittest import mock
from mock import MagicMock

from metadata_service import create_app
from metadata_service.api.table import TableTagAPI


class TableTagAPITest(unittest.TestCase):

    @mock.patch('metadata_service.api.table.SearchProxy')
    @mock.patch('metadata_service.api.table.get_proxy_client')
    def setUp(self, mock_get_proxy_client: MagicMock, SearchProxy: MagicMock) -> None:
        self.app = create_app(config_module_class='metadata_service.config.LocalConfig')
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.mock_search = SearchProxy(config=self.app.config)
        self.mock_client = mock.Mock()
        mock_get_proxy_client.return_value = self.mock_client
        self.api = TableTagAPI()

    def tearDown(self) -> None:
        self.app_context.pop()

    def test_put(self) -> None:
        data = {'name': 'test'}
        self.mock_client.get_table_search_document.return_value = data
        response = self.api.put(table_uri='1', tag='2')
        self.assertEqual(list(response)[1], HTTPStatus.OK)
        self.mock_client.add_tag.assert_called_once()
        self.mock_client.get_table_search_document.assert_called_once_with(table_uri='1')
        self.mock_search.update_elastic.assert_called_once_with(table_uri='1', data=data)

    def test_delete(self) -> None:
        response = self.api.delete(table_uri='1', tag='2')
        self.assertEqual(list(response)[1], HTTPStatus.OK)
        self.mock_client.delete_tag.assert_called_once()
