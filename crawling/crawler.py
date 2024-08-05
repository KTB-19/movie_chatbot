from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException
import time

def init_driver():
    # 드라이버 설정
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://www.kobis.or.kr/kobis/business/mast/thea/findTheaterSchedule.do')
    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#content > div.schedule > div.fl.step1.on > ul > li')))
    return driver

def safe_find_element(driver, selector, title):
    # 에러 발생한 경우 재시도
    retries = 5
    for _ in range(retries):
        try:
            element = driver.find_element(By.CSS_SELECTOR, selector)
            return element
        except (StaleElementReferenceException, NoSuchElementException) as e:
            if title==True:
                return None
            if _ == retries - 1:
                print(f"재시도 중 에러 발생: {selector}{type(e).__name__}")
            time.sleep(1)
    return None

def wait_for_element_to_be_clickable(driver, selector, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, selector)))

def crawling(args):
    initial, index, widearea_name, len_b, division = args
    data_list = []
    driver = init_driver()
    if initial == 1:
        # 6일 후의 날짜로 이동
        for _ in range(6):
            try:
                day_selector = '//*[@id="next"]'
                day_element = wait_for_element_to_be_clickable(driver, day_selector)
                if day_element:
                    driver.execute_script("arguments[0].scrollIntoView();", day_element)  # 스크롤
                    day_element.click()
                    time.sleep(1)
                    # movie_date = driver.find_element(By.XPATH, "//*[@id='content']/div[3]/div[4]/div/p/strong")
                    # print(movie_date.text)

            except Exception as e:
                print(f"날짜 변경 중 에러 발생: {type(e).__name__}")

    for curday in range(initial):
        if curday != 0:
            try:
                day_selector = '//*[@id="next"]'
                day_element = wait_for_element_to_be_clickable(driver, day_selector)
                if day_element:
                    driver.execute_script("arguments[0].scrollIntoView();", day_element)  # 스크롤
                    day_element.click()
                    time.sleep(2)

            except ElementClickInterceptedException as e:
                print(f"날짜 변경 중 에러 발생: {type(e).__name__}")
            except Exception as e:
                print(f"날짜 변경 중 에러 발생: {type(e).__name__}")


        current_date = driver.find_element(By.XPATH, '//*[@id="content"]/div[3]/div[4]/div/p').text
        try:
            w_selector = f"#content > div.schedule > div.fl.step1.on > ul > li:nth-child({index})"
            w_element = safe_find_element(driver, w_selector, title=False)
            if w_element is None:
                print('cannot find w_element')
                return

            wideareacd_value = w_element.get_attribute("wideareacd")
            if wideareacd_value:
                widearea_name = w_element.text

                # 광역 재선택(에러 방지를 위해)
                w_element.click()
                time.sleep(2)
                WebDriverWait(driver, 20).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#sBasareaCd > li')))

            start = division[0]
            end = division[-1] + 1
            for j in range(start, end):
                if j > len_b:
                    continue
                try:
                    b_selector = f"#content > div.schedule > div.fl.step2.on > ul > li:nth-child({j})"
                    b_element = safe_find_element(driver, b_selector, title=False)
                    if b_element is None:
                        print('cannot find b_element')
                        continue

                    basareacd_value = b_element.get_attribute("basareacd")
                    if basareacd_value:
                        basarea_name = b_element.text

                        # 기초 선택
                        b_element.click()
                        time.sleep(2)
                        WebDriverWait(driver, 20).until(
                            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#sTheaCd > li')))

                        theater_elements = driver.find_elements(By.CSS_SELECTOR, "#sTheaCd > li")
                        for h in range(1, len(theater_elements) + 1):
                            try:
                                theater_selector = f"#sTheaCd > li:nth-child({h})"
                                theater_element = safe_find_element(driver, theater_selector, title=False)
                                if theater_element is None:
                                    print(widearea_name, basarea_name, 'cannot find theater_element')
                                    continue

                                if "영화상영관 없음" in theater_element.text:
                                    print(widearea_name, basarea_name, '영화상영관 없음')
                                    continue

                                theatercd_value = theater_element.get_attribute("theacd")
                                if theatercd_value:
                                    theater_name = theater_element.text

                                    # 영화관 선택
                                    theater_element.click()
                                    time.sleep(2)
                                    WebDriverWait(driver, 20).until(
                                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#schedule > li')))

                                    # print("Theater Name:", theater_name)
                                    movie_elements = driver.find_elements(By.CSS_SELECTOR, "#schedule > li")
                                    for k in range(1, len(movie_elements) + 1):
                                        try:
                                            title_selector = f"#schedule > li:nth-child({k}) > div.tit > a"
                                            title_element = safe_find_element(driver, title_selector, title=True)
                                            if title_element is None:
                                                print(widearea_name, basarea_name, '상영스케줄 없음', theater_name)
                                                continue
                                            movie_title = title_element.text

                                            time_elements = driver.find_elements(By.CSS_SELECTOR,
                                                                                 f"#schedule > li:nth-child({k}) > div.times > label")
                                            for time_element in time_elements:
                                                movie_time = time_element.text
                                                movie_date = safe_find_element(driver,
                                                                               "#content > div.schedule > div.ovf.step4.on > div > p",
                                                                               title=False).text
                                                # 데이터 수집 => 추후 database에 넣는 것으로 변경 예정
                                                data_list.append([
                                                    widearea_name, basarea_name,
                                                    theatercd_value, theater_name,
                                                    movie_title, movie_time, movie_date
                                                ])
                                        except Exception as e:
                                            print(f"영화 항목에서 에러 발생: {theater_name} {type(e).__name__}")
                                            continue
                            except Exception as e:
                                print(f"극장 항목에서 에러 발생: {type(e).__name__}")
                                continue
                except Exception as e:
                    print(f"기초 지역 항목 {j}에서 에러 발생: {type(e).__name__}")
                    continue
        except Exception as e:
            print(f"크롤링 중 에러 발생: {type(e).__name__}")

    driver.quit()
    return data_list

