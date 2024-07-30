from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from multiprocessing import Pool
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

def safe_find_element(driver, selector, retries=5):
    for i in range(retries):
        try:
            element = driver.find_element(By.CSS_SELECTOR, selector)
            return element
        except (StaleElementReferenceException, NoSuchElementException) as e:
            if i == retries - 1:
                print(f"Error in safe_find_element: {type(e).__name__}")
            time.sleep(2)
    return None

def init_chrome_driver():
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    return webdriver.Chrome(options=chrome_options)

def process_bas_area(args):
    w_element, widearea_name, basarea_elements, division = args
    print(widearea_name, division)
    driver = init_chrome_driver()
    driver.get('https://www.kobis.or.kr/kobis/business/mast/thea/findTheaterSchedule.do')
    data_list = []
    start = division[0]
    end = division[-1] + 1

    w_element.click()
    for j in range(start, end):
        if j > len(basarea_elements):
            continue
        try:
            basarea_element = f"#content > div.schedule > div.fl.step2.on > ul > li:nth-child({j})"
            basarea_element.click()
            time.sleep(1)
            b_selector = f"#content > div.schedule > div.fl.step2.on > ul > li:nth-child({j})"
            b_element = safe_find_element(driver, b_selector)
            if b_element is None:
                continue
            basareacd_value = b_element.get_attribute("basareacd")

            if basareacd_value:
                basarea_name = b_element.text
                b_element.click()
                time.sleep(1)
                WebDriverWait(driver, 20).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#sTheaCd > li'))
                )

                theater_elements = driver.find_elements(By.CSS_SELECTOR, "#sTheaCd > li")

                for h in range(1, len(theater_elements) + 1):
                    try:
                        theater_selector = f"#sTheaCd > li:nth-child({h})"
                        theater_element = safe_find_element(driver, theater_selector)
                        if theater_element is None or "영화상영관 없음" in theater_element.text:
                            continue

                        theatercd_value = theater_element.get_attribute("theacd")
                        if theatercd_value:
                            theater_name = theater_element.text
                            theater_element.click()
                            time.sleep(1)
                            WebDriverWait(driver, 20).until(
                                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#schedule > li'))
                            )

                            movie_elements = driver.find_elements(By.CSS_SELECTOR, "#schedule > li")

                            for k in range(1, len(movie_elements) + 1):
                                try:
                                    title_selector = f"#schedule > li:nth-child({k}) > div.tit"
                                    title_element = safe_find_element(driver, title_selector)
                                    if title_element is None or "상영스케줄이 없습니다." in title_element.text:
                                        continue

                                    title_element = safe_find_element(driver, title_selector + " > a")
                                    if title_element is None:
                                        continue
                                    movie_title = title_element.text

                                    time_elements = driver.find_elements(By.CSS_SELECTOR,
                                                                         f"#schedule > li:nth-child({k}) > div.times > label")
                                    for time_element in time_elements:
                                        movie_time = time_element.text
                                        movie_date = safe_find_element(driver,
                                                                       "#content > div.schedule > div.ovf.step4.on > div > p").text

                                        data_list.append([
                                            wideareacd_value, widearea_name,
                                            basareacd_value, basarea_name,
                                            theatercd_value, theater_name,
                                            movie_title, movie_time, movie_date
                                        ])

                                except (NoSuchElementException, StaleElementReferenceException) as e:
                                    print(
                                        f"Error in process_bas_area (movie_elements loop) {theater_name}: {type(e).__name__}")

                    except (NoSuchElementException, StaleElementReferenceException) as e:
                        print(f"Error in process_bas_area (theater_elements loop): {type(e).__name__}")

        except (NoSuchElementException, StaleElementReferenceException) as e:
            print(f"Error in process_bas_area (basarea_elements loop): {type(e).__name__}")

    driver.quit()
    return data_list

def divide():
    return [[i] for i in range(1, 18)]

if __name__ == '__main__':
    start_time = time.time()
    divisions = divide()

    driver = init_chrome_driver()
    driver.get('https://www.kobis.or.kr/kobis/business/mast/thea/findTheaterSchedule.do')

    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#content > div.schedule > div.fl.step1.on > ul > li'))
    )
    widearea_elements = driver.find_elements(By.CSS_SELECTOR, '#content > div.schedule > div.fl.step1.on > ul > li')

    data_list = []

    for division in divisions:
        start = division[0]
        end = division[-1] + 1

        for i in range(start, end):
            try:
                w_selector = f"#content > div.schedule > div.fl.step1.on > ul > li:nth-child({i})"
                w_element = driver.find_element(By.CSS_SELECTOR, w_selector)
                wideareacd_value = w_element.get_attribute("wideareacd")

                if wideareacd_value:
                    widearea_name = w_element.text
                    w_element.click()
                    time.sleep(3)
                    WebDriverWait(driver, 20).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#sBasareaCd > li'))
                    )

                    basarea_elements = driver.find_elements(By.CSS_SELECTOR, "#sBasareaCd > li")

                    l = [i for i in range(1, len(basarea_elements) + 1)]
                    chunk_size = 4
                    sub_divisions = [l[i:i + chunk_size] for i in range(0, len(l), chunk_size)]
                    args_list = [(w_element, widearea_name, basarea_elements, div) for div in sub_divisions]

                    with Pool(processes=len(sub_divisions)) as pool:
                        results = pool.map(process_bas_area, args_list)
                        for result in results:
                            data_list.extend(result)

            except (NoSuchElementException, StaleElementReferenceException) as e:
                print(f"Error in processing widearea (i={i}): {type(e).__name__}")

    driver.quit()

    print("Infos:", len(data_list))
    print("— %s seconds —" % (time.time() - start_time))
