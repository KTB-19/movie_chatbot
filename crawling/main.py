import time
import csv

from apscheduler.triggers.date import DateTrigger

import process_division
import database.connect_db, database.insert_data
import schedule
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

# def save_to_csv(data_list, filename):
#     headers = ["widearea_name", "basarea_name", "theater_id", "theater_name", "movie_title", "movie_time_str", "movie_date_str"]
#     with open(filename, mode='w', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         writer.writerow(headers)
#         writer.writerows(data_list)
#
# def load_from_csv(filename):
#     data_list = []
#     with open(filename, mode='r', newline='', encoding='utf-8') as file:
#         reader = csv.reader(file)
#         next(reader)
#         for row in reader:
#             data_list.append(row)
#     return data_list

def job():
    data_list = []
    divisions = [i for i in range(1, 18)]

    for i in divisions:
        data_list.extend(process_division.process_division(i, initial=False))

    print("final: ", len(data_list))
    print("--- %s 초 ---" % (time.time() - start_time))

    # widearea_name, basarea_name, theater_id, theater_name, movie_title, movie_time_str, movie_date_str = data
    # testdata = [["testwide", 'testbas', 'testtid', 'testtname', 'testmname', '09:00', '8월 4일']]

    # database.connect_db.insert_data(data_list)
    # database.insert_data.insert_data(testdata)

    # print("--- %s 초 ---" % (time.time() - start_time))

def job_for7days():
    data_list = []
    divisions = [i for i in range(1, 18)]

    for i in divisions:
        data_list.extend(process_division.process_division(i, initial=True))

    print("final: ", len(data_list))
    print("--- %s 초 ---" % (time.time() - start_time))

    # widearea_name, basarea_name, theater_id, theater_name, movie_title, movie_time_str, movie_date_str = data
    # testdata = [["testwide", 'testbas', 'testtid', 'testtname', 'testmname', '09:00', '8월 4일']]

    # database.connect_db.insert_data(data_list)
    # database.insert_data.insert_data(testdata)

    # print("--- %s 초 ---" % (time.time() - start_time))



if __name__ == '__main__':
    start_time = time.time()
    data_list = []

    # 매일 오전 9시마다
    # schedule.every().day.at("09:00").do(job)


    # csv_filename = 'output_data.csv'

    # Save data to CSV file
    # save_to_csv(data_list, 'output_data.csv')

    # print("finished")
    # loaded_data = load_from_csv(csv_filename)

    # database.connect_db.create_tables()
    # database.insert_data.insert_data(loaded_data)

    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

    # 스케줄러 생성
    scheduler = BackgroundScheduler()

    # 실행 시간 설정
    run_time = datetime(2024, 8, 5, 10, 54)

    # 작업 추가
    scheduler.add_job(job_for7days, trigger=DateTrigger(run_date=run_time))

    # 스케줄러 시작
    scheduler.start()

    # 스케줄러가 실행되는 동안 종료되지 않도록 유지
    try:
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()