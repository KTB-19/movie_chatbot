import time
from apscheduler.triggers.date import DateTrigger
import process_division
import database.insert_db, database.delete_db
import schedule
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

def job():
    data_list = []
    divisions = [i for i in range(1, 18)]

    # 어제의 데이터 삭제
    database.delete_db.delete_data()

    for i in divisions:
        data_list.extend(process_division.process_division(i, initial=1))

    print("final: ", len(data_list))
    print("--- %s 초 ---" % (time.time() - start_time))

    database.insert_db.insert_data(data_list)

    print("--- %s 초 ---" % (time.time() - start_time))

def job_for7days():
    data_list = []
    divisions = [i for i in range(1, 18)]

    for i in divisions:
        data_list.extend(process_division.process_division(i, initial=7))

    print("final: ", len(data_list))
    print("--- %s 초 ---" % (time.time() - start_time))

    database.insert_db.insert_data(data_list)

    print("--- %s 초 ---" % (time.time() - start_time))



if __name__ == '__main__':
    start_time = time.time()
    data_list = []

    # 7일치 크롤을 위한 스케줄러 생성(1회만 실행 후 종료)
    scheduler = BackgroundScheduler()

    # 실행 시간 설정
    """변경해야 하는 부분. 최초 크롤링에 대한 시간 설정"""
    run_time = datetime(2024, 8, 7, 19, 6)

    scheduler.add_job(job_for7days, trigger=DateTrigger(run_date=run_time))
    scheduler.start()

    while True:
        pending_jobs = scheduler.get_jobs()
        if not pending_jobs:
            break
        time.sleep(1)


    # 매일 오전 9시마다
    schedule.every().day.at("19:07").do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)