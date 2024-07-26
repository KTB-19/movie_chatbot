# -*- encoding: utf-8 -*-

import json
import sys

query = sys.argv[0]
print(query)

movieName = "코난"
region = "경기도 구리시"
date = "2024-07-24"


json_object = {
    "movieName": movieName,
    "region": region,
    "date": date,
}

result = json.dumps(json_object)