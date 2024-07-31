import unittest
from unittest.mock import patch, MagicMock
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
import process_division

class TestProcessDivision(unittest.TestCase):

    @patch('process_division._process_with_multiprocessing')
    @patch('crawler.init_driver')
    @patch('crawler.safe_find_element')
    @patch('process_division.WebDriverWait')
    @patch('process_division.time.sleep', return_value=None)
    def test_process_division(self, mock_sleep, mock_WebDriverWait, mock_safe_find_element, mock_init_driver, mock_process_with_multiprocessing):
        driver = mock_init_driver.return_value

        # Mock the driver methods and their returns
        driver.find_elements.side_effect = [
            [MagicMock(text='TheaterName1', get_attribute=MagicMock(return_value='theacd1'))],
            [MagicMock(text='MovieTitle1')],
            [MagicMock(text='10:00')]
        ]

        mock_safe_find_element.side_effect = [
            MagicMock(text='WideareaName', get_attribute=MagicMock(return_value='wideareacd')),
            MagicMock(text='BasareaName1', get_attribute=MagicMock(return_value='basareacd1')),
            MagicMock(text='TheaterName1', get_attribute=MagicMock(return_value='theacd1')),
            MagicMock(text='MovieTitle1'),
            MagicMock(text='7월 1일'),
        ]

        mock_WebDriverWait.return_value.until.return_value = True

        # Set mock for _process_with_multiprocessing
        mock_process_with_multiprocessing.return_value = [
            ['WideareaName', 'basareacd1', 'BasareaName1', 'theacd1', 'TheaterName1', 'MovieTitle1', '10:00', '7월 1일']
        ]

        result = process_division.process_division(1)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0],
                         ['WideareaName', 'basareacd1', 'BasareaName1', 'theacd1', 'TheaterName1', 'MovieTitle1',
                          '10:00', '7월 1일'])

    @patch('process_division._process_with_multiprocessing')
    @patch('crawler.init_driver')
    @patch('crawler.safe_find_element')
    @patch('process_division.WebDriverWait')
    @patch('process_division.time.sleep', return_value=None)
    def test_process_division_with_exceptions(self, mock_sleep, mock_WebDriverWait, mock_safe_find_element, mock_init_driver, mock_process_with_multiprocessing):
        # Test cases where exceptions are raised

        # Mock init_driver to raise an exception
        mock_init_driver.side_effect = Exception("Driver initialization failed")

        # driver initialization failure
        mock_process_with_multiprocessing.return_value = []
        result = process_division.process_division(1)
        self.assertEqual(result, [])

        # Reset mocks
        mock_init_driver.side_effect = None
        driver = mock_init_driver.return_value

        # StaleElementReferenceException
        mock_safe_find_element.side_effect = StaleElementReferenceException
        mock_process_with_multiprocessing.return_value = []
        result = process_division.process_division(1)
        self.assertEqual(result, [])

        # NoSuchElementException
        mock_safe_find_element.side_effect = NoSuchElementException
        mock_process_with_multiprocessing.return_value = []
        result = process_division.process_division(1)
        self.assertEqual(result, [])

        # TimeoutException
        mock_WebDriverWait.return_value.until.side_effect = TimeoutException
        mock_process_with_multiprocessing.return_value = []
        result = process_division.process_division(1)
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
