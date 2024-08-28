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
    print("deleted yesterday's data from database")

    print("start crawling")

    for i in divisions:
        data_list.extend(process_division.process_division(i, initial=1))

    print("final: ", len(data_list))
    database.insert_db.insert_data(data_list)
    print("inserted into database", flush=True)


def job_for7days():
    data_list = []
    divisions = [i for i in range(1, 18)]

    print("start crawling")

    for i in divisions:
        data_list.extend(process_division.process_division(i, initial=7))

    print("final: ", len(data_list))
    database.insert_db.insert_data(data_list)
    print("inserted into database(for 7 days)", flush=True)


if __name__ == '__main__':
    # 최초 1회 실행
    job_for7days()

    # 매일 오전 9시마다 실행
    schedule.every().day.at("09:00").do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)