# 입력한 정보가 정확한지 확인
from app.services.datetime_format import format_date_time, format_date, format_time
import json
def check_json_entities(response):
    try:
        # JSON 형식의 응답을 딕셔너리로 변환합니다.
        response_dict = json.loads(response)

    except json.JSONDecodeError as e:
        # JSON 디코딩 중 오류가 발생한 경우
        print(f"JSON 디코딩 오류: {e}")
        # 에러가 발생해도 response_dict는 기본값을 유지합니다.

    except Exception as e:
        # 다른 예외가 발생한 경우
        print(f"오류 발생: {e}")
        # 에러가 발생해도 response_dict는 기본값을 유지합니다.

    return response_dict


def check_entities(entities):

    # 날짜, 시간 형식 변경 적용
    if entities['date']:
        entities['date'] = format_date(entities['date'])

    if entities['time']:
        entities['time'] = format_time(entities['time'])

    entity_info = [
        ("movieName", "영화 제목"),
        ("region", "지역"),
        ("date", "날짜"),
        ("time", "시간")
    ]

    missing_entities = []
    for key, message in entity_info:
        if key not in entities or not entities[key]:  # None 또는 False인 값을 걸러냄
            missing_entities.append(message)

    if missing_entities:
        # 엔티티가 2개 이상 누락된 경우
        if len(missing_entities) >= 2:
            missing_str = ' 와 '.join(missing_entities)
            user_message = f"관람하고 싶은 {missing_str}을 말씀해 주세요."
        else:
            user_message = f"관람하고 싶은 {missing_entities[0]}을 말씀해 주세요."
    else:
        # 엔티티가 모두 채워진 경우 확인 문장 출력
        user_message = f"{entities['date']} {entities['time']}에 {entities['region']}에서 {entities['movieName']}을(를) 보고 싶으신 게 맞으신가요?"

    return user_message, entities
