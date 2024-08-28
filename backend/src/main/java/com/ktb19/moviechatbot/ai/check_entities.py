# 입력한 정보가 정확한지 확인
def check_entities(entities):
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

    # 엔티티가 2개 이상 누락된 경우
    if missing_entities:
        if len(missing_entities) >= 2:
            missing_str = ' 와 '.join(missing_entities)
            user_message = f"관람하고 싶은 {missing_str}을 말씀해 주세요."
        else:
            user_message = f"관람하고 싶은 {missing_entities[0]}을 말씀해 주세요."
    else:
        # 엔티티가 모두 채워진 경우 확인 문장 출력
        entities['date'], entities['time'] = format_date_time(entities['date'], entities['time'])   # 날짜, 시간 형식 변경 적용
        user_message = f"{entities['date']} {entities['time']}에 {entities['region']}에서 {entities['movieName']}을(를) 보고 싶으신 게 맞으신가요?"

    return user_message, entities
