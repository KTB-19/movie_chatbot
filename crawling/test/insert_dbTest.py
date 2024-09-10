import unittest
from unittest.mock import patch, MagicMock
from datetime import time, date, datetime
from database.insert_db import convert_time, convert_date, insert_data  # 실제 모듈 이름과 경로로 변경합니다.

class TestMovieFunctions(unittest.TestCase):

    def test_convert_time(self):
        # convert_time 테스트
        self.assertEqual(convert_time("10:30"), (time(10, 30), 0))
        self.assertEqual(convert_time("24:15"), (time(0, 15), 1))
        self.assertEqual(convert_time("25:00"), (time(1, 0), 1))

    def test_convert_date(self):
        # convert_date 테스트
        self.assertEqual(convert_date("01월 15일", 0), date(2024, 1, 15))
        self.assertEqual(convert_date("12월 31일", 1), date(2025, 1, 1))

    @patch('pymysql.connect')
    @patch('os.getenv')
    @patch('dotenv.load_dotenv')
    def test_insert_data(self, mock_load_dotenv, mock_getenv, mock_connect):

        mock_load_dotenv.return_value = None
        mock_getenv.side_effect = lambda key: 'test_value'

        # Mock DB connection & cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Mock cursor
        mock_cursor.fetchone.side_effect = [None, None]  # movie와 theater가 모두 없는 경우
        mock_cursor.lastrowid = 1

        data_list = [
            ("wide_area", "basic_area", 1, "theater_name", "movie_title", "10:30", "01월 15일")
        ]

        # insert_data 함수 호출
        insert_data(data_list)

        # DB 연결이 호출되었는지 확인
        mock_connect.assert_called_once_with(host='test_value', user='test_value', passwd='test_value', charset='utf8',
                                             database='moviedatabase')

        # movie 삽입이 호출되었는지 확인
        mock_cursor.execute.assert_any_call("SELECT movie_id FROM movie WHERE title = %s", ("movie_title",))
        mock_cursor.execute.assert_any_call("INSERT INTO movie (title) VALUES (%s)", ("movie_title",))

        # theater 삽입이 호출되었는지 확인
        mock_cursor.execute.assert_any_call("SELECT theater_id FROM theater WHERE name = %s", ("theater_name",))
        mock_cursor.execute.assert_any_call(
            "INSERT INTO theater (theater_id, name, wide_area, basic_area) VALUES (%s, %s, %s, %s)",
            (1, "theater_name", "wide_area", "basic_area"))

        # info 삽입이 호출되었는지 확인
        mock_cursor.execute.assert_any_call(
            "INSERT INTO info (movie_id, theater_id, time, date) VALUES (%s, %s, %s, %s)",
            (1, 1, time(10, 30), date(2024, 1, 15)))

        # DB 변경 사항 커밋이 호출되었는지 확인
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
