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


# 입력한 정보가 정확한지 확인
def check_entities(entities):
    # 필수 엔티티
    entity_info = [("movieName", "영화 제목"), ("region", "지역"), ("date", "날짜")]
    
    # 누락된 필수 엔티티 확인
    missing_entities = [
        message for key, message in entity_info 
        if not entities.get(key) or entities[key] == '' or entities[key] == ['']
    ]

    # None, 빈 문자열, 빈 리스트 처리
    for key in entities:
        if isinstance(entities[key], list):
            continue
        if not entities[key] or entities[key] == '':
            entities[key] = None

    # 시간 형식 변환
    if entities.get("time"):
        entities['time'] = format_time(entities['time'])

    # 엔티티가 하나라도 누락된 경우
    if missing_entities: 
        missing_str = ', '.join(missing_entities)       # 엔티티 연결은 모두 ','로
        user_message = f"{missing_str}가(이) 누락되었습니다. 관람하고 싶은 {missing_str}을(를) 말씀해 주세요."

        print("missing_str",missing_str)
    # 엔티티가 모두 채워진 경우
    else:
        time_str = f" {entities['time']}에" if entities.get("time") else ""
        user_message = f"{entities['date']}{time_str} {entities['region']}에서 {entities['movieName']}을(를) 관람하고 싶은 게 맞으신가요?"
    print("entities",entities)

    return user_message, entities


def data_cleaning(ref_text: str) -> str:
    cleaned_data_json = ref_text.replace('json', '')
    cleaned_data_back = cleaned_data_json.replace('```', '')
    cleaned_data = cleaned_data_back.strip()
    return cleaned_data