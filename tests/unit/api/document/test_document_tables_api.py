import unittest

from http import HTTPStatus
from mock import patch, Mock, MagicMock

from search_service.api.document import DocumentTablesAPI
from search_service.models.table import Table, TableSchema
from search_service import create_app


class TestDocumentTablesAPI(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app(config_module_class='search_service.config.Config')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tear_down(self) -> None:
        self.app_context.pop()

    @patch('search_service.api.document.reqparse.RequestParser')
    @patch('search_service.api.document.get_proxy_client')
    def test_post(self, get_proxy: MagicMock, RequestParser: MagicMock) -> None:
        mock_proxy = get_proxy.return_value = Mock()
        RequestParser().parse_args.return_value = dict(data='[]', index='fake_index')

        response = DocumentTablesAPI().post()
        self.assertEqual(list(response)[1], HTTPStatus.OK)
        mock_proxy.create_document.assert_called_with(data=[], index='fake_index', schema=TableSchema)

    @patch('search_service.api.document.reqparse.RequestParser')
    @patch('search_service.api.document.get_proxy_client')
    def test_put(self, get_proxy: MagicMock, RequestParser: MagicMock) -> None:
        mock_proxy = get_proxy.return_value = Mock()
        test_table = Table(database='1', cluster='2', schema='3', name='4', key='5', tags=[], badges=[],
                           column_names=[], last_updated_timestamp=0)
        expected_data = TableSchema(many=True).dumps([test_table]).data
        RequestParser().parse_args.return_value = dict(data=expected_data, index='fake_index')

        response = DocumentTablesAPI().put()
        self.assertEqual(list(response)[1], HTTPStatus.OK)
        mock_proxy.update_document.assert_called_with(data=[test_table], index='fake_index', schema=TableSchema)

    def test_should_not_reach_create_with_id(self) -> None:
        response = self.app.test_client().post('/document_table/1')

        self.assertEquals(response.status_code, 405)

    def test_should_not_reach_update_with_id(self) -> None:
        response = self.app.test_client().put('/document_table/1')

        self.assertEquals(response.status_code, 405)
