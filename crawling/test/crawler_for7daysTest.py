import unittest
from unittest.mock import patch, MagicMock
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import crawler_for7days

class TestCrawlerFor7Days(unittest.TestCase):

    @patch('crawler.webdriver.Chrome')
    def test_safe_find_element(self, MockWebDriver):
        driver = MockWebDriver.return_value
        element = MagicMock()
        driver.find_element.return_value = element

        # 정상 동작하는 경우
        result = crawler_for7days.safe_find_element(driver, 'selector')
        self.assertEqual(result, element)

        # StaleElementReferenceException 발생하는 경우
        driver.find_element.side_effect = [StaleElementReferenceException, element]
        result = crawler_for7days.safe_find_element(driver, 'selector')
        self.assertEqual(result, element)

        # NoSuchElementException 발생하는 경우
        driver.find_element.side_effect = [NoSuchElementException, element]
        result = crawler_for7days.safe_find_element(driver, 'selector')
        self.assertEqual(result, element)

    @patch('crawler_for7days.init_driver')
    @patch('crawler_for7days.safe_find_element')
    @patch('crawler_for7days.WebDriverWait')
    @patch('crawler_for7days.time.sleep', return_value=None)
    def test_crawling_for7days(self, mock_sleep, mock_WebDriverWait, mock_safe_find_element, mock_init_driver):
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
        args = (1, 'WideareaName', 1, [1])
        result = crawler_for7days.crawling_for7days(args)

        # Check
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        for item in result:
            self.assertIsInstance(item, list)
            self.assertEqual(len(item), 7)

        self.assertEqual(result[0], ['WideareaName', 'BasareaName1', 'theacd1', 'TheaterName1', 'MovieTitle1', '10:00', '7월 1일'])

    @patch('crawler_for7days.webdriver.Chrome')
    def test_init_driver(self, MockWebDriver):
        driver = MockWebDriver.return_value
        driver.get.return_value = None

        result = crawler_for7days.init_driver()
        self.assertEqual(result, driver)
        driver.get.assert_called_once_with('https://www.kobis.or.kr/kobis/business/mast/thea/findTheaterSchedule.do')

if __name__ == '__main__':
    unittest.main()
