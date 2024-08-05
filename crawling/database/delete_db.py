import pymysql
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

def delete_data():
    load_dotenv()
    host = os.getenv('DB_HOST')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')

    conn = pymysql.connect(host=host, user=user, passwd=password, charset='utf8', database='moviedatabase')
    cur = conn.cursor()

    try:
        # 어제의 날짜 받아오기
        yesterday_date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')

        # info table에서 date 컬럼이 어제의 날짜와 같은 데이터 전부 삭제
        delete_query = "DELETE FROM info WHERE date = %s"
        cur.execute(delete_query, (yesterday_date,))
        conn.commit()

    except Exception as e:
        print(f"어제의 데이터 삭제 중 Error occurred: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()
