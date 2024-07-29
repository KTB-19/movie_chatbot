from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from multiprocessing import Pool, Manager
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException

def safe_find_element(driver, selector, retries=5):
    for _ in range(retries):
        try:
            element = driver.find_element(By.CSS_SELECTOR, selector)
            return element
        except (StaleElementReferenceException, NoSuchElementException) as e:
            if _ == retries - 1: print(f"Error in safe_find_element: {type(e).__name__}")
            time.sleep(3)
    return None

def process_bas_area(driver, widearea_name, basarea_elements, theaters, movies, infos, movie_title_to_id, info_id, movie_id_counter, lock, b, cnt):
    for j in range(b, b + 8):
        if j > len(basarea_elements):
            continue
        try:
            b_selector = f"#content > div.schedule > div.fl.step2.on > ul > li:nth-child({j})"
            b_element = safe_find_element(driver, b_selector)
            if b_element is None:
                continue
            basareacd_value = b_element.get_attribute("basareacd")

            if basareacd_value:
                basarea_name = b_element.text
                b_element.click()
                time.sleep(3)
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
                            with lock:
                                cnt.value += 1
                                if not any(t["theater_id"] == theatercd_value for t in theaters):
                                    theaters.append({
                                        "theater_id": theatercd_value,
                                        "name": theater_name,
                                        "location": f"{widearea_name} {basarea_name}"
                                    })
                                    print(theater_name)

                            theater_element.click()
                            time.sleep(3)
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

                                    with lock:
                                        if movie_title not in movie_title_to_id:
                                            movie_id = movie_id_counter.value
                                            movie_id_counter.value += 1

                                            movie_title_to_id[movie_title] = movie_id

                                            movies.append({
                                                "movie_id": movie_id,
                                                "title": movie_title
                                            })
                                        else:
                                            movie_id = movie_title_to_id[movie_title]

                                    time_elements = driver.find_elements(By.CSS_SELECTOR, f"#schedule > li:nth-child({k}) > div.times > label")
                                    for time_element in time_elements:
                                        movie_time = time_element.text
                                        movie_date = safe_find_element(driver, "#content > div.schedule > div.ovf.step4.on > div > p").text
                                        with lock:
                                            infos.append({
                                                "info_id": info_id.value,
                                                "movie_id": movie_id,
                                                "theater_id": theatercd_value,
                                                "time": movie_time,
                                                "date": movie_date
                                            })
                                            info_id.value += 1

                                except (NoSuchElementException, StaleElementReferenceException) as e:
                                    print(f"Error in process_bas_area (movie_elements loop){theater_name}: {type(e).__name__}")

                    except (NoSuchElementException, StaleElementReferenceException) as e:
                        print(f"Error in process_bas_area (theater_elements loop): {type(e).__name__}")

        except (NoSuchElementException, StaleElementReferenceException) as e:
            print(f"Error in process_bas_area (basarea_elements loop): {type(e).__name__}")

def crawling(division, shared_data, lock, cnt):
    theaters = shared_data["theaters"]
    movies = shared_data["movies"]
    infos = shared_data["infos"]
    movie_title_to_id = shared_data["movie_title_to_id"]
    info_id = shared_data["info_id"]
    movie_id_counter = shared_data["movie_id_counter"]

    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=chrome_options)
    time.sleep(3)

    try:
        driver.get('https://www.kobis.or.kr/kobis/business/mast/thea/findTheaterSchedule.do')
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#content > div.schedule > div.fl.step1.on > ul'))
        )
    except TimeoutException as e:
        print(f"Initial load timeout: {type(e).__name__}")
        driver.quit()
        return

    start = division[0]
    end = division[-1] + 1

    for i in range(start, end):
        try:
            w_selector = f"#content > div.schedule > div.fl.step1.on > ul > li:nth-child({i})"
            w_element = safe_find_element(driver, w_selector)
            if w_element is None:
                continue
            wideareacd_value = w_element.get_attribute("wideareacd")

            if wideareacd_value:
                widearea_name = w_element.text
                w_element.click()
                time.sleep(3)
                WebDriverWait(driver, 20).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#sBasareaCd > li'))
                )

                basarea_elements = driver.find_elements(By.CSS_SELECTOR, "#sBasareaCd > li")

                with ThreadPoolExecutor(max_workers=4) as executor:
                    futures = [executor.submit(process_bas_area, driver, widearea_name, basarea_elements, theaters, movies, infos, movie_title_to_id, info_id, movie_id_counter, lock, a, cnt) for a in range(1, len(basarea_elements)+1, 8)]
                    for future in as_completed(futures):
                        try:
                            future.result()
                        except Exception as e:
                            if isinstance(e, StaleElementReferenceException):
                                print("Error in thread: Stale element reference encountered.")
                            else:
                                print(f"Error in thread: {type(e).__name__}")

        except (NoSuchElementException, StaleElementReferenceException) as e:
            print(f"Error in crawling (widearea loop): {type(e).__name__}")

    driver.quit()

def divide():
    return [[1], [2], [3, 4, 5], [6, 7], [8, 9, 10], [11], [12, 13, 14], [15, 16, 17]]

if __name__ == '__main__':
    start_time = time.time()
    with Manager() as manager:
        lock = manager.Lock()
        shared_data = {
            "theaters": manager.list(),
            "movies": manager.list(),
            "infos": manager.list(),
            "movie_title_to_id": manager.dict(),
            "info_id": manager.Value('i', 1),
            "movie_id_counter": manager.Value('i', 1)
        }

        cnt = manager.Value('i', 0)
        divisions = divide()

        with Pool(processes=8) as pool:
            pool.starmap(crawling, [(division, shared_data, lock, cnt) for division in divisions])
            pool.close()
            pool.join()

        print("Infos:", list(shared_data["infos"]))
        print("— %s seconds —" % (time.time() - start_time))
        print(cnt.value)
