import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from database.delete_db import delete_data


class TestDeleteDataFunction(unittest.TestCase):

    @patch('pymysql.connect')
    @patch('os.getenv')
    @patch('dotenv.load_dotenv')
    @patch('database.delete_db.datetime')
    def test_delete_data(self, mock_datetime, mock_load_dotenv, mock_getenv, mock_connect):
        mock_load_dotenv.return_value = None
        mock_getenv.side_effect = lambda key: 'test_value'

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # mock
        mock_datetime.today.return_value = datetime(2024, 8, 1)
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

        delete_data()

        # DB 연결이 호출되었는지 확인
        mock_connect.assert_called_once_with(host='test_value', user='test_value', passwd='test_value', charset='utf8',
                                             database='moviedatabase')

        # delete 쿼리가 호출되었는지 확인
        mock_cursor.execute.assert_any_call("DELETE FROM info WHERE date = %s", ('2024-07-31',))

        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
