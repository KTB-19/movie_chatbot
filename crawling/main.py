from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from multiprocessing import Pool
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, InvalidSelectorException, TimeoutException

def safe_find_element(driver, selector, retries=5, title=False):
    for _ in range(retries):
        try:
            element = driver.find_element(By.CSS_SELECTOR, selector)
            return element
        except (StaleElementReferenceException, NoSuchElementException) as e:
            #타이틀 처리
            if title==True:
                return None
            if _ == retries - 1: print(f"Error in safe_find_element: {selector}{type(e).__name__}")
            time.sleep(1)
            #다시클릭 로직?
    return None

def crawling(args):
    index, widearea_name, len_b, division = args
    data_list = []

    driver = init_driver()

    try:
        w_selector = f"#content > div.schedule > div.fl.step1.on > ul > li:nth-child({index})"
        w_element = safe_find_element(driver, w_selector)
        if w_element is None:
            print('cannot find w_element')
            return

        wideareacd_value = w_element.get_attribute("wideareacd")
        if wideareacd_value:
            widearea_name = w_element.text
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
                b_element = safe_find_element(driver, b_selector)
                if b_element is None:
                    print('cannot find b_element')
                    continue

                basareacd_value = b_element.get_attribute("basareacd")
                if basareacd_value:
                    basarea_name = b_element.text
                    b_element.click()
                    time.sleep(2)
                    WebDriverWait(driver, 20).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#sTheaCd > li')))

                    theater_elements = driver.find_elements(By.CSS_SELECTOR, "#sTheaCd > li")
                    for h in range(1, len(theater_elements) + 1):
                        try:
                            theater_selector = f"#sTheaCd > li:nth-child({h})"
                            theater_element = safe_find_element(driver, theater_selector)
                            if theater_element is None:
                                print(widearea_name, basarea_name, 'cannot find theater_element')
                                continue

                            if "영화상영관 없음" in theater_element.text:
                                print(widearea_name, basarea_name, '영화상영관 없음')
                                continue

                            theatercd_value = theater_element.get_attribute("theacd")
                            if theatercd_value:
                                theater_name = theater_element.text
                                print(theater_name)
                                theater_element.click()
                                time.sleep(2)
                                WebDriverWait(driver, 20).until(
                                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#schedule > li')))

                                movie_elements = driver.find_elements(By.CSS_SELECTOR, "#schedule > li")
                                for k in range(1, len(movie_elements) + 1):
                                    try:
                                        title_selector = f"#schedule > li:nth-child({k}) > div.tit > a"
                                        title_element = safe_find_element(driver, title_selector, title=True)
                                        if title_element is None:
                                            print(widearea_name, basarea_name, '상영스케줄 없음', theater_name)
                                            continue

                                        movie_title = title_element.text

                                        time_elements = driver.find_elements(By.CSS_SELECTOR, f"#schedule > li:nth-child({k}) > div.times > label")
                                        for time_element in time_elements:
                                            movie_time = time_element.text
                                            movie_date = safe_find_element(driver,
                                                                             "#content > div.schedule > div.ovf.step4.on > div > p").text
                                            data_list.append([
                                                widearea_name,
                                                basareacd_value, basarea_name,
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
    print(widearea_name, division, len(data_list))
    return data_list

def divide():
    return [i for i in range(1, 18)]

def init_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://www.kobis.or.kr/kobis/business/mast/thea/findTheaterSchedule.do')
    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#content > div.schedule > div.fl.step1.on > ul > li')))
    return driver

if __name__ == '__main__':
    start_time = time.time()
    data_list = []
    divisions = divide()

    for i in divisions:
        try:
            driver = init_driver()
            time.sleep(1)
            widearea_elements = safe_find_element(driver,
                                                     '#content > div.schedule > div.fl.step1.on > ul > li')

            w_selector = f"#content > div.schedule > div.fl.step1.on > ul > li:nth-child({i})"
            w_element = safe_find_element(driver, w_selector)
            if w_element is None:
                continue
            wideareacd_value = w_element.get_attribute("wideareacd")
            if wideareacd_value:
                widearea_name = w_element.text
                w_element.click()
                time.sleep(1)
                WebDriverWait(driver, 20).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#sBasareaCd > li')))
                basarea_elements = driver.find_elements(By.CSS_SELECTOR, "#sBasareaCd > li")

                l = [i for i in range(1, len(basarea_elements) + 1)]
                chunk_size = (len(basarea_elements) // 10) + (1 if len(basarea_elements) % 10 != 0 else 0)
                sub_divisions = [l[i:i + chunk_size] for i in range(0, len(l), chunk_size)]
                args_list = [(i, widearea_name, len(basarea_elements), div) for div in sub_divisions]
                with Pool(processes=len(sub_divisions)) as pool:
                    results = pool.map(crawling, args_list)
                    for result in results:
                        data_list.extend(result)
            driver.quit()
        except (NoSuchElementException, StaleElementReferenceException, InvalidSelectorException, TimeoutException) as e:
            print(f"광역 지역 처리 중 에러 (i={i}): {type(e).__name__}")

    driver.quit()

    print(len(data_list))
    print("--- %s 초 ---" % (time.time() - start_time))
