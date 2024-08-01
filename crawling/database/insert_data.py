import pymysql
from dotenv import load_dotenv
import os
from datetime import datetime, time, timedelta

def convert_time(time_str):
    hours, minutes = map(int, time_str.split(":"))
    if hours >= 24:
        hours = hours % 24
        movie_time = time(hours, minutes)
        return movie_time, 1
    else:
        movie_time = time(hours, minutes)
        return movie_time, 0

def convert_date(date_str, flag):
    month_day = datetime.strptime(date_str, "%m월 %d일")
    movie_date = month_day.replace(year=2024).date()
    if flag == 1:
        # 날짜에 하루를 더하기 위해 day를 +1
        movie_date = movie_date + timedelta(days=1)
    return movie_date

def insert_data(data_list):
    load_dotenv()
    host = os.getenv('DB_HOST')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')

    conn = pymysql.connect(host=host, user=user, passwd=password, db='testDB', charset='utf8')
    cur = conn.cursor()

    try:
        for data in data_list:
            widearea_name, basarea_name, theater_id, theater_name, movie_title, movie_time_str, movie_date_str = data

            # time, date 형식에 맞게 변환
            movie_time, flag = convert_time(movie_time_str)
            movie_date = convert_date(movie_date_str, flag)

            # movie가 이미 movie table에 있는지 확인
            cur.execute("SELECT movie_id FROM movie WHERE title = %s", (movie_title,))
            movie_result = cur.fetchone()

            if movie_result:
                movie_id = movie_result[0]
            else:
                # Insert into movie table
                cur.execute("INSERT INTO movie (title) VALUES (%s)", (movie_title,))
                movie_id = cur.lastrowid  # Get the last inserted movie_id

            # theater가 이미 theater table에 있는지 확인
            cur.execute("SELECT theater_id FROM theater WHERE name = %s", (theater_name,))
            theater_result = cur.fetchone()

            if theater_result:
                theater_id = theater_result[0]
            else:
                # Insert into theater table
                cur.execute("INSERT INTO theater (theater_id, name, wide_area, basic_area) VALUES (%s, %s, %s, %s)",
                            (theater_id, theater_name, widearea_name, basarea_name))

            # Insert into info table
            cur.execute("INSERT INTO info (movie_id, theater_id, time, date) VALUES (%s, %s, %s, %s)",
                        (movie_id, theater_id, movie_time, movie_date))

        conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()