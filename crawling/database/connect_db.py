"""FOR LOCAL DATABASE"""

import pymysql
# from dotenv import load_dotenv
# import os
#
# def create_tables():
#     load_dotenv()
#     host = os.getenv('DB_HOST')
#     user = os.getenv('DB_USER')
#     password = os.getenv('DB_PASSWORD')
#
#     # Connect & DB 초기화
#     try:
#         conn = pymysql.connect(host=host, user=user, passwd=password, charset='utf8')
#         with conn.cursor() as cur:
#             cur.execute('DROP DATABASE IF EXISTS `testDB`')
#             cur.execute('CREATE DATABASE IF NOT EXISTS testDB')
#             conn.commit()
#     except pymysql.MySQLError as e:
#         print(f"An error occurred while creating the database: {e}")
#         return
#     finally:
#         conn.close()
#
#     # Connect & Create table
#     try:
#         conn = pymysql.connect(host=host, user=user, passwd=password, charset='utf8')
#         with conn.cursor() as cur:
#             # Create tables
#             create_movie_table = """
#             CREATE TABLE IF NOT EXISTS movie (
#                 movie_id INT PRIMARY KEY AUTO_INCREMENT,
#                 title VARCHAR(50)
#             );
#             """
#
#             create_theater_table = """
#             CREATE TABLE IF NOT EXISTS theater (
#                 theater_id INT PRIMARY KEY,
#                 name VARCHAR(50),
#                 wide_area VARCHAR(10),
#                 basic_area VARCHAR(10)
#             );
#             """
#
#             create_info_table = """
#             CREATE TABLE IF NOT EXISTS info (
#                 info_id INT PRIMARY KEY AUTO_INCREMENT,
#                 movie_id INT,
#                 theater_id INT,
#                 time TIME,
#                 date DATE,
#                 FOREIGN KEY (movie_id) REFERENCES movie(movie_id),
#                 FOREIGN KEY (theater_id) REFERENCES theater(theater_id)
#             );
#             """
#
#             cur.execute(create_movie_table)
#             cur.execute(create_theater_table)
#             cur.execute(create_info_table)
#             conn.commit()
#     except pymysql.MySQLError as e:
#         print(f"An error occurred while creating tables: {e}")
#         conn.rollback()
#     finally:
#         conn.close()
#
