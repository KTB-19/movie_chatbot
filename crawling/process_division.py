import time
from multiprocessing import Pool
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, InvalidSelectorException, \
    TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from crawler import crawling, safe_find_element, init_driver
import os

def process_division(i, initial):
    data_list = []
    try:
        driver = init_driver()
        time.sleep(1)

        w_selector = f"#content > div.schedule > div.fl.step1.on > ul > li:nth-child({i})"
        w_element = safe_find_element(driver, w_selector, title=False)
        if w_element is None:
            return data_list
        wideareacd_value = w_element.get_attribute("wideareacd")
        if wideareacd_value:
            widearea_name = w_element.text

            # 광역 선택
            w_element.click()
            time.sleep(1)
            WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#sBasareaCd > li')))
            basarea_elements = driver.find_elements(By.CSS_SELECTOR, "#sBasareaCd > li")

            # 선택한 광역 단체에 해당하는 기초 단체 목록의 길이에 따라 프로세스 분배
            # 최대 가용한 cpu 수와 기초단체 목록 길이에 따라 chuck size 변경
            l = [i for i in range(1, len(basarea_elements) + 1)]

            # 최대 가용한 cpu 수 설정
            my_cpu_count = os.cpu_count() # 크롤링 서버 환경 - Bryan
            chunk_size = max((len(basarea_elements) // my_cpu_count) + (1 if len(basarea_elements) % my_cpu_count != 0 else 0), 1)
            sub_divisions = [l[i:i + chunk_size] for i in range(0, len(l), chunk_size)]
            args_list = [(initial, i, widearea_name, len(basarea_elements), div) for div in sub_divisions]
            data_list.extend(_process_with_multiprocessing(crawling, args_list, len(sub_divisions)))
            driver.quit()

    except (NoSuchElementException, StaleElementReferenceException, InvalidSelectorException, TimeoutException) as e:
        print(f"광역 지역 처리 중 에러 (i={i}): {type(e).__name__}")

    return data_list

def _process_with_multiprocessing(func, args_list, l):
    data_list=[]
    # multiprocessing
    with Pool(processes=l) as pool:
        results = pool.map(func, args_list)
        for result in results:
            data_list.extend(result)
    return data_list
