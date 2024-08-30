from query_ai_process import api_call
from theater_processing import load_theater_data, create_recommendation_message

# 영화관 추천 함수 호출
def recommend_theaters(entities, db):
    # 영화관 주소 데이터 로드
    theater_df = load_theater_data()

    system_message = """
    당신은 영화관 추천을 도와주는 고객지원 챗봇 '무비빔밥'입니다.
    db에는 사용자가 입력한 영화명, 날짜, 시간, 지역에 맞는 상영스케줄 정보가 저장되어 있습니다.
    check_entities 함수의 결과 값인 영화 이름, 장소, 날짜, 시간을 만족하는 영화스케줄을 entities에서 찾고, 영화관을 기준으로 추천하세요.
    반드시 db에 저장된 영화스케줄 정보만을 사용하여, 가장 적합한 영화관을 추천해야 합니다. db에 없는 영화스케줄이나 영화관 정보는 절대 사용하지 마세요.
    또한 챗봇이 추천하는 영화관은 다음 기준도 동시에 만족해야 합니다. 영화관 필터링 기준은 다음과 같습니다:
    
        1. 사용자가 입력한 위치 근처에서 교통 접근성이 좋은 영화관을 우선순위에 두세요.
        2. 사용자가 보고 싶은 영화를 상영하는 횟수가 많은 영화관을 우선순위로 두세요.

    필터링을 거쳐 검색된 영화관 중 상위 3개의 영화관을 추천하는 응답을 생성하세요. 응답을 생성하는 조건은 다음과 같습니다:
    
        1. 상위 3개의 영화관은 각각 다른 영화관이어야 합니다. 지역 내 영화관이 3개 미만일 경우 1개 또는 2개의 영화관만 추천하세요.
        2. movieName으로 설정된 영화의 상영스케줄만 출력하세요. 다른 영화의 스케줄은 절대로 출력하지 마세요.
        3. 단, 상영스케줄은 사용자가 입력한 시간 이후에 상영하는 해당 영화의 회차만 출력해야 합니다. 예를 들어, 사용자가 12:00라고 입력한 경우 12:00 이후에 상영하는 회차를 모두 출력하세요.
        4. 단, 영화 예매를 도와주겠다는 내용은 언급하지 마세요.
        5. 응답은 모두 한국어로 하세요.

    추천된 영화관에 대한 추가 정보를 제공하기 위해, 영화관의 위치(예: 경기도 성남시 분당구)와 주소 데이터를 바탕으로 교통 정보를 알려주세요. 이때 고려해야 할 사항은 다음과 같습니다:
    
        1. 영화관 근처 지하철역 이름을 제공하고, 지하철역의 몇 번 출구에서 나와야 하는지와 영화관까지 도보로 몇 분이 걸리는지 안내하세요.
        2. 만약 근처에 지하철역이 없다면, 대체할 수 있는 버스 정류장 정보나 주요 교통 수단을 안내하세요.
    """

    user_message = f"사용자는 '{entities['movieName']}' 영화를 '{entities['date']}'에 '{entities['region']}'에서 보고 싶어합니다."
    recommendation_context = create_recommendation_message(entities, db, theater_df)

    # ChatGPT API 호출
    recommendMessage = api_call(system_message, user_message + " " + recommendation_context)

    return recommendMessage




'''# 테스트용 코드
entities = {
    "movieName": "에이리언: 로물루스",
    "region": "성남시 분당구",
    "date": "2024-08-30",
    "time": "12:00"
}

db = {
    "movieName": "에이리언: 로물루스",
    "date": "2024-08-30",
    "timesPerTheaterNameMap": {
        "메가박스 분당": ["11:00", "14:00", "17:00"],
        "CGV 오리": ["12:00", "15:00", "18:00"],
        "CGV 서현": ["13:00", "16:00", "19:00"],
        "CGV 판교": ["14:00", "17:00", "20:00"]
    }
}

# 최종 결과 출력
recommendation = recommend_theaters(entities, db)
print(recommendation)'''
