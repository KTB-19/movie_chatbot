# 입력한 정보가 정확한지 확인
from app.services.datetime_format import format_date_time
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
    # 필수 엔티티 정보
    entity_info = [
        ("movieName", "영화 제목"),
        ("region", "지역"),
        ("date", "날짜")
    ]

    missing_entities = []
    for key, message in entity_info:
        value = entities.get(key)

        # missing_entities: value가 None / 빈 문자열 / 빈 문자열만 포함된 리스트인 경우 
        if not value or (isinstance(value, list) and all(not v.strip() for v in value)):
            missing_entities.append(message)
        elif isinstance(value, list):
            # 리스트가 전달된 경우, 리스트의 모든 유효한 값을 쉼표로 구분하여 연결
            entities[key] = ', '.join([v.strip() for v in value if v.strip()])

    
    if missing_entities:
        # 엔티티가 하나 이상 채워지지 않은 경우 다시 질문하기
        if len(missing_entities) > 1:
            missing_str = ' 와 '.join(missing_entities)
            user_message = f"관람하고 싶은 {missing_str}을 말씀해 주세요."
        else:
            user_message = f"관람하고 싶은 {missing_entities[0]}을 말씀해 주세요."
    else:
        # 엔티티가 모두 채워진 경우 확인 문장 출력
        if "time" in entities and entities["time"]:
            entities['date'], entities['time'] = format_date_time(entities['date'], entities['time'])   # 날짜, 시간 형식 변경 적용
            user_message = f"{entities['date']} {entities['time']}에 {entities['region']}에서 {entities['movieName']}을(를) 보고 싶은 게 맞으신가요?"
        else:
            entities['date'], _ = format_date_time(entities['date'], None)   # 사용자가 시간은 입력하지 않은 경우
            user_message = f"{entities['date']}에 {entities['region']}에서 {entities['movieName']}을(를) 보고 싶은 게 맞으신가요?"
    
    return user_message, entities
