import pandas as pd
from config import XLSX_FILE_PATH

# 영화관 주소 데이터 로드
def load_theater_data(xlsx_file_path):
    theater_df = pd.read_excel(xlsx_file_path, header=4, usecols=['광역단체', '기초단체', '영화상영관명', '주소', '전화번호', '홈페이지'], engine='openpyxl')
    return theater_df

# 영화관 추천 응답 생성
def create_recommendation_message(entities, db, theater_df):
    movie_name = entities['movieName']
    location = entities['region']
    date = entities['date']
    
    # 백엔드- 영화스케줄 DB 연결
    matched_theaters = db["timesPerTheaterNameMap"]

    # 상영 횟수로 정렬하기
    sorted_theaters = sorted(matched_theaters.items(), key=lambda x: len(x[1]), reverse=True)

    # 상영 시간 정보와 영화관 정보 결합
    recommendations = []
    for theater_name, showtimes in sorted_theaters[:3]:
        # 해당 영화관명이 있는지 확인
        filtered_df = theater_df[theater_df['영화상영관명'] == theater_name]
        
        if not filtered_df.empty:  # 데이터가 존재할 때만 처리
            theater_info = filtered_df.iloc[0]
            recommendation = {
                "name": theater_name,
                "movieName": movie_name,
                "showtimes": showtimes,
                "address": theater_info['주소']
            }
            recommendations.append(recommendation)
        else:
            print(f"Warning: '{theater_name}'에 해당하는 영화관 정보를 찾을 수 없습니다.")

    # 추천 영화관 정보를 텍스트로 변환
    context = ""
    for rec in recommendations:
        context += f"{rec['name']}에서 '{rec['movieName']}'이 {', '.join(rec['showtimes'])}에 상영됩니다. 주소: {rec['address']}, {rec['transport_info']} "

    return context