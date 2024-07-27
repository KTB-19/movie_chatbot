# -*- encoding: utf-8 -*-

import json
import sys

movieNameQuery = sys.argv[0]
print(movieNameQuery)
regionQuery = sys.argv[1]
dateQuery = sys.argv[2]

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

result = json.dumps(json_object)