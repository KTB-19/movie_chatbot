import time
import csv
from apscheduler.triggers.date import DateTrigger
import process_division
import database.insert_data, database.delete_db
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

    # database.connect_db.insert_data(data_list)
    # testdata = [["testwide", 'testbas', 1234, 'testtname', 'testmname', '09:00', '8월 4일']]
    # database.insert_data.insert_data(testdata)

    print("--- %s 초 ---" % (time.time() - start_time))

def job_for7days():
    data_list = []
    divisions = [i for i in range(1, 18)]

    for i in divisions:
        data_list.extend(process_division.process_division(i, initial=6))

    print("final: ", len(data_list))
    print("--- %s 초 ---" % (time.time() - start_time))

    # database.connect_db.insert_data(data_list)

    # print("--- %s 초 ---" % (time.time() - start_time))



if __name__ == '__main__':
    start_time = time.time()
    data_list = []

    # job()

    # # 매일 오전 9시마다
    # schedule.every().day.at("09:00").do(job)
    #
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

    # # 스케줄러 생성
    # scheduler = BackgroundScheduler()
    #
    # # 실행 시간 설정
    # run_time = datetime(2024, 8, 5, 17, 18)
    #
    # scheduler.add_job(job_for7days, trigger=DateTrigger(run_date=run_time))
    # scheduler.start()
    #
    # try:
    #     while True:
    #         pass
    # except (KeyboardInterrupt, SystemExit):
    #     scheduler.shutdown()
