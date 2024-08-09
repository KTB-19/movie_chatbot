# -*- encoding: utf-8 -*-

import json

def parseQueries(movieNameQuery, regionQuery, dateQuery):

    print(movieNameQuery)
    print(regionQuery)
    print(dateQuery)

    # 입력 값에서 추출할 수 없는 것은 None 반환
    movieName = None
    region = "경기도 구리시"
    date = "2024-07-27"

    json_object = {
        "movieName": movieName,
        "region": region,
        "date": date,
    }

    return json.dumps(json_object)