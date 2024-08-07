import unittest
from unittest.mock import patch, MagicMock
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException
import crawler

class TestCrawler(unittest.TestCase):

    @patch('crawler.webdriver.Chrome')
    def test_safe_find_element(self, MockWebDriver):
        driver = MockWebDriver.return_value
        element = MagicMock()
        driver.find_element.return_value = element

        # 정상 동작하는 경우
        result = crawler.safe_find_element(driver, 'selector', title=False)
        self.assertEqual(result, element)

        # StaleElementReferenceException 발생하는 경우
        driver.find_element.side_effect = [StaleElementReferenceException, element]
        result = crawler.safe_find_element(driver, 'selector', title=False)
        self.assertEqual(result, element)

        # NoSuchElementException 발생하는 경우
        driver.find_element.side_effect = [NoSuchElementException, element]
        result = crawler.safe_find_element(driver, 'selector', title=False)
        self.assertEqual(result, element)

        # 모든 재시도 후 None 반환
        driver.find_element.side_effect = NoSuchElementException
        result = crawler.safe_find_element(driver, 'selector', title=False)
        self.assertIsNone(result)

    @patch('crawler.init_driver')
    @patch('crawler.safe_find_element')
    @patch('crawler.WebDriverWait')
    @patch('crawler.time.sleep', return_value=None)
    def test_crawling(self, mock_sleep, mock_WebDriverWait, mock_safe_find_element, mock_init_driver):
        driver = mock_init_driver.return_value

        driver.find_elements.side_effect = [
            [MagicMock(text='TheaterName1', get_attribute=MagicMock(return_value='theacd1'))],
            [MagicMock(text='MovieTitle1')],
            [MagicMock(text='10:00')]
        ]

        # Mock safe_find_element
        mock_safe_find_element.side_effect = [
            MagicMock(text='WideareaName', get_attribute=MagicMock(return_value='wideareacd')),
            MagicMock(text='BasareaName1', get_attribute=MagicMock(return_value='basareacd1')),
            MagicMock(text='TheaterName1', get_attribute=MagicMock(return_value='theacd1')),
            MagicMock(text='MovieTitle1'),
            MagicMock(text='7월 1일'),
        ]

        mock_WebDriverWait.return_value.until.return_value = True

        # Test
        args = (1, 1, 'WideareaName', 1, [1])
        result = crawler.crawling(args)

        # Check
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        for item in result:
            self.assertIsInstance(item, list)
            self.assertEqual(len(item), 7)  # Update to match the actual number of elements in data_list

        self.assertEqual(result[0], ['WideareaName', 'BasareaName1', 'theacd1', 'TheaterName1', 'MovieTitle1', '10:00', '7월 1일'])

    @patch('crawler.webdriver.Chrome')
    def test_init_driver(self, MockWebDriver):
        driver = MockWebDriver.return_value
        driver.get.return_value = None

        result = crawler.init_driver()
        self.assertEqual(result, driver)
        driver.get.assert_called_once_with('https://www.kobis.or.kr/kobis/business/mast/thea/findTheaterSchedule.do')

if __name__ == '__main__':
    unittest.main()
